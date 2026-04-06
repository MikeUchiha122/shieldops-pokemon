"""
core/hack_check/validator.py
Valida la legalidad competitiva de un Pokémon.
Compara contra los Máximos Legales del VGC/LZA y reporta infracciones.
Sin pickling, sin eval — pure Python pydantic.
"""
from __future__ import annotations

from core.models import Pokemon, LegalityReport, Game

# ── Máximos legales globales ──────────────────────────────────────────
MAX_EV_TOTAL   = 510
MAX_EV_SINGLE  = 252
MAX_IV         = 31
MAX_MOVES      = 4
MAX_LEVEL_VGC  = 50


# ── Movimientos baneados (ejemplo VGC 2025) ───────────────────────────
BANNED_MOVES_VGC: frozenset[str] = frozenset({
    "Shadow Force", "Spore", "Baton Pass",
    "Moody",         # habilidad — se verifica por nombre de habilidad también
})

BANNED_ABILITIES_VGC: frozenset[str] = frozenset({
    "Moody", "Power Construct",
})

# Pokémon no permitidos en VGC 2025 (Restricted list — actualizar cada temporada)
RESTRICTED_POKEMON_VGC: frozenset[str] = frozenset({
    "Mewtwo", "Lugia", "Ho-Oh", "Kyogre", "Groudon", "Rayquaza",
    "Dialga", "Palkia", "Giratina", "Reshiram", "Zekrom", "Kyurem",
    "Xerneas", "Yveltal", "Zygarde", "Cosmog", "Cosmoem",
    "Solgaleo", "Lunala", "Necrozma", "Zacian", "Zamazenta",
    "Eternatus", "Calyrex",
})


def validate_pokemon(pokemon: Pokemon, game: Game, format_rules: str = "VGC 2025") -> LegalityReport:
    """
    Valida un Pokémon contra las reglas del formato.
    Retorna un LegalityReport con todas las infracciones detectadas.
    """
    violations: list[str] = []
    warnings:   list[str] = []

    p = pokemon

    # ── 1. EVs ───────────────────────────────────────────────────────
    ev_vals = [p.evs.hp, p.evs.attack, p.evs.defense,
               p.evs.sp_atk, p.evs.sp_def, p.evs.speed]
    total_ev = sum(ev_vals)
    if total_ev > MAX_EV_TOTAL:
        violations.append(f"EVs totales = {total_ev} (máximo legal: {MAX_EV_TOTAL})")
    for stat_name, val in zip(
        ["HP","Ataque","Defensa","Atk. Esp.","Def. Esp.","Velocidad"], ev_vals
    ):
        if val > MAX_EV_SINGLE:
            violations.append(f"EV de {stat_name} = {val} (máximo por stat: {MAX_EV_SINGLE})")

    # ── 2. IVs ───────────────────────────────────────────────────────
    iv_vals = {
        "HP": p.ivs.hp, "Ataque": p.ivs.attack, "Defensa": p.ivs.defense,
        "Atk. Esp.": p.ivs.sp_atk, "Def. Esp.": p.ivs.sp_def, "Velocidad": p.ivs.speed,
    }
    for stat_name, val in iv_vals.items():
        if val > MAX_IV:
            violations.append(f"IV de {stat_name} = {val} (máximo: {MAX_IV})")
        # IVs en 0 en Ataque y Velocidad son LEGALES si son intencionales (trick room, físico puro)
        # Solo avisamos si parecen accidentales
        if val == 0 and stat_name not in ("Velocidad", "Ataque"):
            warnings.append(f"IV 0 en {stat_name} — ¿intencional? Verifica la crianza.")

    # ── 3. Nivel ─────────────────────────────────────────────────────
    if p.level != MAX_LEVEL_VGC:
        warnings.append(
            f"Nivel = {p.level}. El formato {format_rules} usa nivel {MAX_LEVEL_VGC} escalado."
        )

    # ── 4. Movimientos ───────────────────────────────────────────────
    if len(p.moves) > MAX_MOVES:
        violations.append(f"Tiene {len(p.moves)} movimientos (máximo: {MAX_MOVES})")
    move_names = {m.name for m in p.moves}
    banned_found = move_names & BANNED_MOVES_VGC
    if banned_found:
        violations.append(f"Movimientos baneados detectados: {', '.join(banned_found)}")

    # Movimiento duplicado
    if len(move_names) != len(p.moves):
        violations.append("Movimiento duplicado detectado.")

    # ── 5. Habilidad ─────────────────────────────────────────────────
    if p.ability in BANNED_ABILITIES_VGC:
        violations.append(f"Habilidad baneada: {p.ability}")

    # ── 6. Pokémon restringido ────────────────────────────────────────
    if p.name in RESTRICTED_POKEMON_VGC and "Restricted" not in format_rules:
        violations.append(
            f"{p.name} está en la lista Restricted y no está permitido en {format_rules}."
        )

    # ── 7. Tera type (EyP) ───────────────────────────────────────────
    if game == Game.SCARLET_VIOLET and p.tera_type is None:
        warnings.append("Sin tipo Tera asignado — asigna uno para el exportador de Showdown.")

    # ── 8. Ítem duplicado (se verifica a nivel equipo, no aquí) ──────

    is_legal = len(violations) == 0
    return LegalityReport(
        pokemon_name=p.name,
        is_legal=is_legal,
        violations=violations,
        warnings=warnings,
    )


def validate_team(team_members: list[Pokemon], game: Game, format_rules: str = "VGC 2025") -> list[LegalityReport]:
    """Valida un equipo completo. También detecta ítems y especies duplicadas."""
    reports: list[LegalityReport] = []
    items: list[str] = []
    names: list[str] = []

    for pkmn in team_members:
        report = validate_pokemon(pkmn, game, format_rules)

        # Ítem duplicado
        if pkmn.item and pkmn.item in items:
            report.violations.append(f"Ítem duplicado en equipo: {pkmn.item}")
            report.is_legal = False
        if pkmn.item:
            items.append(pkmn.item)

        # Especie duplicada
        if pkmn.name in names:
            report.violations.append(f"Especie duplicada en equipo: {pkmn.name}")
            report.is_legal = False
        names.append(pkmn.name)

        reports.append(report)

    return reports
