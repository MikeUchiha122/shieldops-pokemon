"""
cerebros/go/api/router.py
Router Cerebro C — Pokémon GO. Incluye cálculo de daño + guías GO Battle League.
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from core.types import APIResponse
from cerebros.go.models.schemas import (
    PeticionDanoGO, PeticionCPGO, ResultadoCPGO, EquipoGO, LigaGO, CP_CAPS,
)
from cerebros.go.engine.damage import calcular_dano, calcular_cp, nivel_optimo_para_liga
from cerebros.go.engine.guia import generar_guia_pokemon_go, generar_mejor_equipo_go
from cerebros.go.data.pokemon import listar_pokemon_go, pokemon_go_por_liga

router = APIRouter(prefix="/go", tags=["Cerebro C — Pokémon GO"])
_VERSION = "2.0.0"


class PeticionGuiaGO(BaseModel):
    pokemon: str = Field(min_length=1, max_length=64)
    liga: str = Field(default="great", pattern="^(great|ultra|master)$")

class PeticionEquipoGO(BaseModel):
    liga: str = Field(default="great", pattern="^(great|ultra|master)$")


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


@router.post("/guia-pokemon", response_model=APIResponse,
             summary="Genera guía GO Battle League con IVs óptimos y matchups")
def endpoint_guia_pokemon(req: PeticionGuiaGO) -> APIResponse:
    """
    El cerebro GO:
    1. Verifica Pokémon en catálogo GO (stats Niantic — diferente a serie principal)
    2. Calcula IVs óptimos para el CP cap de la liga
    3. Evalúa combos Fast Move + Charged Move(s) por DPS/TDO
    4. Simula matchups vs amenazas meta de la liga
    5. Retorna build con tabla de tipos GO (×1.6/×0.625/×0.391)
    """
    resultado = generar_guia_pokemon_go(req.pokemon, req.liga)
    if not resultado.get("ok"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=resultado.get("error"))
    return APIResponse(cerebro="go", version=_VERSION, ok=True, data=resultado)


@router.post("/mejor-equipo", response_model=APIResponse,
             summary="Genera equipo meta GO Battle League")
def endpoint_mejor_equipo(req: PeticionEquipoGO) -> APIResponse:
    resultado = generar_mejor_equipo_go(req.liga)
    return APIResponse(cerebro="go", version=_VERSION, ok=True, data=resultado)


@router.get("/catalogo", response_model=APIResponse,
            summary="Lista Pokémon disponibles en GO por liga")
def endpoint_catalogo(liga: str = "great") -> APIResponse:
    pokemon_liga = pokemon_go_por_liga(liga)
    return APIResponse(cerebro="go", version=_VERSION, ok=True, data={
        "liga": liga,
        "total": len(pokemon_liga),
        "pokemon": pokemon_liga,
    })


@router.get("/health", response_model=APIResponse)
def health() -> APIResponse:
    return APIResponse(cerebro="go", version=_VERSION, ok=True,
                       data={
                           "status": "operativo",
                           "motor": "GO Battle League Tap System",
                           "tabla_tipos_go": "×1.6 SE | ×0.625 NVE | ×0.391 inmune",
                           "stab": 1.2, "super_eficaz": 1.6, "poco_eficaz": 0.625,
                           "inmune_go": 0.391, "shadow_atk_bonus": 1.2,
                           "endpoints_guia": ["/go/guia-pokemon", "/go/mejor-equipo", "/go/catalogo"],
                       })
