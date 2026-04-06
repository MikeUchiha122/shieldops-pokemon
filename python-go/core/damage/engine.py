"""
core/damage/engine.py — Motor de daño Pokémon GO
Fórmula oficial: Daño = ⌊0.5 × Power × (Atk/Def) × Modificadores⌋ + 1

Diferencias clave vs VGC:
- IVs: 0–15 (no 0–31)
- STAB: ×1.2 (no ×1.5)
- Efectividad: ×1.6 super eficaz, ×0.625 poco eficaz (no ×2/×0.5)
- Shadow Pokémon: Atk ×1.2, Def ×0.833
- CPM (CP Multiplier) escala los stats según nivel
"""
from __future__ import annotations
import math
from core.models import GoPokemon, GoMove, GoDamageResult

# CPM por nivel (cada 0.5 niveles) — datos oficiales Niantic
CPM_TABLE: dict[float, float] = {
    1.0:0.0939,1.5:0.1351,2.0:0.1664,2.5:0.1927,3.0:0.2157,3.5:0.2365,
    4.0:0.2553,4.5:0.2725,5.0:0.2884,5.5:0.3030,6.0:0.3167,6.5:0.3296,
    7.0:0.3418,7.5:0.3533,8.0:0.3643,8.5:0.3748,9.0:0.3848,9.5:0.3944,
    10.0:0.4236,10.5:0.4399,11.0:0.4550,11.5:0.4691,12.0:0.4823,12.5:0.4947,
    13.0:0.5065,13.5:0.5177,14.0:0.5283,14.5:0.5384,15.0:0.5481,15.5:0.5574,
    16.0:0.5663,16.5:0.5748,17.0:0.5830,17.5:0.5909,18.0:0.5985,18.5:0.6059,
    19.0:0.6130,19.5:0.6199,20.0:0.6265,20.5:0.6329,21.0:0.6391,21.5:0.6451,
    22.0:0.6508,22.5:0.6564,23.0:0.6617,23.5:0.6670,24.0:0.6720,24.5:0.6769,
    25.0:0.6817,25.5:0.6863,26.0:0.6908,26.5:0.6952,27.0:0.6995,27.5:0.7037,
    28.0:0.7079,28.5:0.7119,29.0:0.7159,29.5:0.7198,30.0:0.7236,30.5:0.7274,
    31.0:0.7310,31.5:0.7346,32.0:0.7382,32.5:0.7417,33.0:0.7451,33.5:0.7485,
    34.0:0.7518,34.5:0.7551,35.0:0.7583,35.5:0.7615,36.0:0.7647,36.5:0.7678,
    37.0:0.7708,37.5:0.7739,38.0:0.7769,38.5:0.7799,39.0:0.7828,39.5:0.7857,
    40.0:0.7903,40.5:0.7928,41.0:0.7953,41.5:0.7977,42.0:0.8000,42.5:0.8022,
    43.0:0.8044,43.5:0.8066,44.0:0.8087,44.5:0.8108,45.0:0.8129,45.5:0.8149,
    46.0:0.8169,46.5:0.8188,47.0:0.8208,47.5:0.8227,48.0:0.8246,48.5:0.8265,
    49.0:0.8283,49.5:0.8301,50.0:0.8319,50.5:0.8336,51.0:0.8353,
}

# Tabla de efectividad GO (simplificada — multiplicadores 1.6 / 0.625 / 0.391)
TYPE_EFF: dict[str, dict[str, float]] = {
    "normal":   {"rock":0.625,"steel":0.625,"ghost":0.391},
    "fire":     {"fire":0.625,"water":0.625,"rock":0.625,"dragon":0.625,
                 "grass":1.6,"ice":1.6,"bug":1.6,"steel":1.6},
    "water":    {"water":0.625,"grass":0.625,"dragon":0.625,
                 "fire":1.6,"ground":1.6,"rock":1.6},
    "electric": {"electric":0.625,"grass":0.625,"dragon":0.625,"ground":0.391,
                 "water":1.6,"flying":1.6},
    "grass":    {"fire":0.625,"grass":0.625,"poison":0.625,"flying":0.625,
                 "bug":0.625,"steel":0.625,"dragon":0.625,
                 "water":1.6,"ground":1.6,"rock":1.6},
    "ice":      {"water":0.625,"ice":0.625,"fire":0.625,"steel":0.625,
                 "grass":1.6,"ground":1.6,"flying":1.6,"dragon":1.6},
    "fighting": {"flying":0.625,"poison":0.625,"bug":0.625,"psychic":0.625,
                 "fairy":0.625,"ghost":0.391,
                 "normal":1.6,"ice":1.6,"rock":1.6,"dark":1.6,"steel":1.6},
    "poison":   {"poison":0.625,"ground":0.625,"rock":0.625,"ghost":0.625,
                 "steel":0.391,"grass":1.6,"fairy":1.6},
    "ground":   {"grass":0.625,"bug":0.625,"flying":0.391,
                 "fire":1.6,"electric":1.6,"poison":1.6,"rock":1.6,"steel":1.6},
    "flying":   {"electric":0.625,"rock":0.625,"steel":0.625,
                 "grass":1.6,"fighting":1.6,"bug":1.6},
    "psychic":  {"psychic":0.625,"steel":0.625,"dark":0.391,
                 "fighting":1.6,"poison":1.6},
    "bug":      {"fire":0.625,"fighting":0.625,"flying":0.625,"ghost":0.625,
                 "steel":0.625,"fairy":0.625,
                 "grass":1.6,"psychic":1.6,"dark":1.6},
    "rock":     {"fighting":0.625,"ground":0.625,"steel":0.625,
                 "fire":1.6,"ice":1.6,"flying":1.6,"bug":1.6},
    "ghost":    {"normal":0.391,"dark":0.625,
                 "ghost":1.6,"psychic":1.6},
    "dragon":   {"steel":0.625,"fairy":0.391,"dragon":1.6},
    "dark":     {"fighting":0.625,"fairy":0.625,"dark":0.625,
                 "ghost":1.6,"psychic":1.6},
    "steel":    {"fire":0.625,"water":0.625,"electric":0.625,"steel":0.625,
                 "ice":1.6,"rock":1.6,"fairy":1.6},
    "fairy":    {"fire":0.625,"poison":0.625,"steel":0.625,
                 "fighting":1.6,"dragon":1.6,"dark":1.6},
}

