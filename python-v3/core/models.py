"""
core/models.py
Modelos de datos con Pydantic v2 + type hints modernos.
Todo input externo DEBE pasar por estos modelos antes de procesarse.
Sin pickle, sin eval, sin os.system con datos de usuario.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator


# ══════════════════════════════════════════════════════════════════════
# Enumerados
# ══════════════════════════════════════════════════════════════════════

class Game(StrEnum):
    SCARLET_VIOLET = "scarlet_violet"   # EyP — Teracristalización
    LEGENDS_ZA     = "legends_za"       # LZA — 3v3, Mega-Evolución


class Type(StrEnum):
    NORMAL   = "normal";  FIRE     = "fire";    WATER    = "water"
    ELECTRIC = "electric"; GRASS   = "grass";   ICE      = "ice"
    FIGHTING = "fighting"; POISON  = "poison";  GROUND   = "ground"
    FLYING   = "flying";   PSYCHIC = "psychic"; BUG      = "bug"
    ROCK     = "rock";     GHOST   = "ghost";   DRAGON   = "dragon"
    DARK     = "dark";     STEEL   = "steel";   FAIRY    = "fairy"


class Nature(StrEnum):
    HARDY  = "hardy";  LONELY = "lonely"; BRAVE  = "brave"
    ADAMANT= "adamant";NAUGHTY= "naughty";BOLD   = "bold"
    DOCILE = "docile"; RELAXED= "relaxed";IMPISH = "impish"
    LAX    = "lax";    TIMID  = "timid";  HASTY  = "hasty"
    JOLLY  = "jolly";  NAIVE  = "naive";  MODEST = "modest"
    MILD   = "mild";   QUIET  = "quiet";  BASHFUL= "bashful"
    RASH   = "rash";   CALM   = "calm";   GENTLE = "gentle"
    SASSY  = "sassy";  CAREFUL= "careful";QUIRKY = "quirky"


class MoveCategory(StrEnum):
    PHYSICAL = "physical"
    SPECIAL  = "special"
    STATUS   = "status"


# ══════════════════════════════════════════════════════════════════════
# Tipos auxiliares con validación
# ══════════════════════════════════════════════════════════════════════

# EVs: 0-252 por stat, máximo 510 total entre todos
EV = Annotated[int, Field(ge=0, le=252)]
# IVs: 0-31 (o 0 intencional para velocidad/ataque)
IV = Annotated[int, Field(ge=0, le=31)]
# Nivel: 1-100
Level = Annotated[int, Field(ge=1, le=100)]
# Poder base de movimiento
BasePower = Annotated[int, Field(ge=0, le=999)]


# ══════════════════════════════════════════════════════════════════════
# Modelos de Movimientos
# ══════════════════════════════════════════════════════════════════════

class Move(BaseModel):
    name:     str         = Field(min_length=1, max_length=64)
    type:     Type
    category: MoveCategory
    power:    BasePower   = 0
    accuracy: int | None  = Field(default=None, ge=1, le=100)  # None = never-miss
    pp:       int         = Field(ge=1, le=64)
    # Flags de mecánica relevante
    makes_contact:    bool = False
    sound_based:      bool = False
    punch_based:      bool = False
    priority:         int  = Field(default=0, ge=-7, le=7)

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        """Elimina caracteres peligrosos — no se usa eval ni exec."""
        return v.strip()


# ══════════════════════════════════════════════════════════════════════
# Modelos de Pokémon
# ══════════════════════════════════════════════════════════════════════

class BaseStats(BaseModel):
    hp:      int = Field(ge=1, le=255)
    attack:  int = Field(ge=1, le=255)
    defense: int = Field(ge=1, le=255)
    sp_atk:  int = Field(ge=1, le=255)
    sp_def:  int = Field(ge=1, le=255)
    speed:   int = Field(ge=1, le=255)


class EVSpread(BaseModel):
    hp:      EV = 0
    attack:  EV = 0
    defense: EV = 0
    sp_atk:  EV = 0
    sp_def:  EV = 0
    speed:   EV = 0

    @model_validator(mode="after")
    def total_max_510(self) -> EVSpread:
        total = self.hp + self.attack + self.defense + self.sp_atk + self.sp_def + self.speed
        if total > 510:
            msg = f"Total EVs ({total}) excede el máximo legal de 510."
            raise ValueError(msg)
        return self


class IVSpread(BaseModel):
    hp:      IV = 31
    attack:  IV = 31
    defense: IV = 31
    sp_atk:  IV = 31
    sp_def:  IV = 31
    speed:   IV = 31


class Pokemon(BaseModel):
    """Representación completa de un Pokémon competitivo."""
    name:       str        = Field(min_length=1, max_length=64)
    dex_number: int        = Field(ge=1, le=9999)
    types:      list[Type] = Field(min_length=1, max_length=2)
    base_stats: BaseStats
    nature:     Nature
    ability:    str        = Field(min_length=1, max_length=64)
    item:       str | None = Field(default=None, max_length=64)
    level:      Level      = 50
    ivs:        IVSpread   = IVSpread()
    evs:        EVSpread   = EVSpread()
    moves:      list[Move] = Field(min_length=1, max_length=4)
    # Mecánicas por juego
    tera_type:  Type | None = None        # EyP — Teracristalización
    can_mega:   bool        = False       # LZA — elegible para Mega

    @field_validator("name", "ability")
    @classmethod
    def no_injection(cls, v: str) -> str:
        """Previene caracteres de inyección SQL / shell."""
        forbidden_chars = {"'", '"', ";", "--", "/*", "*/", "\x00"}
        for ch in forbidden_chars:
            if ch in v:
                msg = f"Carácter no permitido detectado: {ch!r}"
                raise ValueError(msg)
        return v.strip()


# ══════════════════════════════════════════════════════════════════════
# Modelos de Equipo
# ══════════════════════════════════════════════════════════════════════

class Team(BaseModel):
    name:    str          = Field(min_length=1, max_length=128)
    game:    Game
    members: list[Pokemon] = Field(min_length=1, max_length=6)
    format:  str          = "VGC 2025"   # ej: "VGC 2025", "LZA 3v3"

    @model_validator(mode="after")
    def validate_game_rules(self) -> Team:
        if self.game == Game.LEGENDS_ZA and len(self.members) not in (3, 6):
            # LZA permite equipos de 3 (battles) o 6 (full roster)
            pass
        return self


# ══════════════════════════════════════════════════════════════════════
# Modelos de resultado / output (limpios para serialización)
# ══════════════════════════════════════════════════════════════════════

class DamageResult(BaseModel):
    """Resultado del motor de daño con rangos."""
    move_name:       str
    attacker:        str
    defender:        str
    base_damage:     int
    rolls:           list[int]   # 16 valores (85%–100%)
    min_damage:      int
    max_damage:      int
    min_percent:     float
    max_percent:     float
    is_ohko:         bool        # mata en un golpe (mínimo)
    is_guaranteed_ohko: bool     # mata en un golpe (máximo)
    modifiers_applied: list[str] # STAB, Adaptable, Tera, etc.


class LegalityReport(BaseModel):
    """Resultado del Hack-Check."""
    pokemon_name: str
    is_legal:     bool
    violations:   list[str] = []   # lista de infracciones detectadas
    warnings:     list[str] = []   # advertencias (no bloquean pero son sospechosas)


class TrainingRoadmap(BaseModel):
    """Hoja de ruta de entrenamiento exportable a Markdown."""
    pokemon_name: str
    game:         Game
    iv_guide:     str   # Markdown
    ev_guide:     str   # Markdown
    move_guide:   str   # Markdown
    full_markdown: str  # Documento completo concatenado
