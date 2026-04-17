"""
cerebros/lza/api/router.py
Router Cerebro B — Leyendas Z-A. Incluye cálculo Action Time + guías PvP.
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from core.types import APIResponse
from cerebros.lza.models.schemas import PeticionCalculoDanoLZA, EstadoCombateLZA
from cerebros.lza.engine.damage import calcular_dano
from cerebros.lza.engine.guia import generar_guia_pokemon_lza, generar_mejor_equipo_lza
from cerebros.lza.data.pokemon import listar_pokemon_lza, listar_con_mega_lza

router = APIRouter(prefix="/lza", tags=["Cerebro B — LZA Action PvP"])
_VERSION = "2.0.0"


class PeticionGuiaLZA(BaseModel):
    pokemon: str = Field(min_length=1, max_length=64)

class PeticionEquipoLZA(BaseModel):
    pokemon_ancla: str = Field(min_length=1, max_length=64)


@router.post("/dano", response_model=APIResponse,
             summary="Daño Action Time LZA (startup_frames, cooldown, sin habilidades)")
def endpoint_dano(req: PeticionCalculoDanoLZA) -> APIResponse:
    try:
        resultado = calcular_dano(req)
        return APIResponse(cerebro="lza", version=_VERSION, ok=True,
                           data=resultado.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))


@router.post("/validar-combate", response_model=APIResponse,
             summary="Valida estado de combate LZA")
def endpoint_validar_combate(estado: EstadoCombateLZA) -> APIResponse:
    errores: list[str] = []
    if estado.switches_a > 3:
        errores.append(f"Equipo A: {estado.switches_a} switches > límite 3.")
    if estado.switches_b > 3:
        errores.append(f"Equipo B: {estado.switches_b} switches > límite 3.")
    if estado.mega_usada_a:
        megas_a = sum(1 for p in estado.equipo_a.miembros if p.mega_activa)
        if megas_a > 1:
            errores.append("Equipo A: más de 1 Mega activa.")
    if estado.mega_usada_b:
        megas_b = sum(1 for p in estado.equipo_b.miembros if p.mega_activa)
        if megas_b > 1:
            errores.append("Equipo B: más de 1 Mega activa.")
    return APIResponse(cerebro="lza", version=_VERSION, ok=len(errores) == 0,
                       data={"turno_ms": estado.turno_ms,
                             "switches_a": estado.switches_a,
                             "switches_b": estado.switches_b},
                       errores=errores)


@router.post("/guia-pokemon", response_model=APIResponse,
             summary="Genera guía Action Time PvP con simulación interna")
def endpoint_guia_pokemon(req: PeticionGuiaLZA) -> APIResponse:
    """
    El cerebro LZA:
    1. Verifica Pokémon en catálogo Kalos/LZA
    2. Evalúa con/sin Mega, objetos LZA
    3. Simula vs amenazas meta con startup_frames y cooldowns reales
    4. Considera cambios de tipo por Mega → recalcula tabla de tipos
    """
    resultado = generar_guia_pokemon_lza(req.pokemon)
    if not resultado.get("ok"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=resultado.get("error"))
    return APIResponse(cerebro="lza", version=_VERSION, ok=True, data=resultado)


@router.post("/mejor-equipo", response_model=APIResponse,
             summary="Genera equipo de 3 para LZA")
def endpoint_mejor_equipo(req: PeticionEquipoLZA) -> APIResponse:
    resultado = generar_mejor_equipo_lza(req.pokemon_ancla)
    if not resultado.get("ok"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=resultado.get("error"))
    return APIResponse(cerebro="lza", version=_VERSION, ok=True, data=resultado)


@router.get("/catalogo", response_model=APIResponse,
            summary="Lista Pokémon disponibles en LZA")
def endpoint_catalogo() -> APIResponse:
    return APIResponse(cerebro="lza", version=_VERSION, ok=True, data={
        "total": len(listar_pokemon_lza()),
        "pokemon": listar_pokemon_lza(),
        "con_mega_evolucion": listar_con_mega_lza(),
    })


@router.get("/health", response_model=APIResponse)
def health() -> APIResponse:
    return APIResponse(cerebro="lza", version=_VERSION, ok=True, data={
        "status": "operativo",
        "motor": "LZA Action Time PvP — Kalos",
        "tabla_tipos": "×2.0 / ×0.5 / ×0.0 — habilidades DESACTIVADAS",
        "mega": "1 por combate — cambia tipos → tabla de tipos recalculada",
        "endpoints_guia": ["/lza/guia-pokemon", "/lza/mejor-equipo", "/lza/catalogo"],
    })
