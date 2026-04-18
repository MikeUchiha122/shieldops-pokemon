"""
cerebros/champions/api/router.py
Router Cerebro D — Pokémon Champions (Singles multi-generacional).
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from core.types import APIResponse
from cerebros.champions.models.schemas import PeticionDanoChampions
from cerebros.champions.engine.damage import calcular_dano
from cerebros.champions.engine.guia import (
    generar_guia_pokemon_champions, generar_mejor_equipo_champions,
)
from cerebros.champions.data.pokemon import (
    POKEMON_CHAMPIONS, buscar_pokemon_champions,
)
from cerebros.champions.data.movimientos import MOVIMIENTOS_CHAMPIONS

router = APIRouter(prefix="/champions", tags=["Cerebro D — Pokémon Champions"])
_VERSION = "1.0.0"


class PeticionGuiaChampions(BaseModel):
    pokemon: str = Field(min_length=1, max_length=64)


class PeticionEquipoChampions(BaseModel):
    pokemon_ancla: str = Field(min_length=1, max_length=64)


@router.post(
    "/dano",
    response_model=APIResponse,
    summary="Calcula daño en Champions (Singles Gen IX, 16 rolls 85–100 %)",
)
def endpoint_dano(req: PeticionDanoChampions) -> APIResponse:
    try:
        resultado = calcular_dano(req)
        return APIResponse(
            cerebro="champions", version=_VERSION, ok=True,
            data=resultado.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        )


@router.post(
    "/guia-pokemon",
    response_model=APIResponse,
    summary="Genera guía Singles con simulación interna vs amenazas meta",
)
def endpoint_guia_pokemon(req: PeticionGuiaChampions) -> APIResponse:
    """
    El cerebro Champions:
    1. Verifica que el Pokémon esté en el catálogo multi-gen
    2. Genera combinaciones de naturaleza × EVs × objeto × movimientos
    3. Simula batallas internas vs las 10 amenazas meta de Champions Singles
    4. Ordena por victorias y score ponderado
    5. Retorna top 3 builds con estadísticas finales y detalles de matchups
    """
    resultado = generar_guia_pokemon_champions(req.pokemon)
    if not resultado.get("ok"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=resultado.get("error"),
        )
    return APIResponse(cerebro="champions", version=_VERSION, ok=True, data=resultado)


@router.post(
    "/mejor-equipo",
    response_model=APIResponse,
    summary="Genera equipo de 6 para Champions Singles alrededor de un Pokémon ancla",
)
def endpoint_mejor_equipo(req: PeticionEquipoChampions) -> APIResponse:
    resultado = generar_mejor_equipo_champions(req.pokemon_ancla)
    if not resultado.get("ok"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=resultado.get("error"),
        )
    return APIResponse(cerebro="champions", version=_VERSION, ok=True, data=resultado)


@router.get(
    "/catalogo",
    response_model=APIResponse,
    summary="Lista todos los Pokémon del catálogo Champions por tier",
)
def endpoint_catalogo(tier: str | None = None) -> APIResponse:
    resultado: list[dict] = []
    for clave, poke in POKEMON_CHAMPIONS.items():
        if tier and poke.get("tier", "").upper() != tier.upper():
            continue
        resultado.append({
            "id": clave,
            "nombre": poke.get("nombre", clave),
            "tipos": poke["tipos"],
            "tier": poke.get("tier", "?"),
        })
    return APIResponse(
        cerebro="champions", version=_VERSION, ok=True,
        data={"total": len(resultado), "tier_filtro": tier, "pokemon": resultado},
    )


@router.get(
    "/movimientos",
    response_model=APIResponse,
    summary="Lista los movimientos disponibles en Champions",
)
def endpoint_movimientos(tipo: str | None = None) -> APIResponse:
    resultado = [
        {"id": k, "nombre": v["nombre"], "tipo": v["tipo"],
         "categoria": v["categoria"], "potencia": v.get("potencia")}
        for k, v in MOVIMIENTOS_CHAMPIONS.items()
        if not tipo or v["tipo"] == tipo.lower()
    ]
    return APIResponse(
        cerebro="champions", version=_VERSION, ok=True,
        data={"total": len(resultado), "tipo_filtro": tipo, "movimientos": resultado},
    )


@router.get("/health", response_model=APIResponse)
def health() -> APIResponse:
    return APIResponse(
        cerebro="champions", version=_VERSION, ok=True,
        data={
            "status": "operativo",
            "formato": "Singles",
            "generaciones": "I–IX",
            "total_pokemon": len(POKEMON_CHAMPIONS),
            "total_movimientos": len(MOVIMIENTOS_CHAMPIONS),
            "formula_dano": "Gen IX estándar (16 rolls, 85–100 %)",
            "tabla_tipos": "×2.0 / ×0.5 / ×0.0 (main series estándar)",
            "mecanicas_excluidas": ["Tera", "Dynamax", "Z-Moves"],
            "nota_mega": "Pokemon Champions incluye ~60 Megas (Mega-Lucario, Mega-Charizard X/Y, etc.). Catalogo backend expandido a ~205 Pokemon base + ~64 Megas via WikiDex. Megas canonicas Gen VI/VII usan stats oficiales; Megas exclusivas Champions llevan flag `mega_speculado=True`.",
            "endpoints": ["/champions/dano", "/champions/guia-pokemon",
                          "/champions/mejor-equipo", "/champions/catalogo",
                          "/champions/movimientos"],
        },
    )
