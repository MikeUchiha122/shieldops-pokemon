"""
cerebros/champions/models/schemas.py
Esquemas Pydantic para Pokémon Champions (Singles multi-generacional).
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class NaturalezaChampions(str, Enum):
    # +Ataque
    solitario  = "solitario"
    malo       = "malo"
    audaz      = "audaz"
    picaresco  = "picaresco"
    ingenuo    = "ingenuo"
    # +Defensa
    imprudente = "imprudente"
    relajado   = "relajado"
    sosegado   = "sosegado"
    descuidado = "descuidado"
    flojo      = "flojo"
    # +Atq Especial
    modesto    = "modesto"
    discreto   = "discreto"
    manso      = "manso"
    agitado    = "agitado"
    timido_atk = "timido_atkesp"
    # +Def Especial
    calmo      = "calmo"
    suave      = "suave"
    cauto      = "cauto"
    amable     = "amable"
    alocado    = "alocado"
    # +Velocidad
    timido     = "timido"
    apresurado = "apresurado"
    alegre     = "alegre"
    ingenioso  = "ingenioso"
    jupiterino = "jupiterino"
    # Neutral
    serio      = "serio"


NATURALEZA_MODIFICADORES: dict[str, dict[str, float]] = {
    "solitario":   {"ataque": 1.1, "defensa": 0.9},
    "malo":        {"ataque": 1.1, "defensa_especial": 0.9},
    "audaz":       {"ataque": 1.1, "velocidad": 0.9},
    "picaresco":   {"ataque": 1.1, "ataque_especial": 0.9},
    "ingenuo":     {"ataque": 1.1, "defensa_especial": 0.9},
    "imprudente":  {"defensa": 1.1, "ataque": 0.9},
    "relajado":    {"defensa": 1.1, "velocidad": 0.9},
    "sosegado":    {"defensa": 1.1, "ataque_especial": 0.9},
    "descuidado":  {"defensa": 1.1, "defensa_especial": 0.9},
    "flojo":       {"defensa": 1.1, "ataque_especial": 0.9},
    "modesto":     {"ataque_especial": 1.1, "ataque": 0.9},
    "discreto":    {"ataque_especial": 1.1, "defensa": 0.9},
    "manso":       {"ataque_especial": 1.1, "velocidad": 0.9},
    "agitado":     {"ataque_especial": 1.1, "defensa_especial": 0.9},
    "timido_atkesp": {"ataque_especial": 1.1, "ataque": 0.9},
    "calmo":       {"defensa_especial": 1.1, "ataque": 0.9},
    "suave":       {"defensa_especial": 1.1, "defensa": 0.9},
    "cauto":       {"defensa_especial": 1.1, "velocidad": 0.9},
    "amable":      {"defensa_especial": 1.1, "ataque_especial": 0.9},
    "alocado":     {"defensa_especial": 1.1, "ataque": 0.9},
    "timido":      {"velocidad": 1.1, "ataque": 0.9},
    "apresurado":  {"velocidad": 1.1, "defensa": 0.9},
    "alegre":      {"velocidad": 1.1, "ataque_especial": 0.9},
    "ingenioso":   {"velocidad": 1.1, "defensa_especial": 0.9},
    "jupiterino":  {"velocidad": 1.1, "ataque": 0.9},
    "serio":       {},
}


class StatsBaseChampions(BaseModel):
    hp: int = Field(ge=1, le=255)
    ataque: int = Field(ge=1, le=255)
    defensa: int = Field(ge=1, le=255)
    ataque_especial: int = Field(ge=1, le=255)
    defensa_especial: int = Field(ge=1, le=255)
    velocidad: int = Field(ge=1, le=255)


class EVsChampions(BaseModel):
    hp: int = Field(default=0, ge=0, le=252)
    ataque: int = Field(default=0, ge=0, le=252)
    defensa: int = Field(default=0, ge=0, le=252)
    ataque_especial: int = Field(default=0, ge=0, le=252)
    defensa_especial: int = Field(default=0, ge=0, le=252)
    velocidad: int = Field(default=0, ge=0, le=252)

    def total(self) -> int:
        return (self.hp + self.ataque + self.defensa +
                self.ataque_especial + self.defensa_especial + self.velocidad)


class IVsChampions(BaseModel):
    hp: int = Field(default=31, ge=0, le=31)
    ataque: int = Field(default=31, ge=0, le=31)
    defensa: int = Field(default=31, ge=0, le=31)
    ataque_especial: int = Field(default=31, ge=0, le=31)
    defensa_especial: int = Field(default=31, ge=0, le=31)
    velocidad: int = Field(default=31, ge=0, le=31)


class PokemonChampions(BaseModel):
    nombre: str = Field(min_length=1, max_length=64)
    tipos: list[str] = Field(min_length=1, max_length=2)
    stats_base: StatsBaseChampions
    evs: EVsChampions = Field(default_factory=EVsChampions)
    ivs: IVsChampions = Field(default_factory=IVsChampions)
    naturaleza: NaturalezaChampions = NaturalezaChampions.serio
    nivel: int = Field(default=50, ge=1, le=100)
    habilidad: Optional[str] = None
    objeto: Optional[str] = None
    movimientos: list[str] = Field(default_factory=list, max_length=4)


class MovimientoChampions(BaseModel):
    nombre: str
    tipo: str
    categoria: str
    potencia: Optional[int] = None
    precision: Optional[int] = None
    pp: int
    prioridad: int = 0


class PeticionDanoChampions(BaseModel):
    atacante: PokemonChampions
    defensor: PokemonChampions
    movimiento: str = Field(min_length=1, max_length=64)
    critico: bool = False
    clima: Optional[str] = None  # "sol", "lluvia", "granizo", "arena"
    boost_atacante: int = Field(default=0, ge=-6, le=6)
    boost_defensor: int = Field(default=0, ge=-6, le=6)


class ResultadoDanoChampions(BaseModel):
    dano_minimo: int
    dano_maximo: int
    dano_promedio: float
    porcentaje_min: float
    porcentaje_max: float
    porcentaje_promedio: float
    efectividad: float
    stab: bool
    critico: bool
    ko_garantizado: bool
    posible_2hko: bool
    detalle: str
