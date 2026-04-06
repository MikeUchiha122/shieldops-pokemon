"""
core/models.py — Modelos Pokémon GO competitivo
IVs 0–15 | CP dinámico | Fast+Charged Moves | Ligas con límite
"""
from __future__ import annotations
from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, model_validator


class League(StrEnum):
    GREAT  = "great"    # ≤1500 CP
    ULTRA  = "ultra"    # ≤2500 CP
    MASTER = "master"   # sin límite


class MoveCategory(StrEnum):
    FAST    = "fast"
    CHARGED = "charged"


class PlayStyle(StrEnum):
    AGGRO    = "aggro"
    BALANCED = "balanced"
    BUDGET   = "budget"


class TeamRole(StrEnum):
    LEAD        = "lead"
    SAFE_SWITCH = "safe_switch"
    CLOSER      = "closer"


GoIV = Annotated[int, Field(ge=0, le=15)]
CP_CAPS = {League.GREAT: 1500, League.ULTRA: 2500, League.MASTER: 99_999}


class GoIVSpread(BaseModel):
    attack:  GoIV = 15
    defense: GoIV = 15
    hp:      GoIV = 15

    @property
    def is_hundo(self) -> bool:
        return self.attack == 15 and self.defense == 15 and self.hp == 15

    @property
    def is_nundo(self) -> bool:
        return self.attack == 0 and self.defense == 0 and self.hp == 0

    @property
    def iv_sum(self) -> int:
        return self.attack + self.defense + self.hp


class GoMove(BaseModel):
    name:              str          = Field(min_length=1, max_length=64)
    type:              str
    category:          MoveCategory
    power:             int          = Field(ge=0, le=300)
    energy:            int          = Field(ge=0, le=100)
    cooldown_ms:       int          = Field(default=700, ge=100)
    requires_elite_tm: bool         = False

    @field_validator("name")
    @classmethod
    def sanitize(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00"}:
            if c in v:
                raise ValueError(f"Carácter no permitido: {c!r}")
        return v.strip()


class GoPokemon(BaseModel):
    name:          str            = Field(min_length=1, max_length=64)
    types:         list[str]      = Field(min_length=1, max_length=2)
    base_attack:   int            = Field(ge=1, le=500)
    base_defense:  int            = Field(ge=1, le=500)
    base_hp:       int            = Field(ge=1, le=500)
    ivs:           GoIVSpread     = GoIVSpread()
    level:         float          = Field(ge=1.0, le=51.0, default=40.0)
    fast_move:     GoMove | None  = None
    charged_moves: list[GoMove]   = Field(default_factory=list, max_length=2)
    role:          TeamRole | None = None
    shadow:        bool           = False

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        for c in {"'", '"', ";", "--", "\x00"}:
            if c in v:
                raise ValueError(f"Carácter no permitido: {c!r}")
        return v.strip()


class GoTeam(BaseModel):
    name:    str            = Field(min_length=1, max_length=128)
    league:  League
    style:   PlayStyle
    season:  str            = "Season 26"
    members: list[GoPokemon] = Field(min_length=3, max_length=3)


class GoDamageResult(BaseModel):
    attacker:         str
    defender:         str
    move_name:        str
    move_type:        str
    damage:           int
    defender_hp:      int
    pct_of_hp:        float
    is_ko:            bool
    type_eff:         float
    stab_applied:     bool
    energy_generated: int


class GoIVReport(BaseModel):
    pokemon:     str
    league:      League
    ivs:         GoIVSpread
    cp:          int
    is_legal_cp: bool
    is_optimal:  bool
    notes:       list[str] = []
    suggestions: list[str] = []
