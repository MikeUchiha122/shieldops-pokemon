"""
main.py — Punto de entrada de ShieldOps Backend.

Monta los 3 cerebros como routers independientes bajo /api/v1/.
Cada cerebro tiene su propio prefijo y no comparte estado con los otros.

Endpoints disponibles:
  GET  /api/v1/health           → Estado de los 3 cerebros
  POST /api/v1/eyp/dano         → Motor daño EyP (Gen IX, 16 rolls)
  POST /api/v1/eyp/validar-equipo
  POST /api/v1/lza/dano         → Motor daño LZA (Action Time, sin habilidades)
  POST /api/v1/lza/validar-combate
  POST /api/v1/go/dano          → Motor daño GO (STAB x1.2, inmune x0.391)
  POST /api/v1/go/cp            → Calcula CP y nivel óptimo por liga
  POST /api/v1/go/validar-equipo
"""
from __future__ import annotations
import sys
import os

# Hacer que los módulos se importen desde la raíz del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.types import APIResponse
from cerebros.eyp.api.router import router as eyp_router
from cerebros.lza.api.router import router as lza_router
from cerebros.go.api.router  import router as go_router

app = FastAPI(
    title="ShieldOps Backend — 3 Cerebros Pokémon",
    description=(
        "Motor de cálculo competitivo para Escarlata/Púrpura (VGC), "
        "Leyendas Z-A (Action Time PvP) y Pokémon GO (GO Battle League)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — ajustar origins en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://MikeUchiha122.github.io", "https://thriving-tranquility-production.up.railway.app", "https://railway.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Montar los 3 cerebros como routers independientes
API_V1 = "/api/v1"
app.include_router(eyp_router, prefix=API_V1)
app.include_router(lza_router, prefix=API_V1)
app.include_router(go_router,  prefix=API_V1)


@app.get("/", tags=["Sistema"])
async def root() -> dict:
    return {"message": "ShieldOps Backend", "version": "1.0.0", "endpoints": ["/api/v1/health", "/docs"]}

@app.get(f"{API_V1}/health", response_model=dict, tags=["Sistema"])
async def health_global() -> dict:
    """Estado global — consulta los 3 cerebros."""
    return {
        "sistema": "ShieldOps Backend",
        "version": "1.0.0",
        "cerebros": {
            "eyp": {"nombre": "Escarlata/Púrpura VGC", "ruta": f"{API_V1}/eyp"},
            "lza": {"nombre": "Leyendas Z-A Action PvP", "ruta": f"{API_V1}/lza"},
            "go":  {"nombre": "Pokémon GO Battle League", "ruta": f"{API_V1}/go"},
        },
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
