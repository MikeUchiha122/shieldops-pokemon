"""
cerebros/go/api/router.py
Router FastAPI del Cerebro C — Pokémon GO (Tap Battle System).
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from core.types import APIResponse
from cerebros.go.models.schemas import (
    PeticionDanoGO, PeticionCPGO, ResultadoCPGO, EquipoGO, LigaGO, CP_CAPS,
)
from cerebros.go.engine.damage import calcular_dano, calcular_cp, nivel_optimo_para_liga

router = APIRouter(prefix="/go", tags=["Cerebro C — Pokémon GO"])
_VERSION = "1.0.0"


@router.post("/dano", response_model=APIResponse,
             summary="Calcula daño en GO (STAB x1.2, SE x1.6, inmune x0.391)")
def endpoint_dano(req: PeticionDanoGO) -> APIResponse:
    try:
        resultado = calcular_dano(req)
        return APIResponse(cerebro="go", version=_VERSION, ok=True,
                           data=resultado.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=str(exc))


@router.post("/cp", response_model=APIResponse,
             summary="Calcula el CP de un Pokémon GO y nivel óptimo para una liga")
def endpoint_cp(req: PeticionCPGO) -> APIResponse:
    try:
        cp_actual = calcular_cp(
            req.stats_base.ataque, req.stats_base.defensa, req.stats_base.hp,
            req.ivs.ataque, req.ivs.defensa, req.ivs.hp,
            req.nivel,
        )
        cap = CP_CAPS[req.liga]
        nivel_opt, cp_en_cap = (req.nivel, cp_actual) if cap is None else \
            nivel_optimo_para_liga(
                req.stats_base.ataque, req.stats_base.defensa, req.stats_base.hp,
                req.ivs.ataque, req.ivs.defensa, req.ivs.hp,
                cap,
            )
        resultado = ResultadoCPGO(
            cp=cp_actual,
            nivel_optimo=nivel_opt,
            cp_en_cap=cp_en_cap if cap else None,
            dentro_del_cap=(cap is None or cp_actual <= cap),
        )
        return APIResponse(cerebro="go", version=_VERSION, ok=True,
                           data=resultado.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=str(exc))


@router.post("/validar-equipo", response_model=APIResponse,
             summary="Valida equipo GO (CP caps, escudos, moveset)")
def endpoint_validar_equipo(equipo: EquipoGO) -> APIResponse:
    import math
    from cerebros.go.models.schemas import obtener_cpm
    errores: list[str] = []
    cap = CP_CAPS[equipo.liga]

    for p in equipo.miembros:
        if cap is not None:
            cpm = obtener_cpm(p.nivel)
            atq = (p.stats_base.ataque + p.ivs.ataque) * cpm
            df  = (p.stats_base.defensa + p.ivs.defensa) * cpm
            hp  = (p.stats_base.hp + p.ivs.hp) * cpm
            cp  = max(10, math.floor(atq * math.sqrt(df) * math.sqrt(hp) / 10))
            if cp > cap:
                errores.append(
                    f"{p.nombre}: CP {cp} excede el cap de {cap} para {equipo.liga}."
                )
        if equipo.escudos < 0 or equipo.escudos > 2:
            errores.append("Escudos deben ser 0, 1 o 2.")

    nombres = [p.nombre.lower() for p in equipo.miembros]
    if len(nombres) != len(set(nombres)):
        errores.append("El equipo tiene Pokémon duplicados.")

    return APIResponse(cerebro="go", version=_VERSION, ok=len(errores) == 0,
                       data={"equipo": equipo.nombre, "liga": equipo.liga,
                             "miembros": len(equipo.miembros)},
                       errores=errores)


@router.get("/health", response_model=APIResponse)
def health() -> APIResponse:
    return APIResponse(cerebro="go", version=_VERSION, ok=True,
                       data={"status": "operativo",
                             "motor": "GO Battle League Tap System",
                             "stab": 1.2, "super_eficaz": 1.6,
                             "inmune": 0.391, "shadow_atk": 1.2})
