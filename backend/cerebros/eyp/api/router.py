"""
cerebros/eyp/api/router.py
Router Cerebro A — Escarlata/Púrpura. Incluye cálculo de daño + guías competitivas.
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from core.types import APIResponse
from cerebros.eyp.models.schemas import PeticionCalculoDanoEyP, EquipoEyP
from cerebros.eyp.engine.damage import calcular_dano
from cerebros.eyp.engine.guia import generar_guia_pokemon_eyp, generar_mejor_equipo_eyp
from cerebros.eyp.data.pokemon import listar_pokemon_eyp, listar_restringidos_eyp

router = APIRouter(prefix="/eyp", tags=["Cerebro A — EyP VGC 2026"])
_VERSION = "2.0.0"


class PeticionGuiaEyP(BaseModel):
    pokemon: str = Field(min_length=1, max_length=64, description="Nombre del Pokémon")
    formato: str = Field(default="vgc2026", description="Formato competitivo")

class PeticionEquipoEyP(BaseModel):
    pokemon_ancla: str = Field(min_length=1, max_length=64)
    formato: str = Field(default="vgc2026")


@router.post("/dano", response_model=APIResponse,
             summary="Calcula daño entre dos Pokémon (Gen IX, 16 rolls)")
def endpoint_dano(req: PeticionCalculoDanoEyP) -> APIResponse:
    try:
        resultado = calcular_dano(req)
        return APIResponse(cerebro="eyp", version=_VERSION, ok=True,
                           data=resultado.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))


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


@router.post("/guia-pokemon", response_model=APIResponse,
             summary="Genera guía competitiva VGC con simulación de batallas internas")
def endpoint_guia_pokemon(req: PeticionGuiaEyP) -> APIResponse:
    """
    El cerebro EyP:
    1. Verifica que el Pokémon esté en el catálogo Paldea/DLC
    2. Genera candidatos (naturaleza × EVs × objeto × movimientos EyP)
    3. Simula batallas vs amenazas meta VGC 2026
    4. Retorna los 3 mejores builds con stats nivel 50 y análisis
    """
    resultado = generar_guia_pokemon_eyp(req.pokemon)
    if not resultado.get("ok"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=resultado.get("error"))
    return APIResponse(cerebro="eyp", version=_VERSION, ok=True, data=resultado)


@router.post("/mejor-equipo", response_model=APIResponse,
             summary="Genera el mejor equipo VGC alrededor de un Pokémon ancla")
def endpoint_mejor_equipo(req: PeticionEquipoEyP) -> APIResponse:
    resultado = generar_mejor_equipo_eyp(req.pokemon_ancla, req.formato)
    if not resultado.get("ok"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=resultado.get("error"))
    return APIResponse(cerebro="eyp", version=_VERSION, ok=True, data=resultado)


@router.get("/catalogo", response_model=APIResponse,
            summary="Lista todos los Pokémon disponibles en EyP")
def endpoint_catalogo() -> APIResponse:
    return APIResponse(cerebro="eyp", version=_VERSION, ok=True, data={
        "total": len(listar_pokemon_eyp()),
        "pokemon": listar_pokemon_eyp(),
        "restringidos_vgc": listar_restringidos_eyp(),
    })


@router.get("/health", response_model=APIResponse)
def health() -> APIResponse:
    return APIResponse(cerebro="eyp", version=_VERSION, ok=True, data={
        "status": "operativo",
        "motor": "Gen IX VGC 2026 — Reg G/H",
        "tabla_tipos": "×2.0 / ×0.5 / ×0.0 (serie principal)",
        "endpoints_guia": ["/eyp/guia-pokemon", "/eyp/mejor-equipo", "/eyp/catalogo"],
    })
