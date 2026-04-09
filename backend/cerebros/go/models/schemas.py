"""
cerebros/go/models/schemas.py
Modelos de datos para el Cerebro C — Pokémon GO (Tap Battle System).

Reglas del motor GO (completamente distintas de EyP y LZA):
- IVs: 0-15 (no 0-31). Sin EVs ni naturaleza.
- CP = floor(Atq_eff * sqrt(Def_eff) * sqrt(HP_eff) * CPM^2 / 10)
- STAB: x1.2 (no x1.5). Super eficaz: x1.6. Poco eficaz: x0.625. Inmune: x0.391.
- Shadow: Ataque x1.2, Defensa x0.833.
- Niveles 1-51 con tabla CPM (CP Multiplier) oficial de Niantic.
- Fast Moves generan energía; Charged Moves consumen energía.
- 2 escudos por combate. Usar escudo bloquea el Charged Move rival (1 HP).
- Sin habilidades ni teracristalización.
"""
from __future__ import annotations
from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, model_validator
from core.types import TipoElemental

# IVs GO: 0-15
IVGO = Annotated[int, Field(ge=0, le=15)]

# Nivel GO: 1-51 (medios niveles incluidos como x.5)
# Representamos como int*2 para cubrir medios niveles (20 = nivel 10, 21 = nivel 10.5)
NivelGO = Annotated[float, Field(ge=1.0, le=51.0, multiple_of=0.5)]

# Tabla CPM oficial Niantic (niveles 1 a 51, incluyendo x.5)
# Solo incluimos niveles completos para brevedad — en producción se cargaría de JSON
CPM_TABLE: dict[float, float] = {
    1.0: 0.09399414, 1.5: 0.13513743, 2.0: 0.16639787, 2.5: 0.19265091,
    3.0: 0.21573247, 3.5: 0.23657745, 4.0: 0.25572005, 4.5: 0.27353038,
    5.0: 0.29024988, 5.5: 0.30605721, 6.0: 0.32108760, 6.5: 0.33544503,
    7.0: 0.34921268, 7.5: 0.36245775, 8.0: 0.37523559, 8.5: 0.38759241,
    9.0: 0.39956728, 9.5: 0.41119355, 10.0: 0.42250001,
    11.0: 0.44820450, 12.0: 0.47258770, 13.0: 0.49575001,
    14.0: 0.51776695, 15.0: 0.53869629,
    20.0: 0.59740001, 25.0: 0.66999999,
    30.0: 0.73779999, 35.0: 0.79600000,
    40.0: 0.79030001, 41.0: 0.79530001, 42.0: 0.80030000,
    43.0: 0.80530000, 44.0: 0.81029999, 45.0: 0.81529999,
    46.0: 0.82029999, 47.0: 0.82529998, 48.0: 0.83029997,
    49.0: 0.83529997, 50.0: 0.84029999, 50.5: 0.84529999,
    51.0: 0.85029999,
}

def obtener_cpm(nivel: float) -> float:
    """Retorna el CPM para un nivel. Interpola si no está en tabla."""
    if nivel in CPM_TABLE:
        return CPM_TABLE[nivel]
    # Interpolación lineal entre niveles adyacentes
    nivel_bajo = max(k for k in CPM_TABLE if k <= nivel)
    nivel_alto = min(k for k in CPM_TABLE if k >= nivel)
    if nivel_bajo == nivel_alto:
        return CPM_TABLE[nivel_bajo]
    frac = (nivel - nivel_bajo) / (nivel_alto - nivel_bajo)
    return CPM_TABLE[nivel_bajo] + frac * (CPM_TABLE[nivel_alto] - CPM_TABLE[nivel_bajo])


class TipoPokemonGO(StrEnum):
    NORMAL   = "normal"
    SHADOW   = "shadow"
    PURIFIED = "purified"


class CategoriaMovimientoGO(StrEnum):
    RAPIDO   = "rapido"    # Fast Move — genera energía
    CARGADO  = "cargado"   # Charged Move — consume energía


class StatsBaseGO(BaseModel):
    """Stats base oficiales de Pokémon GO (diferentes de los juegos principales)."""
    ataque:  Annotated[int, Field(ge=1, le=400)]
    defensa: Annotated[int, Field(ge=1, le=400)]
    hp:      Annotated[int, Field(ge=1, le=400)]


class IVsGO(BaseModel):
    ataque:  IVGO = 15
    defensa: IVGO = 15
    hp:      IVGO = 15


