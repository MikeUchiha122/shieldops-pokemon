"""
cerebros/lza/models/schemas.py
Modelos de datos para el Cerebro B — Leyendas Z-A (Action Time PvP).

Reglas LZA:
- NO hay turnos: sistema de accion en tiempo real con Startup Frames y Cooldowns.
- Habilidades DESACTIVADAS. Inmunidades solo por tipo elemental base.
- Maximo 3 switches por combate.
- Paralisis: cooldowns x1.5. Quemadura: dano fisico x0.5.
- Equipos de 3 Pokemon. 1 Mega Evolucion por combate.
- STAB x1.5 sin Adaptable ni Teracristalizacion.
"""
from __future__ import annotations
from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, model_validator
from core.types import TipoElemental


class EstadoAlteradoLZA(StrEnum):
    NINGUNO    = "ninguno"
    PARALIZADO = "paralizado"
    QUEMADO    = "quemado"
    ENVENENADO = "envenenado"
    DORMIDO    = "dormido"
    CONGELADO  = "congelado"


class CategoriaMovimientoLZA(StrEnum):
    RAPIDO   = "rapido"
    CARGADO  = "cargado"
    AOE      = "aoe"
    ESTADO   = "estado"


class MovimientoLZA(BaseModel):
    nombre:           str                    = Field(min_length=1, max_length=64)
    tipo:             TipoElemental
    categoria:        CategoriaMovimientoLZA
    potencia:         int | None             = Field(default=None, ge=0, le=300)
    startup_frames:   int                    = Field(ge=1, le=120)
    cooldown_ms:      int                    = Field(ge=0, le=5000)
    alcance:          str                    = Field(default="cuerpo_a_cuerpo",
                                                     pattern=r"^[a-z_]+$")
    prioridad_accion: int                    = Field(default=0, ge=-3, le=3)

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()


class StatsBaseLZA(BaseModel):
    hp:      Annotated[int, Field(ge=1, le=255)]
    ataque:  Annotated[int, Field(ge=1, le=255)]
    defensa: Annotated[int, Field(ge=1, le=255)]
    vel:     Annotated[int, Field(ge=1, le=255)]


class PokemonLZA(BaseModel):
    nombre:       str                 = Field(min_length=1, max_length=64)
    tipos:        list[TipoElemental] = Field(min_length=1, max_length=2)
    stats:        StatsBaseLZA
    movimientos:  list[MovimientoLZA] = Field(min_length=1, max_length=4)
    estado:       EstadoAlteradoLZA   = EstadoAlteradoLZA.NINGUNO
    hp_actual:    int | None          = None
    puede_mega:   bool                = False
    tipos_mega:   list[TipoElemental] = Field(default_factory=list, max_length=2)
    stats_mega:   StatsBaseLZA | None = None
    mega_activa:  bool                = False

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()

    @model_validator(mode="after")
    def validar_hp_y_mega(self) -> "PokemonLZA":
        if self.hp_actual is not None:
            if self.hp_actual < 0:
                raise ValueError("hp_actual no puede ser negativo")
            if self.hp_actual > self.stats.hp:
                raise ValueError(f"hp_actual {self.hp_actual} > hp max {self.stats.hp}")
        if self.mega_activa and not self.puede_mega:
            raise ValueError(f"{self.nombre} no puede Mega Evolucionar.")
        if self.mega_activa and not self.stats_mega:
            raise ValueError(f"{self.nombre}: mega_activa pero sin stats_mega.")
        return self

    @property
    def tipos_activos(self) -> list[TipoElemental]:
        if self.mega_activa and self.tipos_mega:
            return self.tipos_mega
        return self.tipos

    @property
    def stats_activos(self) -> StatsBaseLZA:
        if self.mega_activa and self.stats_mega:
            return self.stats_mega
        return self.stats


class EquipoLZA(BaseModel):
    nombre:          str              = Field(min_length=1, max_length=128)
    miembros:        list[PokemonLZA] = Field(min_length=1, max_length=3)
    switches_usados: int              = Field(default=0, ge=0, le=3)

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()

    @model_validator(mode="after")
    def max_una_mega(self) -> "EquipoLZA":
        if sum(1 for p in self.miembros if p.mega_activa) > 1:
            raise ValueError("Solo 1 Mega Evolucion activa por combate.")
        return self


class PeticionCalculoDanoLZA(BaseModel):
    atacante:             PokemonLZA
    defensor:             PokemonLZA
    movimiento:           MovimientoLZA
    defensor_esquivando:  bool = False
    quemadura_activa:     bool = False


class ResultadoDanoLZA(BaseModel):
    atacante:              str
    defensor:              str
    movimiento:            str
    dano:                  int
    dano_con_estado:       int
    porcentaje_hp:         float
    efectividad:           float
    stab_aplicado:         bool
    es_ohko:               bool
    cooldown_efectivo_ms:  int
    puede_esquivar:        bool


class EventoCombateLZA(BaseModel):
    timestamp_ms: int  = Field(ge=0)
    actor:        str  = Field(min_length=1, max_length=64)
    accion:       str  = Field(min_length=1, max_length=64)
    movimiento:   str | None = None
    resultado:    str  = Field(default="pendiente")


class EstadoCombateLZA(BaseModel):
    equipo_a:     EquipoLZA
    equipo_b:     EquipoLZA
    activo_a:     int = Field(default=0, ge=0, le=2)
    activo_b:     int = Field(default=0, ge=0, le=2)
    switches_a:   int = Field(default=0, ge=0, le=3)
    switches_b:   int = Field(default=0, ge=0, le=3)
    mega_usada_a: bool = False
    mega_usada_b: bool = False
    turno_ms:     int = Field(default=0, ge=0)
    historial:    list[EventoCombateLZA] = Field(default_factory=list)

    @model_validator(mode="after")
    def switches_validos(self) -> "EstadoCombateLZA":
        if self.switches_a > 3:
            raise ValueError("Equipo A: limite de 3 switches superado.")
        if self.switches_b > 3:
            raise ValueError("Equipo B: limite de 3 switches superado.")
        return self
