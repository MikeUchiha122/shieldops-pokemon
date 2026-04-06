"""
data/rag_engine.py
Motor RAG con ChromaDB para fundamentar estrategias con fuentes locales y web.
Scrapers seguros con rate limiting. Sin pickle, sin eval.
Los archivos subidos (PDFs/guías) se cargan aquí para enriquecer el contexto.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import time
from pathlib import Path
from typing import Any

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════
# Scraper seguro
# ══════════════════════════════════════════════════════════════════════

class SafeScraper:
    """
    Scraper asíncrono con:
    - Rate limiting configurable (respeta ToS)
    - Timeout estricto (no cuelga la app)
    - User-Agent identificado (buena práctica)
    - Sin os.system, sin eval, sin subprocess con input de usuario
    """

    ALLOWED_DOMAINS = frozenset({
        "pikalytics.com",
        "pokemonshowdown.com",
        "pokemon.com",
        "smogon.com",
    })

    def __init__(self, rate_limit_seconds: float = 2.0, user_agent: str = "ShieldOps/1.0") -> None:
        self.rate_limit = rate_limit_seconds
        self._last_request: dict[str, float] = {}
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml",
        }

    def _is_domain_allowed(self, url: str) -> bool:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.lower().removeprefix("www.")
        return domain in self.ALLOWED_DOMAINS

    async def _rate_limit_wait(self, domain: str) -> None:
        now = time.monotonic()
        last = self._last_request.get(domain, 0.0)
        wait = self.rate_limit - (now - last)
        if wait > 0:
            await asyncio.sleep(wait)
        self._last_request[domain] = time.monotonic()

    async def fetch_html(self, url: str) -> str | None:
        """Descarga HTML de una URL permitida. Retorna None si falla."""
        if not self._is_domain_allowed(url):
            logger.warning("Dominio no permitido bloqueado: %s", url)
            return None

        from urllib.parse import urlparse
        domain = urlparse(url).netloc

        await self._rate_limit_wait(domain)

        try:
            async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as exc:
            logger.error("Error HTTP al scrapear %s: %s", url, exc)
            return None

    async def scrape_pikalytics_usage(self) -> list[dict[str, Any]]:
        """Obtiene datos de uso de Pikalytics (lista de Pokémon + % uso)."""
        url = "https://pikalytics.com/pokedex"
        html = await self.fetch_html(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "lxml")
        results: list[dict[str, Any]] = []

        # Estructura de Pikalytics varía — esto es un ejemplo de parsing seguro
        for row in soup.select(".pokemon-usage-row")[:50]:
            name_el  = row.select_one(".pokemon-name")
            usage_el = row.select_one(".usage-percent")
            if name_el and usage_el:
                results.append({
                    "name":  name_el.get_text(strip=True)[:64],    # max 64 chars
                    "usage": usage_el.get_text(strip=True)[:16],
                })

        return results


# ══════════════════════════════════════════════════════════════════════
# Vector DB con ChromaDB
# ══════════════════════════════════════════════════════════════════════

class StrategyVectorDB:
    """
    Wrapper de ChromaDB para almacenar y consultar estrategias.
    Los documentos provienen de:
      1. Archivos locales (PDFs, guías subidas)
      2. Páginas scrapeadas
    """

    def __init__(self, persist_path: str = "./data/vectors", collection_name: str = "pokemon_strategies") -> None:
        self.persist_path   = persist_path
        self.collection_name = collection_name
        self._client         = None
        self._collection     = None

    def _get_client(self) -> Any:
        """Lazy init — importa chromadb solo cuando se necesita."""
        if self._client is None:
            try:
                import chromadb
                from chromadb.config import Settings as ChromaSettings
                self._client = chromadb.PersistentClient(
                    path=self.persist_path,
                    settings=ChromaSettings(anonymized_telemetry=False),
                )
                self._collection = self._client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"},
                )
            except ImportError:
                logger.error("ChromaDB no instalado. Ejecuta: pip install chromadb")
                raise
        return self._client

    def _stable_id(self, text: str) -> str:
        """ID determinístico basado en hash — sin inputs de usuario directos."""
        return hashlib.sha256(text[:512].encode()).hexdigest()[:32]

    def add_document(self, text: str, metadata: dict[str, str] | None = None) -> None:
        """Agrega un documento al vector store."""
        self._get_client()
        doc_id = self._stable_id(text)
        self._collection.upsert(
            documents=[text[:4096]],           # truncar para seguridad
            metadatas=[metadata or {}],
            ids=[doc_id],
        )
        logger.info("Documento indexado: %s", doc_id)

    def query(self, query_text: str, n_results: int = 5) -> list[str]:
        """Consulta semántica — retorna documentos relevantes."""
        self._get_client()
        safe_query = query_text[:512]   # limitar longitud de query
        results    = self._collection.query(
            query_texts=[safe_query],
            n_results=min(n_results, 20),   # cap en 20
        )
        docs: list[str] = results.get("documents", [[]])[0]
        return docs

    def load_text_file(self, path: Path) -> None:
        """
        Carga un archivo de texto/guía al vector store.
        Usado para: PDFs convertidos, guías de crianza, etc.
        Sin pickle — solo texto plano.
        """
        if not path.exists():
            logger.warning("Archivo no encontrado: %s", path)
            return
        if path.suffix.lower() not in {".txt", ".md"}:
            logger.warning("Tipo de archivo no soportado para RAG: %s", path.suffix)
            return

        text = path.read_text(encoding="utf-8", errors="replace")
        # Dividir en chunks para mejor recuperación
        chunk_size = 1000
        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size]
            self.add_document(
                text=chunk,
                metadata={"source": path.name, "chunk": str(i // chunk_size)},
            )
        logger.info("Archivo cargado al RAG: %s (%d chars)", path.name, len(text))
