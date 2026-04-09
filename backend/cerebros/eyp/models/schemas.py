"""
cerebros/eyp/models/schemas.py
Modelos de datos para el Cerebro A: Escarlata/Púrpura (VGC / Singles Clásico).

Reglas del motor EyP:
- Turnos estrictos. Equipos de 6, se llevan 4 al campo.
- Habilidades ACTIVAS (Levitación, Rompemoldes, etc.).
- Teracristalización disponible (1 vez por combate).
- STAB: ×1.5. Super eficaz: ×2.0. Poco eficaz: ×0.5. Inmune: ×0.
- IVs: 0-31. EVs: 0-252 por stat, 510 total. Nivel 50 fijo.
- Adaptable: STAB ×2.0. Sin teratype, STAB normal.
"""
from __future__ import annotations
from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, model_validator


class NaturalezaEyP(StrEnum):
    TIMIDO   = "timido"    # +Vel -AtqFis
    MODESTO  = "modesto"   # +AtqEsp -AtqFis
    RELAJADO = "relajado"  # +Def -Vel
    FIRME    = "firme"     # +AtqFis -AtqEsp
    OSADO    = "osado"     # +AtqFis -Vel
    AFABLE   = "afable"    # +AtqFis -AtqEsp (alias)
    AGITADO  = "agitado"   # +Vel -AtqEsp
    CAUTO    = "cauto"     # +AtqEsp -Vel
    SERENO   = "sereno"    # +AtqEsp -AtqFis
    ACTIVO   = "activo"    # +Vel -Def
    ALEGRE   = "alegre"    # +Vel -DefEsp
    MIEDOSO  = "miedoso"   # +Vel -AtqFis
    AUDAZ    = "audaz"     # +AtqFis -Def
    PLACIDO  = "placido"   # +Def -AtqEsp
    MANSO    = "manso"     # +DefEsp -AtqFis
    GENTIL   = "gentil"    # +DefEsp -AtqFis
    CALMADO  = "calmado"   # +DefEsp -Vel
    GROSERO  = "grosero"   # +AtqFis -DefEsp
    FLOJO    = "flojo"     # +Def -Vel
    SERIO    = "serio"     # sin bonus


MODIFICADORES_NATURALEZA: dict[NaturalezaEyP, tuple[str, str | None]] = {
    NaturalezaEyP.TIMIDO:   ("vel",    "atq_fis"),
    NaturalezaEyP.MODESTO:  ("atq_esp","atq_fis"),
    NaturalezaEyP.RELAJADO: ("def",    "vel"),
    NaturalezaEyP.FIRME:    ("atq_fis","atq_esp"),
    NaturalezaEyP.OSADO:    ("atq_fis","vel"),
    NaturalezaEyP.AGITADO:  ("vel",    "atq_esp"),
    NaturalezaEyP.CAUTO:    ("atq_esp","vel"),
    NaturalezaEyP.SERENO:   ("atq_esp","atq_fis"),
    NaturalezaEyP.ACTIVO:   ("vel",    "def"),
    NaturalezaEyP.ALEGRE:   ("vel",    "def_esp"),
    NaturalezaEyP.MIEDOSO:  ("vel",    "atq_fis"),
    NaturalezaEyP.AUDAZ:    ("atq_fis","def"),
    NaturalezaEyP.PLACIDO:  ("def",    "atq_esp"),
    NaturalezaEyP.MANSO:    ("def_esp","atq_fis"),
    NaturalezaEyP.GENTIL:   ("def_esp","atq_fis"),
    NaturalezaEyP.CALMADO:  ("def_esp","vel"),
    NaturalezaEyP.GROSERO:  ("atq_fis","def_esp"),
    NaturalezaEyP.FLOJO:    ("def",    "vel"),
    NaturalezaEyP.SERIO:    ("",       None),
    NaturalezaEyP.AFABLE:   ("atq_fis","atq_esp"),
}


class CategoriaMovimiento(StrEnum):
    FISICO   = "fisico"
    ESPECIAL = "especial"
    ESTADO   = "estado"


from core.types import TipoElemental

