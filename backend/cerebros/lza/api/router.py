"""
cerebros/lza/api/router.py
Router FastAPI del Cerebro B — Leyendas Z-A (Action Time PvP).
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from core.types import APIResponse
from cerebros.lza.models.schemas import (
    PeticionCalculoDanoLZA, EstadoCombateLZA, EquipoLZA,
)
from cerebros.lza.engine.damage import calcular_dano

router = APIRouter(prefix="/lza", tags=["Cerebro B — LZA Action PvP"])
_VERSION = "1.0.0"


@router.post("/dano", response_model=APIResponse,
             summary="Calcula daño en tiempo real (LZA, sin habilidades)")
def endpoint_dano(req: PeticionCalculoDanoLZA) -> APIResponse:
    try:
        resultado = calcular_dano(req)
        return APIResponse(cerebro="lza", version=_VERSION, ok=True,
                           data=resultado.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=str(exc))


@router.post("/validar-combate", response_model=APIResponse,
             summary="Valida estado de combate LZA (switches, mega, etc.)")
def endpoint_validar_combate(estado: EstadoCombateLZA) -> APIResponse:
    errores: list[str] = []
    if estado.switches_a > 3:
        errores.append(f"Equipo A: {estado.switches_a} switches > limite 3.")
    if estado.switches_b > 3:
        errores.append(f"Equipo B: {estado.switches_b} switches > limite 3.")
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


@router.get("/health", response_model=APIResponse)
def health() -> APIResponse:
    return APIResponse(cerebro="lza", version=_VERSION, ok=True,
                       data={"status": "operativo",
                             "motor": "LZA Action Time PvP",
                             "habilidades": "desactivadas",
                             "max_switches": 3})
