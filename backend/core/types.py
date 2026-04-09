"""
core/types.py — Tipos compartidos entre los 3 cerebros.
NO contiene lógica de juego — solo contratos de datos y enumeraciones.
"""
from __future__ import annotations
from enum import StrEnum
from typing import Annotated, Final
from pydantic import BaseModel, Field

# ── Tipos elementales (los 18 de Gen IX / LZA / GO) ─────────────
class TipoElemental(StrEnum):
    NORMAL    = "normal"
    FUEGO     = "fuego"
    AGUA      = "agua"
    ELECTRICO = "electrico"
    PLANTA    = "planta"
    HIELO     = "hielo"
    LUCHA     = "lucha"
    VENENO    = "veneno"
    TIERRA    = "tierra"
    VOLADOR   = "volador"
    PSIQUICO  = "psiquico"
    BICHO     = "bicho"
    ROCA      = "roca"
    FANTASMA  = "fantasma"
    DRAGON    = "dragon"
    SINIESTRO = "siniestro"
    ACERO     = "acero"
    HADA      = "hada"

# ── Tabla de efectividades (relaciones base — idénticas en los 3 juegos) ──
# Valor: 2=supereficaz, 0.5=poco eficaz, 0=sin efecto/inmune, 1=normal (omitido)
TABLA_EFECTIVIDAD: Final[dict[TipoElemental, dict[TipoElemental, float]]] = {
    TipoElemental.NORMAL:    {TipoElemental.ROCA: 0.5, TipoElemental.ACERO: 0.5,
                               TipoElemental.FANTASMA: 0.0},
    TipoElemental.FUEGO:     {TipoElemental.FUEGO: 0.5, TipoElemental.AGUA: 0.5,
                               TipoElemental.ROCA: 0.5, TipoElemental.DRAGON: 0.5,
                               TipoElemental.PLANTA: 2.0, TipoElemental.HIELO: 2.0,
                               TipoElemental.BICHO: 2.0, TipoElemental.ACERO: 2.0},
    TipoElemental.AGUA:      {TipoElemental.FUEGO: 2.0, TipoElemental.TIERRA: 2.0,
                               TipoElemental.ROCA: 2.0, TipoElemental.AGUA: 0.5,
                               TipoElemental.PLANTA: 0.5, TipoElemental.DRAGON: 0.5},
    TipoElemental.ELECTRICO: {TipoElemental.AGUA: 2.0, TipoElemental.VOLADOR: 2.0,
                               TipoElemental.TIERRA: 0.0, TipoElemental.ELECTRICO: 0.5,
                               TipoElemental.PLANTA: 0.5, TipoElemental.DRAGON: 0.5},
    TipoElemental.PLANTA:    {TipoElemental.AGUA: 2.0, TipoElemental.TIERRA: 2.0,
                               TipoElemental.ROCA: 2.0, TipoElemental.FUEGO: 0.5,
                               TipoElemental.PLANTA: 0.5, TipoElemental.VENENO: 0.5,
                               TipoElemental.VOLADOR: 0.5, TipoElemental.BICHO: 0.5,
                               TipoElemental.DRAGON: 0.5, TipoElemental.ACERO: 0.5},
    TipoElemental.HIELO:     {TipoElemental.PLANTA: 2.0, TipoElemental.TIERRA: 2.0,
                               TipoElemental.VOLADOR: 2.0, TipoElemental.DRAGON: 2.0,
                               TipoElemental.FUEGO: 0.5, TipoElemental.AGUA: 0.5,
                               TipoElemental.HIELO: 0.5, TipoElemental.ACERO: 0.5},
    TipoElemental.LUCHA:     {TipoElemental.NORMAL: 2.0, TipoElemental.HIELO: 2.0,
                               TipoElemental.ROCA: 2.0, TipoElemental.SINIESTRO: 2.0,
                               TipoElemental.ACERO: 2.0, TipoElemental.VENENO: 0.5,
                               TipoElemental.BICHO: 0.5, TipoElemental.PSIQUICO: 0.5,
                               TipoElemental.VOLADOR: 0.5, TipoElemental.HADA: 0.5,
                               TipoElemental.FANTASMA: 0.0},
    TipoElemental.VENENO:    {TipoElemental.PLANTA: 2.0, TipoElemental.HADA: 2.0,
                               TipoElemental.VENENO: 0.5, TipoElemental.TIERRA: 0.5,
                               TipoElemental.ROCA: 0.5, TipoElemental.FANTASMA: 0.5,
                               TipoElemental.ACERO: 0.0},
    TipoElemental.TIERRA:    {TipoElemental.FUEGO: 2.0, TipoElemental.ELECTRICO: 2.0,
                               TipoElemental.VENENO: 2.0, TipoElemental.ROCA: 2.0,
                               TipoElemental.ACERO: 2.0, TipoElemental.PLANTA: 0.5,
                               TipoElemental.BICHO: 0.5, TipoElemental.VOLADOR: 0.0},
    TipoElemental.VOLADOR:   {TipoElemental.PLANTA: 2.0, TipoElemental.LUCHA: 2.0,
                               TipoElemental.BICHO: 2.0, TipoElemental.ELECTRICO: 0.5,
                               TipoElemental.ROCA: 0.5, TipoElemental.ACERO: 0.5},
    TipoElemental.PSIQUICO:  {TipoElemental.LUCHA: 2.0, TipoElemental.VENENO: 2.0,
                               TipoElemental.PSIQUICO: 0.5, TipoElemental.ACERO: 0.5,
                               TipoElemental.SINIESTRO: 0.0},
    TipoElemental.BICHO:     {TipoElemental.PLANTA: 2.0, TipoElemental.PSIQUICO: 2.0,
                               TipoElemental.SINIESTRO: 2.0, TipoElemental.FUEGO: 0.5,
                               TipoElemental.LUCHA: 0.5, TipoElemental.VOLADOR: 0.5,
                               TipoElemental.FANTASMA: 0.5, TipoElemental.ACERO: 0.5,
                               TipoElemental.HADA: 0.5},
    TipoElemental.ROCA:      {TipoElemental.FUEGO: 2.0, TipoElemental.HIELO: 2.0,
                               TipoElemental.VOLADOR: 2.0, TipoElemental.BICHO: 2.0,
                               TipoElemental.LUCHA: 0.5, TipoElemental.TIERRA: 0.5,
                               TipoElemental.ACERO: 0.5},
    TipoElemental.FANTASMA:  {TipoElemental.PSIQUICO: 2.0, TipoElemental.FANTASMA: 2.0,
                               TipoElemental.NORMAL: 0.0, TipoElemental.SINIESTRO: 0.5},
    TipoElemental.DRAGON:    {TipoElemental.DRAGON: 2.0, TipoElemental.ACERO: 0.5,
                               TipoElemental.HADA: 0.0},
    TipoElemental.SINIESTRO: {TipoElemental.PSIQUICO: 2.0, TipoElemental.FANTASMA: 2.0,
                               TipoElemental.LUCHA: 0.5, TipoElemental.SINIESTRO: 0.5,
                               TipoElemental.HADA: 0.5},
    TipoElemental.ACERO:     {TipoElemental.HIELO: 2.0, TipoElemental.ROCA: 2.0,
                               TipoElemental.HADA: 2.0, TipoElemental.FUEGO: 0.5,
                               TipoElemental.AGUA: 0.5, TipoElemental.ELECTRICO: 0.5,
                               TipoElemental.ACERO: 0.5},
    TipoElemental.HADA:      {TipoElemental.LUCHA: 2.0, TipoElemental.DRAGON: 2.0,
                               TipoElemental.SINIESTRO: 2.0, TipoElemental.FUEGO: 0.5,
                               TipoElemental.VENENO: 0.5, TipoElemental.ACERO: 0.5},
}


def efectividad_base(ataque: TipoElemental, defensor: TipoElemental) -> float:
    """Retorna el multiplicador base sin aplicar reglas de juego específicas."""
    return TABLA_EFECTIVIDAD.get(ataque, {}).get(defensor, 1.0)


# ── Respuesta estándar de la API ─────────────────────────────────
class APIResponse(BaseModel):
    """Envuelve todas las respuestas de los 3 cerebros."""
    cerebro: str          # "eyp" | "lza" | "go"
    version: str          # versión del motor
    ok: bool
    data: dict            # payload específico del cerebro
    errores: list[str] = []
