"""
core/hack_check/validator.py — Validador de legalidad GBL
Verifica IVs, CP, moves y restricciones de liga.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from core.models import GoPokemon, League, CP_CAPS
from core.damage.engine import calculate_cp

# Pokémon que requieren Elite TM para ciertos movimientos
ELITE_TM_MOVES: dict[str, list[str]] = {
    "Swampert":          ["Hydro Cannon"],
    "Empoleon":          ["Hydro Cannon"],
    "Blastoise":         ["Hydro Cannon"],
    "Charizard":         ["Blast Burn", "Dragon Breath"],
    "Venusaur":          ["Frenzy Plant"],
    "Meganium":          ["Frenzy Plant"],
    "Typhlosion":        ["Blast Burn"],
    "Dragonite":         ["Draco Meteor"],
    "Mewtwo":            ["Shadow Ball", "Psystrike"],
    "Giratina-A":        ["Shadow Claw"],
    "Giratina-O":        ["Shadow Claw", "Shadow Ball"],
    "Zacian-C":          ["Snarl"],
    "Togekiss":          ["Flamethrower"],
    "Melmetal":          ["Double Iron Bash"],
}

# Moves completamente baneados en GBL
BANNED_MOVES_GBL: set[str] = {
    "Fissure", "Sheer Cold", "Horn Drill", "Guillotine",  # OHKO moves (no existen en GO pero por seguridad)
}

# Pokémon baneados o restringidos por liga/temporada
MASTER_ONLY: set[str] = set()  # en GO todos los Pokémon pueden estar en todas las ligas si tienen el CP correcto

SHADOW_BONUS_ATK  = 1.2
SHADOW_PENALTY_DEF = 0.833


@dataclass
class ValidationResult:
    pokemon:   str
    league:    League
    passed:    bool = True
    errors:    list[str] = field(default_factory=list)
    warnings:  list[str] = field(default_factory=list)
    notes:     list[str] = field(default_factory=list)


def validate_pokemon(pokemon: GoPokemon, league: League) -> ValidationResult:
    result = ValidationResult(pokemon=pokemon.name, league=league)
    cap = CP_CAPS[league]

    # ── 1. IVs en rango 0–15 ─────────────────────────────────────
    for stat, val in [("Ataque", pokemon.ivs.attack), ("Defensa", pokemon.ivs.defense), ("HP", pokemon.ivs.hp)]:
        if not (0 <= val <= 15):
            result.errors.append(f"IV {stat} = {val} fuera de rango (debe ser 0–15)")
            result.passed = False

    # ── 2. CP dentro del límite ───────────────────────────────────
    cp = calculate_cp(pokemon)
    if league != League.MASTER and cp > cap:
        result.errors.append(f"CP {cp} excede el límite de {cap} para {league.value.title()} League")
        result.passed = False
    else:
        result.notes.append(f"CP {cp} — dentro del límite de {cap}")

    # ── 3. IVs estratégicamente sospechosos (warning, no error) ───
    if league != League.MASTER:
        if pokemon.ivs.attack > 5:
            result.warnings.append(
                f"IV Ataque = {pokemon.ivs.attack}. Para {league.value.title()} League "
                "los IVs bajos de Ataque (0–3) son meta — más bulk bajo el límite de CP."
            )
    else:
        if pokemon.ivs.attack < 14 or pokemon.ivs.defense < 14 or pokemon.ivs.hp < 14:
            result.warnings.append("En Master League, 15/15/15 maximiza el CP. IVs bajos son subóptimos.")

    # ── 4. Nivel válido ───────────────────────────────────────────
    if not (1.0 <= pokemon.level <= 51.0):
        result.errors.append(f"Nivel {pokemon.level} fuera de rango (1.0–51.0)")
        result.passed = False

    # ── 5. Fast Move ──────────────────────────────────────────────
    if pokemon.fast_move:
        if pokemon.fast_move.category.value != "fast":
            result.errors.append(f"'{pokemon.fast_move.name}' no es un Fast Move")
            result.passed = False
        if pokemon.fast_move.name in BANNED_MOVES_GBL:
            result.errors.append(f"'{pokemon.fast_move.name}' está baneado en GBL")
            result.passed = False
        # Verificar Elite TM
        elite_needed = ELITE_TM_MOVES.get(pokemon.name, [])
        if pokemon.fast_move.name in elite_needed:
            result.notes.append(f"'{pokemon.fast_move.name}' requiere Elite Fast TM para {pokemon.name}")

    # ── 6. Charged Moves ─────────────────────────────────────────
    if len(pokemon.charged_moves) > 2:
        result.errors.append("Máximo 2 Charged Moves permitidos")
        result.passed = False

    for move in pokemon.charged_moves:
        if move.category.value != "charged":
            result.errors.append(f"'{move.name}' no es un Charged Move")
            result.passed = False
        if move.name in BANNED_MOVES_GBL:
            result.errors.append(f"'{move.name}' está baneado en GBL")
            result.passed = False
        elite_needed = ELITE_TM_MOVES.get(pokemon.name, [])
        if move.name in elite_needed:
            result.notes.append(f"'{move.name}' requiere Elite Charged TM para {pokemon.name}")

    # ── 7. Shadow: nota informativa ──────────────────────────────
    if pokemon.shadow:
        result.notes.append(
            f"{pokemon.name} Shadow: +20% Atk ({SHADOW_BONUS_ATK}×), "
            f"-17% Def ({SHADOW_PENALTY_DEF}×). Legal en GBL."
        )

    if result.passed and not result.errors:
        result.notes.insert(0, f"✅ {pokemon.name} es LEGAL para {league.value.title()} League")

    return result
