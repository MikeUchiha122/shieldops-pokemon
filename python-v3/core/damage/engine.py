"""
core/damage/engine.py
Motor de daño oficial de Pokémon (Gen IX / LZA).
Implementa la fórmula con los 16 rolls (85%–100%).
Soporta:
  - Teracristalización (EyP): STAB 1.5x → 2.0x si mismo tipo que Tera
  - Mega-Lucario / Adaptable (LZA): STAB base 1.5x → 2.0x
  - Sin eval(), sin exec(), sin inputs sin sanitizar.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Move, Pokemon, DamageResult, Type

# Tabla de efectividad de tipos (factor × 10 para evitar floats)
# 0 = inmune, 5 = 0.5x, 10 = 1x, 20 = 2x
_TYPE_CHART: dict[str, dict[str, int]] = {
    "normal":   {"rock":5,"steel":5,"ghost":0},
    "fire":     {"fire":5,"water":5,"rock":5,"dragon":5,"grass":20,"ice":20,"bug":20,"steel":20},
    "water":    {"water":5,"grass":5,"dragon":5,"fire":20,"ground":20,"rock":20},
    "electric": {"electric":5,"grass":5,"dragon":5,"ground":0,"water":20,"flying":20},
    "grass":    {"fire":5,"grass":5,"poison":5,"flying":5,"bug":5,"steel":5,"dragon":5,
                 "water":20,"ground":20,"rock":20},
    "ice":      {"water":5,"ice":5,"fire":5,"steel":5,"grass":20,"ground":20,"flying":20,"dragon":20},
    "fighting": {"flying":5,"poison":5,"bug":5,"psychic":5,"fairy":5,"ghost":0,
                 "normal":20,"ice":20,"rock":20,"dark":20,"steel":20},
    "poison":   {"poison":5,"ground":5,"rock":5,"ghost":5,"steel":0,"grass":20,"fairy":20},
    "ground":   {"grass":5,"bug":5,"flying":0,"fire":20,"electric":20,"poison":20,"rock":20,"steel":20},
    "flying":   {"electric":5,"rock":5,"steel":5,"grass":20,"fighting":20,"bug":20},
    "psychic":  {"psychic":5,"steel":5,"dark":0,"fighting":20,"poison":20},
    "bug":      {"fire":5,"fighting":5,"flying":5,"ghost":5,"steel":5,"fairy":5,
                 "grass":20,"psychic":20,"dark":20},
    "rock":     {"fighting":5,"ground":5,"steel":5,"fire":20,"ice":20,"flying":20,"bug":20},
    "ghost":    {"normal":0,"dark":5,"ghost":20,"psychic":20},
    "dragon":   {"steel":5,"fairy":0,"dragon":20},
    "dark":     {"fighting":5,"dark":5,"fairy":5,"ghost":20,"psychic":20},
    "steel":    {"fire":5,"water":5,"electric":5,"steel":5,
                 "ice":20,"rock":20,"fairy":20},
    "fairy":    {"fire":5,"poison":5,"steel":5,"fighting":20,"dragon":20,"dark":20},
}

# 16 rolls oficiales: 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100
_ROLLS = tuple(range(85, 101))


@dataclass
class DamageContext:
    """Parámetros completos para calcular daño — inmutable."""
    attacker:       "Pokemon"
    defender:       "Pokemon"
    move:           "Move"
    weather:        str | None = None        # "sun","rain","sand","snow"
    terrain:        str | None = None        # "electric","grassy","misty","psychic"
    is_tera_active: bool = False             # ¿atacante teracristalizado? (EyP)
    tera_type:      "Type | None" = None     # tipo Tera activo
    is_mega_active: bool = False             # ¿atacante en Mega-forma? (LZA)


def _type_effectiveness(move_type: str, defender_types: list[str]) -> float:
    """Calcula multiplicador de efectividad total."""
    multiplier = 1.0
    chart = _TYPE_CHART.get(move_type, {})
    for dtype in defender_types:
        factor = chart.get(dtype, 10)   # 10 = 1x por defecto
        multiplier *= factor / 10.0
    return multiplier


def _stab_multiplier(ctx: DamageContext) -> float:
    """
    STAB con mecánicas modernas:
    - Adaptable (Lucario Mega en LZA): 2.0x
    - Tera STAB doble (EyP): 2.0x si tipo del movimiento == Tera tipo == tipo original
    - STAB estándar: 1.5x
    - Sin STAB: 1.0x
    """
    move_type = ctx.move.type.value
    atk_types  = [t.value for t in ctx.attacker.types]
    ability    = ctx.attacker.ability.lower()

    has_stab = move_type in atk_types

    # Adaptable (Mega-Lucario y otros en LZA)
    if ability == "adaptability" and has_stab:
        return 2.0

    # Teracristalización EyP
    if ctx.is_tera_active and ctx.tera_type:
        tera = ctx.tera_type.value
        if move_type == tera:
            # Si además es tipo original del Pokémon: 2.0x; si no: 1.5x
            return 2.0 if has_stab else 1.5
        if has_stab:
            return 1.5

    # STAB estándar
    return 1.5 if has_stab else 1.0


def _stat_at_level(base: int, iv: int, ev: int, level: int, nature_mult: float) -> int:
    """Fórmula oficial de stats para nivel dado."""
    stat = math.floor(((2 * base + iv + ev // 4) * level // 100 + 5) * nature_mult)
    return stat


def _hp_at_level(base: int, iv: int, ev: int, level: int) -> int:
    return math.floor((2 * base + iv + ev // 4) * level // 100 + level + 10)


def _nature_multipliers(nature_name: str) -> dict[str, float]:
    """Retorna multiplicadores de naturaleza para cada stat."""
    boosts: dict[str, str] = {
        "lonely":"attack","brave":"attack","adamant":"attack","naughty":"attack",
        "bold":"defense","relaxed":"defense","impish":"defense","lax":"defense",
        "modest":"sp_atk","mild":"sp_atk","quiet":"sp_atk","rash":"sp_atk",
        "calm":"sp_def","gentle":"sp_def","sassy":"sp_def","careful":"sp_def",
        "timid":"speed","hasty":"speed","jolly":"speed","naive":"speed",
    }
    reduces: dict[str, str] = {
        "lonely":"defense","brave":"speed","adamant":"sp_atk","naughty":"sp_def",
        "bold":"attack","relaxed":"speed","impish":"sp_atk","lax":"sp_def",
        "modest":"attack","mild":"defense","quiet":"speed","rash":"sp_def",
        "calm":"attack","gentle":"defense","sassy":"speed","careful":"sp_atk",
        "timid":"attack","hasty":"defense","jolly":"sp_atk","naive":"sp_def",
    }
    stats = ["attack","defense","sp_atk","sp_def","speed"]
    mults = {s: 1.0 for s in stats}
    n = nature_name.lower()
    if n in boosts:
        mults[boosts[n]] = 1.1
    if n in reduces:
        mults[reduces[n]] = 0.9
    return mults


def calculate_damage(ctx: DamageContext) -> "DamageResult":
    """
    Calcula los 16 rolls de daño según la fórmula oficial Gen IX.

    Fórmula base:
        Damage = floor(floor(floor(2×Level/5 + 2) × BasePower × A/D / 50 + 2)
                       × Targets × Weather × Badge × Critical
                       × random/100 × STAB × Type × Burn × Other)
    """
    from core.models import DamageResult  # import local para evitar ciclos

    # Movimientos de estado — sin daño
    if ctx.move.category.value == "status" or ctx.move.power == 0:
        return DamageResult(
            move_name=ctx.move.name,
            attacker=ctx.attacker.name,
            defender=ctx.defender.name,
            base_damage=0,
            rolls=[0] * 16,
            min_damage=0,
            max_damage=0,
            min_percent=0.0,
            max_percent=0.0,
            is_ohko=False,
            is_guaranteed_ohko=False,
            modifiers_applied=["STATUS — sin daño"],
        )

    atk = ctx.attacker
    dfn = ctx.defender
    move = ctx.move
    level = atk.level

    nature_mults = _nature_multipliers(atk.nature.value)

    # ── Calcular stats efectivos ──────────────────────────────────────
    if move.category.value == "physical":
        atk_base   = atk.base_stats.attack
        atk_iv     = atk.ivs.attack
        atk_ev     = atk.evs.attack
        atk_nmult  = nature_mults["attack"]
        def_base   = dfn.base_stats.defense
        def_iv     = dfn.ivs.defense
        def_ev     = dfn.evs.defense
        def_nature = _nature_multipliers(dfn.nature.value)
        def_nmult  = def_nature["defense"]
        a_stat     = _stat_at_level(atk_base, atk_iv, atk_ev, level, atk_nmult)
        d_stat     = _stat_at_level(def_base, def_iv, def_ev, level, def_nmult)
    else:
        atk_base   = atk.base_stats.sp_atk
        atk_iv     = atk.ivs.sp_atk
        atk_ev     = atk.evs.sp_atk
        atk_nmult  = nature_mults["sp_atk"]
        def_base   = dfn.base_stats.sp_def
        def_iv     = dfn.ivs.sp_def
        def_ev     = dfn.evs.sp_def
        def_nature = _nature_multipliers(dfn.nature.value)
        def_nmult  = def_nature["sp_def"]
        a_stat     = _stat_at_level(atk_base, atk_iv, atk_ev, level, atk_nmult)
        d_stat     = _stat_at_level(def_base, def_iv, def_ev, level, def_nmult)

    def_hp = _hp_at_level(dfn.base_stats.hp, dfn.ivs.hp, dfn.evs.hp, level)

    # ── Modificadores ────────────────────────────────────────────────
    stab    = _stab_multiplier(ctx)
    type_eff = _type_effectiveness(
        move.type.value,
        [t.value for t in dfn.types]
    )

    modifiers: list[str] = []
    if stab > 1.0:
        label = "Adaptable-STAB×2.0" if stab == 2.0 and ctx.is_mega_active else f"STAB×{stab}"
        modifiers.append(label)
    if type_eff != 1.0:
        modifiers.append(f"Effectiveness×{type_eff}")
    if ctx.is_tera_active:
        modifiers.append(f"Tera:{ctx.tera_type}")

    # ── Base de daño (sin roll) ───────────────────────────────────────
    base = math.floor(
        math.floor(
            math.floor(2 * level / 5 + 2) * move.power * a_stat / d_stat / 50
        ) + 2
    )

    # ── 16 rolls ─────────────────────────────────────────────────────
    rolls = [
        math.floor(math.floor(base * roll / 100) * stab * type_eff)
        for roll in _ROLLS
    ]

    min_dmg = rolls[0]
    max_dmg = rolls[-1]
    min_pct = round(min_dmg / def_hp * 100, 1)
    max_pct = round(max_dmg / def_hp * 100, 1)

    return DamageResult(
        move_name=move.name,
        attacker=atk.name,
        defender=dfn.name,
        base_damage=base,
        rolls=rolls,
        min_damage=min_dmg,
        max_damage=max_dmg,
        min_percent=min_pct,
        max_percent=max_pct,
        is_ohko=min_dmg >= def_hp,
        is_guaranteed_ohko=max_dmg >= def_hp,
        modifiers_applied=modifiers,
    )