# EVs: 0–252 por stat
EV = Annotated[int, Field(ge=0, le=252)]
# IVs: 0–31
IV = Annotated[int, Field(ge=0, le=31)]
# Boosts de combate: -6 a +6
Boost = Annotated[int, Field(ge=-6, le=6)]


class EVsEyP(BaseModel):
    hp:      EV = 0
    atq_fis: EV = 0
    def_fis: EV = 0
    atq_esp: EV = 0
    def_esp: EV = 0
    vel:     EV = 0

    @model_validator(mode="after")
    def total_max_510(self) -> "EVsEyP":
        total = self.hp + self.atq_fis + self.def_fis + self.atq_esp + self.def_esp + self.vel
        if total > 510:
            raise ValueError(f"EVs totales {total} superan el máximo de 510")
        return self


class IVsEyP(BaseModel):
    hp:      IV = 31
    atq_fis: IV = 31
    def_fis: IV = 31
    atq_esp: IV = 31
    def_esp: IV = 31
    vel:     IV = 31


class MovimientoEyP(BaseModel):
    nombre:    str            = Field(min_length=1, max_length=64)
    tipo:      TipoElemental
    categoria: CategoriaMovimiento
    potencia:  int | None     = Field(default=None, ge=0, le=300)
    precision: int | None     = Field(default=None, ge=1, le=101)
    pp:        int            = Field(ge=1, le=64)
    prioridad: int            = Field(default=0, ge=-7, le=5)

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido en nombre: {c!r}")
        return v.strip()


class PokemonEyP(BaseModel):
    nombre:      str              = Field(min_length=1, max_length=64)
    tipos:       list[TipoElemental] = Field(min_length=1, max_length=2)
    habilidad:   str              = Field(min_length=1, max_length=64)
    item:        str | None       = Field(default=None, max_length=64)
    naturaleza:  NaturalezaEyP
    nivel:       int              = Field(default=50, ge=1, le=100)
    stats_base:  dict[str, int]   = Field(
        description="hp, atq_fis, def_fis, atq_esp, def_esp, vel"
    )
    evs:         EVsEyP           = EVsEyP()
    ivs:         IVsEyP           = IVsEyP()
    movimientos: list[MovimientoEyP] = Field(min_length=1, max_length=4)
    # Teracristalización
    teratipo:    TipoElemental | None = None
    teraactivada: bool            = False

    @field_validator("nombre", "habilidad")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()

    @model_validator(mode="after")
    def stats_base_completos(self) -> "PokemonEyP":
        required = {"hp", "atq_fis", "def_fis", "atq_esp", "def_esp", "vel"}
        missing = required - set(self.stats_base.keys())
        if missing:
            raise ValueError(f"Stats base faltantes: {missing}")
        for stat, val in self.stats_base.items():
            if not (1 <= val <= 255):
                raise ValueError(f"Stat base '{stat}' = {val} fuera de rango (1-255)")
        return self


class EquipoEyP(BaseModel):
    nombre:   str             = Field(min_length=1, max_length=128)
    formato:  str             = Field(default="vgc2026", pattern=r"^[a-z0-9_]+$")
    miembros: list[PokemonEyP] = Field(min_length=1, max_length=6)

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()


class PeticionCalculoDanoEyP(BaseModel):
    atacante:     PokemonEyP
    defensor:     PokemonEyP
    movimiento:   MovimientoEyP
    boost_atq:    Boost = 0
    boost_def:    Boost = 0
    boost_vel:    Boost = 0
    terreno_activo: str | None = None  # "electrico"|"psiquico"|"hierba"|"niebla"
    clima_activo:   str | None = None  # "sol"|"lluvia"|"granizo"|"tormenta_arena"
    pantallas:    bool = False         # Pantalla de Luz / Reflejo activo
    critico:      bool = False
    n_rolls:      int  = Field(default=16, ge=1, le=16)


class ResultadoDanoEyP(BaseModel):
    atacante:    str
    defensor:    str
    movimiento:  str
    dano_minimo: int
    dano_maximo: int
    porcentaje_min: float
    porcentaje_max: float
    hp_defensor: int
    es_ohko:     bool
    es_2hko:     bool
    stab_aplicado: bool
    tera_aplicado: bool
    efectividad:  float
    rolls:        list[int]