class MovimientoGO(BaseModel):
    nombre:         str                    = Field(min_length=1, max_length=64)
    tipo:           TipoElemental
    categoria:      CategoriaMovimientoGO
    potencia:       int                    = Field(ge=0, le=300)
    energia:        int = Field(
        description="Positivo=genera (Fast), Negativo=consume (Charged)",
        ge=-100, le=20,
    )
    duracion_turnos: int = Field(ge=1, le=10,
                                  description="Turnos que tarda en ejecutarse")

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()

    @model_validator(mode="after")
    def coherencia_energia(self) -> "MovimientoGO":
        if self.categoria == CategoriaMovimientoGO.RAPIDO and self.energia <= 0:
            raise ValueError("Fast Move debe generar energía (energia > 0)")
        if self.categoria == CategoriaMovimientoGO.CARGADO and self.energia >= 0:
            raise ValueError("Charged Move debe consumir energía (energia < 0)")
        return self


class PokemonGO(BaseModel):
    nombre:        str          = Field(min_length=1, max_length=64)
    tipos:         list[TipoElemental] = Field(min_length=1, max_length=2)
    stats_base:    StatsBaseGO
    ivs:           IVsGO        = IVsGO()
    nivel:         NivelGO      = 40.0
    tipo_pokemon:  TipoPokemonGO = TipoPokemonGO.NORMAL
    fast_move:     MovimientoGO
    charged_moves: list[MovimientoGO] = Field(min_length=1, max_length=2)
    hp_actual:     int | None   = None
    energia_actual: int          = Field(default=0, ge=0, le=100)

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()

    @model_validator(mode="after")
    def charged_coherente(self) -> "PokemonGO":
        for cm in self.charged_moves:
            if cm.categoria != CategoriaMovimientoGO.CARGADO:
                raise ValueError(f"{cm.nombre} debe ser Charged Move.")
        if self.fast_move.categoria != CategoriaMovimientoGO.RAPIDO:
            raise ValueError(f"{self.fast_move.nombre} debe ser Fast Move.")
        return self

    @property
    def cpm(self) -> float:
        return obtener_cpm(self.nivel)

    @property
    def ataque_efectivo(self) -> float:
        base = self.stats_base.ataque + self.ivs.ataque
        mult = 1.2 if self.tipo_pokemon == TipoPokemonGO.SHADOW else 1.0
        return base * self.cpm * mult

    @property
    def defensa_efectiva(self) -> float:
        base = self.stats_base.defensa + self.ivs.defensa
        mult = 0.833 if self.tipo_pokemon == TipoPokemonGO.SHADOW else 1.0
        return base * self.cpm * mult

    @property
    def hp_maximo(self) -> int:
        import math
        return max(10, math.floor((self.stats_base.hp + self.ivs.hp) * self.cpm))


class LigaGO(StrEnum):
    GREAT  = "great"   # CP <= 1500
    ULTRA  = "ultra"   # CP <= 2500
    MASTER = "master"  # sin limite


CP_CAPS: dict[LigaGO, int | None] = {
    LigaGO.GREAT:  1500,
    LigaGO.ULTRA:  2500,
    LigaGO.MASTER: None,
}


class EquipoGO(BaseModel):
    nombre:   str              = Field(min_length=1, max_length=128)
    liga:     LigaGO
    miembros: list[PokemonGO]  = Field(min_length=1, max_length=3)
    escudos:  int              = Field(default=2, ge=0, le=2)

    @field_validator("nombre")
    @classmethod
    def sin_inyeccion(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00", "<", ">"}:
            if c in v:
                raise ValueError(f"Caracter no permitido: {c!r}")
        return v.strip()


class PeticionDanoGO(BaseModel):
    atacante:       PokemonGO
    defensor:       PokemonGO
    movimiento:     MovimientoGO
    defensor_usa_escudo: bool = False


class ResultadoDanoGO(BaseModel):
    atacante:          str
    defensor:          str
    movimiento:        str
    dano:              int
    porcentaje_hp:     float
    efectividad:       float
    stab_aplicado:     bool
    escudo_usado:      bool
    energia_generada:  int    # energia que gana el atacante tras el movimiento
    es_ohko:           bool
    hp_defensor_restante: int


class PeticionCPGO(BaseModel):
    stats_base: StatsBaseGO
    ivs:        IVsGO
    nivel:      NivelGO
    liga:       LigaGO

class ResultadoCPGO(BaseModel):
    cp:            int
    nivel_optimo:  float
    cp_en_cap:     int | None
    dentro_del_cap: bool