STAB_MULTIPLIER   = 1.2
SHADOW_ATK_BONUS  = 1.2
SHADOW_DEF_PENALTY= 0.833


def get_cpm(level: float) -> float:
    """Retorna el CPM para un nivel dado."""
    if level in CPM_TABLE:
        return CPM_TABLE[level]
    # Interpolación lineal para niveles no exactos
    lower = math.floor(level * 2) / 2
    upper = math.ceil(level * 2) / 2
    if lower == upper:
        return CPM_TABLE.get(lower, 0.7903)
    cpm_l = CPM_TABLE.get(lower, 0.7903)
    cpm_u = CPM_TABLE.get(upper, 0.7903)
    t = (level - lower) / (upper - lower)
    return cpm_l + t * (cpm_u - cpm_l)


def effective_attack(pokemon: GoPokemon) -> float:
    cpm = get_cpm(pokemon.level)
    atk = (pokemon.base_attack + pokemon.ivs.attack) * cpm
    if pokemon.shadow:
        atk *= SHADOW_ATK_BONUS
    return atk


def effective_defense(pokemon: GoPokemon) -> float:
    cpm = get_cpm(pokemon.level)
    def_ = (pokemon.base_defense + pokemon.ivs.defense) * cpm
    if pokemon.shadow:
        def_ *= SHADOW_DEF_PENALTY
    return def_


def effective_hp(pokemon: GoPokemon) -> int:
    cpm = get_cpm(pokemon.level)
    return max(10, int((pokemon.base_hp + pokemon.ivs.hp) * cpm))


def calculate_cp(pokemon: GoPokemon) -> int:
    """Calcula CP oficial."""
    cpm = get_cpm(pokemon.level)
    atk = (pokemon.base_attack  + pokemon.ivs.attack)  * cpm
    def_ = (pokemon.base_defense + pokemon.ivs.defense) * cpm
    hp   = (pokemon.base_hp      + pokemon.ivs.hp)     * cpm
    cp = int(atk * (def_ ** 0.5) * (hp ** 0.5) / 10)
    return max(10, cp)


def get_type_effectiveness(move_type: str, defender_types: list[str]) -> float:
    """Calcula multiplicador de tipo total."""
    eff_table = TYPE_EFF.get(move_type.lower(), {})
    multiplier = 1.0
    for dtype in defender_types:
        multiplier *= eff_table.get(dtype.lower(), 1.0)
    return multiplier


def calculate_damage(
    attacker: GoPokemon,
    defender: GoPokemon,
    move: GoMove,
) -> GoDamageResult:
    """
    Fórmula oficial GO:
    Daño = ⌊0.5 × Power × (EffAtk / EffDef) × STAB × TypeEff⌋ + 1
    """
    eff_atk = effective_attack(attacker)
    eff_def = effective_defense(defender)
    def_hp  = effective_hp(defender)

    # STAB — ×1.2 si el tipo del movimiento coincide con algún tipo del atacante
    stab = STAB_MULTIPLIER if move.type.lower() in [t.lower() for t in attacker.types] else 1.0

    # Efectividad de tipo
    type_eff = get_type_effectiveness(move.type, defender.types)

    # Fórmula
    raw = 0.5 * move.power * (eff_atk / eff_def) * stab * type_eff
    damage = int(raw) + 1  # mínimo 1

    pct = round(damage / def_hp * 100, 1)

    return GoDamageResult(
        attacker=attacker.name,
        defender=defender.name,
        move_name=move.name,
        move_type=move.type,
        damage=damage,
        defender_hp=def_hp,
        pct_of_hp=pct,
        is_ko=damage >= def_hp,
        type_eff=type_eff,
        stab_applied=stab > 1.0,
        energy_generated=move.energy if move.category.value == "fast" else 0,
    )
