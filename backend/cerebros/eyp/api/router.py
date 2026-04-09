"""
cerebros/eyp/api/router.py
Router FastAPI del Cerebro A — Escarlata/Púrpura (VGC / Singles Clásico).
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from core.types import APIResponse
from cerebros.eyp.models.schemas import PeticionCalculoDanoEyP, EquipoEyP
from cerebros.eyp.engine.damage import calcular_dano

router = APIRouter(prefix="/eyp", tags=["Cerebro A — EyP VGC"])
_VERSION = "1.0.0"


@router.post("/dano", response_model=APIResponse,
             summary="Calcula daño entre dos Pokémon (Gen IX, 16 rolls)")
def endpoint_dano(req: PeticionCalculoDanoEyP) -> APIResponse:
    try:
        resultado = calcular_dano(req)
        return APIResponse(cerebro="eyp", version=_VERSION, ok=True,
                           data=resultado.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=str(exc))


@router.post("/validar-equipo", response_model=APIResponse,
             summary="Valida un equipo VGC 2026")
def endpoint_validar_equipo(equipo: EquipoEyP) -> APIResponse:
    errores: list[str] = []
    nombres = [p.nombre.lower() for p in equipo.miembros]
    if len(nombres) != len(set(nombres)):
        errores.append("El equipo tiene Pokémon duplicados.")
    for p in equipo.miembros:
        total_ev = (p.evs.hp + p.evs.atq_fis + p.evs.def_fis
                    + p.evs.atq_esp + p.evs.def_esp + p.evs.vel)
        if total_ev > 510:
            errores.append(f"{p.nombre}: EVs totales {total_ev} > 510.")
    return APIResponse(cerebro="eyp", version=_VERSION, ok=len(errores) == 0,
                       data={"equipo": equipo.nombre, "miembros": len(equipo.miembros)},
                       errores=errores)


@router.get("/health", response_model=APIResponse)
def health() -> APIResponse:
    return APIResponse(cerebro="eyp", version=_VERSION, ok=True,
                       data={"status": "operativo", "motor": "Gen IX VGC 2026"})
