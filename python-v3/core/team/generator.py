"""
core/team/generator.py
Exporta equipos al formato Pokémon Showdown.
Genera hojas de ruta de entrenamiento en Markdown con:
  - Guía de IVs (crianza / Chapas de Hyper Training)
  - Guía de EVs (por combate, vitaminas, reseteo con Bayas/Reiniciador)
  - Guía de movimientos (MTs, Movimientos Huevo con Hierba Copia)
"""
from __future__ import annotations

from core.models import Pokemon, Team, TrainingRoadmap, Game, Nature


# ── Natures que boostan/reducen stats ────────────────────────────────
_NATURE_FLAVOR: dict[str, tuple[str, str]] = {
    "adamant":  ("+Ataque", "-Atk. Esp."),
    "modest":   ("+Atk. Esp.", "-Ataque"),
    "jolly":    ("+Velocidad", "-Atk. Esp."),
    "timid":    ("+Velocidad", "-Ataque"),
    "bold":     ("+Defensa", "-Ataque"),
    "impish":   ("+Defensa", "-Atk. Esp."),
    "calm":     ("+Def. Esp.", "-Ataque"),
    "careful":  ("+Def. Esp.", "-Atk. Esp."),
    "relaxed":  ("+Defensa", "-Velocidad"),
    "quiet":    ("+Atk. Esp.", "-Velocidad"),
    "brave":    ("+Ataque", "-Velocidad"),
    "sassy":    ("+Def. Esp.", "-Velocidad"),
}


def export_to_showdown(team: Team) -> str:
    """
    Genera el bloque de texto importable en Pokémon Showdown.
    Formato oficial: https://pokemonshowdown.com/damagecalc/
    """
    lines: list[str] = []

    for p in team.members:
        # Línea 1: Nombre @ Ítem
        item_str = f" @ {p.item}" if p.item else ""
        lines.append(f"{p.name}{item_str}")

        # Tera type (EyP)
        if team.game == Game.SCARLET_VIOLET and p.tera_type:
            lines.append(f"Tera Type: {p.tera_type.value.capitalize()}")

        # Habilidad
        lines.append(f"Ability: {p.ability}")

        # Nivel (VGC siempre 50)
        lines.append(f"Level: {p.level}")

        # EVs — solo stats con valor > 0
        ev_parts: list[str] = []
        ev_map = {
            "HP": p.evs.hp, "Atk": p.evs.attack, "Def": p.evs.defense,
            "SpA": p.evs.sp_atk, "SpD": p.evs.sp_def, "Spe": p.evs.speed,
        }
        for stat, val in ev_map.items():
            if val > 0:
                ev_parts.append(f"{val} {stat}")
        if ev_parts:
            lines.append(f"EVs: {' / '.join(ev_parts)}")

        # Naturaleza
        lines.append(f"{p.nature.value.capitalize()} Nature")

        # IVs — solo si alguno no es 31
        iv_map = {
            "HP": p.ivs.hp, "Atk": p.ivs.attack, "Def": p.ivs.defense,
            "SpA": p.ivs.sp_atk, "SpD": p.ivs.sp_def, "Spe": p.ivs.speed,
        }
        iv_parts = [f"{v} {s}" for s, v in iv_map.items() if v != 31]
        if iv_parts:
            lines.append(f"IVs: {' / '.join(iv_parts)}")

        # Movimientos
        for move in p.moves:
            lines.append(f"- {move.name}")

        lines.append("")   # línea en blanco entre Pokémon

    return "\n".join(lines)


# ── Generador de hoja de ruta ─────────────────────────────────────────

def _iv_guide(p: Pokemon, game: Game) -> str:
    iv_map = {
        "HP": p.ivs.hp, "Ataque": p.ivs.attack, "Defensa": p.ivs.defense,
        "Atk. Esp.": p.ivs.sp_atk, "Def. Esp.": p.ivs.sp_def, "Velocidad": p.ivs.speed,
    }
    lines = [f"## IVs — {p.name}\n"]

    target_ivs = [f"- **{s}**: {v}" for s, v in iv_map.items()]
    lines.append("### IVs objetivo\n" + "\n".join(target_ivs) + "\n")

    # Chapas de Hyper Training
    non_31 = {s: v for s, v in iv_map.items() if v != 31}
    if non_31:
        lines.append("### IVs en 0 (intencionales)")
        for stat, val in non_31.items():
            if val == 0:
                lines.append(
                    f"- **{stat} = 0**: Para IVs en 0, usa una **Chapa Plateada** "
                    f"en Hyper Training y luego reduce con el método de crianza "
                    f"(no hay Chapa de 0 — debes criar con padre/madre de IV 0 en ese stat). "
                    f"Alternativa: usa un Pokémon con el rasgo **Poder** correspondiente en el Jardín de Crianza."
                )
        lines.append("")

    lines.append("### Obtención\n")
    lines.append("**Opción A — Crianza (Jardín de Crianza):**\n")
    lines.append("1. Obtén al menos un progenitor con los IVs deseados.")
    lines.append("2. Equipa **Destino Nudo** al progenitor con mejores IVs para heredar 5 IVs.")
    lines.append("3. Usa **Potencias** (Power Items) para fijar el IV de un stat específico al hijo.")
    lines.append("4. Itera hasta obtener el spread deseado.\n")
    lines.append("**Opción B — Hyper Training (Post-crianza, nivel 50+):**\n")
    lines.append("1. Sube al Pokémon al nivel 50 (obligatorio para Showdown/VGC).")
    lines.append(
        "2. Habla con el **Entrenador de Hyper Training** "
        "(en EyP: Mesagoza Academia; en LZA: Lumialia Centro)."
    )
    lines.append("3. Paga con **Chapas de Plata** (1 por stat) — obtenibles en Raids/Torneos.")
    lines.append("4. Los IVs subirán a 31 **de cara al juego competitivo** (el valor real no cambia).\n")

    return "\n".join(lines)


