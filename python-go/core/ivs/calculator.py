"""
core/ivs/calculator.py — Calculadora de IVs para GBL
Determina si un IV spread es óptimo para una liga dada.

Concepto clave: En Great/Ultra League, IVs BAJOS de Ataque
son ventajosos porque permiten alcanzar más HP y Defensa
bajo el límite de CP.
"""
from __future__ import annotations
import math
from core.models import GoPokemon, GoIVSpread, GoIVReport, League, CP_CAPS
from core.damage.engine import calculate_cp, get_cpm


# IVs óptimos conocidos para los Pokémon más usados en GBL S26
# Formato: {nombre: {liga: (atk, def, hp)}}
KNOWN_OPTIMAL_IVS: dict[str, dict[str, tuple[int,int,int]]] = {
    "Galarian Stunfisk": {"great": (0,15,15), "ultra": (0,15,15)},
    "Swampert":          {"great": (0,14,15), "ultra": (0,14,15)},
    "Giratina-A":        {"great": (0,15,14), "ultra": (0,15,15)},
    "Walrein":           {"great": (0,13,15), "ultra": (0,14,15)},
    "Cresselia":         {"ultra": (0,15,15)},
    "Malamar":           {"great": (1,15,15)},
    "Obstagoon":         {"great": (1,14,15), "ultra": (2,15,15)},
    "Florges":           {"great": (0,14,15), "ultra": (0,15,14)},
    "Zacian-C":          {"master": (15,15,15)},
}

# Rango aceptable de IVs de Ataque por liga (lo que se considera competitivo)
ATK_IV_RANGE: dict[str, tuple[int,int]] = {
    "great":  (0, 3),   # 0–3 es el rango meta
    "ultra":  (0, 5),   # más flexibilidad
    "master": (14, 15), # máximo CP
}


def evaluate_ivs(pokemon: GoPokemon, league: League) -> GoIVReport:
    """
    Evalúa si los IVs de un Pokémon son óptimos para la liga.
    """
    cp = calculate_cp(pokemon)
    cap = CP_CAPS[league]
    is_legal = cp <= cap

    notes: list[str] = []
    suggestions: list[str] = []
    is_optimal = False

    atk_range = ATK_IV_RANGE.get(league.value, (0, 15))

    if league == League.MASTER:
        is_optimal = pokemon.ivs.is_hundo
        if not is_optimal:
            suggestions.append("En Master League, el objetivo es 15/15/15 (Hundo) para maximizar CP.")
        if pokemon.ivs.iv_sum == 45:
            notes.append("✅ IVs perfectos (Hundo) — máximo CP posible.")
    else:
        # Great / Ultra League: Atk bajo = más bulk bajo el límite de CP
        atk_ok  = atk_range[0] <= pokemon.ivs.attack <= atk_range[1]
        def_ok  = pokemon.ivs.defense >= 12
        hp_ok   = pokemon.ivs.hp >= 12
        is_optimal = atk_ok and def_ok and hp_ok and is_legal

        if not atk_ok:
            suggestions.append(
                f"IV Ataque {pokemon.ivs.attack} es alto para {league}. "
                f"El rango meta es {atk_range[0]}–{atk_range[1]} — "
                "los IVs bajos de Ataque permiten más HP y Defensa bajo el límite de CP."
            )
        if not def_ok:
            suggestions.append(f"IV Defensa {pokemon.ivs.defense} es bajo. Busca 12+ para mayor durabilidad.")
        if not hp_ok:
            suggestions.append(f"IV HP {pokemon.ivs.hp} es bajo. Busca 12+ para resistir más golpes.")
        if not is_legal:
            suggestions.append(f"CP {cp} excede el límite de {cap} para {league}. Sube a un nivel menor.")

        # Verificar contra óptimos conocidos
        known = KNOWN_OPTIMAL_IVS.get(pokemon.name, {}).get(league.value)
        if known:
            opt_atk, opt_def, opt_hp = known
            if (pokemon.ivs.attack, pokemon.ivs.defense, pokemon.ivs.hp) == (opt_atk, opt_def, opt_hp):
                notes.append(f"✅ IVs idénticos al Rank 1 conocido para {pokemon.name} en {league}.")
            else:
                notes.append(f"💡 Rank 1 conocido para {pokemon.name}: {opt_atk}/{opt_def}/{opt_hp}.")

        if is_optimal:
            notes.append(f"✅ IVs competitivos para {league} — dentro del rango meta.")

    if not is_legal:
        notes.append(f"❌ CP {cp} excede {cap}. El Pokémon no puede entrar en {league}.")
    elif is_legal and league != League.MASTER:
        headroom = cap - cp
        notes.append(f"📊 CP {cp}/{cap} — {headroom} CP de margen hasta el límite.")

    return GoIVReport(
        pokemon=pokemon.name,
        league=league,
        ivs=pokemon.ivs,
        cp=cp,
        is_legal_cp=is_legal,
        is_optimal=is_optimal,
        notes=notes,
        suggestions=suggestions,
    )


def find_max_level_under_cap(
    base_atk: int, base_def: int, base_hp: int,
    iv_atk: int, iv_def: int, iv_hp: int,
    cap: int,
) -> float:
    """
    Encuentra el nivel máximo al que un Pokémon con estos IVs
    puede subir sin superar el CP cap.
    """
    best_level = 1.0
    for level_x2 in range(2, 103):  # niveles 1.0 a 51.0 en pasos de 0.5
        level = level_x2 / 2
        cpm = get_cpm(level)
        atk  = (base_atk  + iv_atk)  * cpm
        def_ = (base_def  + iv_def)  * cpm
        hp   = (base_hp   + iv_hp)   * cpm
        cp = max(10, int(atk * (def_ ** 0.5) * (hp ** 0.5) / 10))
        if cp <= cap:
            best_level = level
        else:
            break
    return best_level