def _ev_guide(p: Pokemon, game: Game) -> str:
    ev_map = {
        "HP": p.evs.hp, "Ataque": p.evs.attack, "Defensa": p.evs.defense,
        "Atk. Esp.": p.evs.sp_atk, "Def. Esp.": p.evs.sp_def, "Velocidad": p.evs.speed,
    }
    total = sum(ev_map.values())
    lines = [f"## EVs — {p.name}\n"]
    lines.append(f"**Spread total**: {total}/510\n")

    for stat, val in ev_map.items():
        if val > 0:
            lines.append(f"- **{stat}**: {val} EVs")
    lines.append("")

    lines.append("### Métodos de entrenamiento\n")
    lines.append("**Vitaminas (más rápido, hasta 100 EVs por stat):**\n")
    vitamins = {
        "HP":"Proteína HP","Ataque":"Proteína","Defensa":"Hierro",
        "Atk. Esp.":"Calcio","Def. Esp.":"Zinc","Velocidad":"Carbos"
    }
    for stat, val in ev_map.items():
        if val > 0:
            vit = vitamins[stat]
            qty = min(val // 10, 10)   # 1 vitamina = 10 EVs, máx 10 por stat
            if qty > 0:
                lines.append(f"- Usa **{qty}x {vit}** para los primeros {qty*10} EVs de {stat}.")
    lines.append("")
    lines.append("**Por combate (gratis):**\n")
    lines.append("Busca los Pokémon que dan los EVs que necesitas. Usa **Amigovirus** (+1 EV extra por combate) y **Potencia** del stat correspondiente (+8 EVs extra por combate).\n")

    lines.append("### Reset de EVs\n")
    lines.append("- **Bayas Pimientaáraz / Bayas Quago / etc.**: Reducen 10 EVs del stat correspondiente (cosechables en EyP).")
    lines.append("- **Reiniciador de EVs** (LZA): Ítem que resetea todos los EVs a 0 de una vez.")
    lines.append("- Recomendación: resetea antes de re-entrenar si cambiaste el spread.\n")

    return "\n".join(lines)


def _move_guide(p: Pokemon, game: Game) -> str:
    lines = [f"## Movimientos — {p.name}\n"]

    for move in p.moves:
        lines.append(f"### {move.name} ({move.type.value.capitalize()} / {move.category.value})\n")
        # En una versión completa esto consultaría la BD; aquí es template
        lines.append("**Obtención:**")
        lines.append("- Busca esta MT en la Tienda de MTs / Pokémercado (EyP) o en las Tiendas de Lumialia (LZA).")
        lines.append("- Si es **Movimiento Huevo**: usa **Hierba Copia** en el Jardín de Crianza.")
        lines.append("  1. Obtén un Pokémon de la misma Grupo de Crianza que ya sepa el movimiento.")
        lines.append("  2. Ponlo con el objetivo en el Jardín de Crianza con una **Hierba Copia** equipada en el objetivo.")
        lines.append("  3. Da unos pasos — el objetivo aprenderá el movimiento sin necesidad de criar.\n")

    return "\n".join(lines)


def generate_training_roadmap(p: Pokemon, game: Game) -> TrainingRoadmap:
    """Genera la hoja de ruta completa en Markdown para un Pokémon."""
    nature_info = _NATURE_FLAVOR.get(p.nature.value.lower(), ("Neutral", "Neutral"))

    header = (
        f"# Hoja de Ruta — {p.name}\n\n"
        f"**Juego**: {'Escarlata/Púrpura (EyP)' if game == Game.SCARLET_VIOLET else 'Leyendas: Z-A (LZA)'}\n"
        f"**Naturaleza**: {p.nature.value.capitalize()} ({nature_info[0]} / {nature_info[1]})\n"
        f"**Habilidad**: {p.ability}\n"
        f"**Ítem**: {p.item or 'Sin asignar'}\n\n"
        "---\n\n"
    )

    iv_md   = _iv_guide(p, game)
    ev_md   = _ev_guide(p, game)
    move_md = _move_guide(p, game)
    full    = header + iv_md + "\n---\n\n" + ev_md + "\n---\n\n" + move_md

    return TrainingRoadmap(
        pokemon_name=p.name,
        game=game,
        iv_guide=iv_md,
        ev_guide=ev_md,
        move_guide=move_md,
        full_markdown=full,
    )
