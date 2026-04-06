"""
main.py
CLI principal de ShieldOps Pokémon usando Typer + Rich.
Punto de entrada para todas las funciones del sistema.
"""
from __future__ import annotations

from pathlib import Path
import json

import typer
from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel
from rich.markdown import Markdown

app     = typer.Typer(name="shieldops-pokemon", help="🛡️ ShieldOps Pokémon — Competitive Architect")
console = Console()


@app.command("damage")
def cmd_damage(
    attacker_json: Path = typer.Argument(..., help="JSON del atacante"),
    defender_json: Path = typer.Argument(..., help="JSON del defensor"),
    move_name:     str  = typer.Argument(..., help="Nombre del movimiento"),
    tera_active:   bool = typer.Option(False, "--tera", help="¿Teracristalización activa?"),
) -> None:
    """Calcula los 16 rolls de daño entre dos Pokémon."""
    from core.models import Pokemon, Move
    from core.damage.engine import calculate_damage, DamageContext

    try:
        atk  = Pokemon.model_validate_json(attacker_json.read_text())
        dfn  = Pokemon.model_validate_json(defender_json.read_text())
        move = next((m for m in atk.moves if m.name.lower() == move_name.lower()), None)

        if not move:
            console.print(f"[red]Movimiento '{move_name}' no encontrado en el atacante.[/red]")
            raise typer.Exit(1)

        ctx    = DamageContext(attacker=atk, defender=dfn, move=move, is_tera_active=tera_active)
        result = calculate_damage(ctx)

        table = Table(title=f"💥 {result.move_name}: {result.attacker} → {result.defender}")
        table.add_column("Stat",  style="cyan")
        table.add_column("Valor", style="green")

        table.add_row("Rolls (min-max)", f"{result.min_damage}–{result.max_damage}")
        table.add_row("Porcentaje",      f"{result.min_percent}%–{result.max_percent}%")
        table.add_row("OHKO garantizado",
                      "✅ SÍ" if result.is_guaranteed_ohko else ("⚠️ Posible" if result.is_ohko else "❌ No"))
        table.add_row("Modificadores",  ", ".join(result.modifiers_applied) or "Ninguno")

        console.print(table)
        console.print(f"\n🎲 16 rolls: {result.rolls}")

    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("hack-check")
def cmd_hack_check(
    pokemon_json: Path = typer.Argument(..., help="JSON del Pokémon a verificar"),
    game:         str  = typer.Option("scarlet_violet", help="scarlet_violet | legends_za"),
) -> None:
    """Verifica la legalidad de un Pokémon."""
    from core.models import Pokemon, Game
    from core.hack_check.validator import validate_pokemon

    try:
        pkmn   = Pokemon.model_validate_json(pokemon_json.read_text())
        game_e = Game(game)
        report = validate_pokemon(pkmn, game_e)

        if report.is_legal:
            console.print(Panel(f"[green]✅ {pkmn.name} es LEGAL[/green]", title="Hack-Check"))
        else:
            console.print(Panel(f"[red]❌ {pkmn.name} NO es legal[/red]", title="Hack-Check"))

        if report.violations:
            console.print("[red]Infracciones:[/red]")
            for v in report.violations:
                console.print(f"  [red]• {v}[/red]")

        if report.warnings:
            console.print("[yellow]Advertencias:[/yellow]")
            for w in report.warnings:
                console.print(f"  [yellow]• {w}[/yellow]")

    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("export-showdown")
def cmd_export(
    team_json: Path = typer.Argument(..., help="JSON del equipo"),
    output:    Path = typer.Option(Path("./data/exports/team.txt"), help="Archivo de salida"),
) -> None:
    """Exporta un equipo al formato Pokémon Showdown."""
    from core.models import Team
    from core.team.generator import export_to_showdown

    try:
        team = Team.model_validate_json(team_json.read_text())
        text = export_to_showdown(team)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        console.print(f"[green]✅ Equipo exportado a: {output}[/green]")
        console.print(Panel(text, title="Showdown Import"))
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("roadmap")
def cmd_roadmap(
    pokemon_json: Path = typer.Argument(..., help="JSON del Pokémon"),
    game:         str  = typer.Option("scarlet_violet"),
    output:       Path = typer.Option(Path("./guides/markdown/roadmap.md")),
) -> None:
    """Genera la hoja de ruta de entrenamiento en Markdown."""
    from core.models import Pokemon, Game
    from core.team.generator import generate_training_roadmap

    try:
        pkmn   = Pokemon.model_validate_json(pokemon_json.read_text())
        game_e = Game(game)
        roadmap = generate_training_roadmap(pkmn, game_e)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(roadmap.full_markdown, encoding="utf-8")
        console.print(f"[green]✅ Hoja de ruta guardada: {output}[/green]")
        console.print(Markdown(roadmap.full_markdown))
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]Error: {exc}[/red]")
        raise typer.Exit(1) from exc


@app.command("load-guide")
def cmd_load_guide(
    guide_path: Path = typer.Argument(..., help="Ruta al archivo .txt o .md de la guía"),
) -> None:
    """Carga una guía al vector store RAG (ChromaDB)."""
    from data.rag_engine import StrategyVectorDB
    from core.config import get_settings

    cfg = get_settings()
    db  = StrategyVectorDB(str(cfg.chromadb_path), cfg.chromadb_collection)

    if not guide_path.exists():
        console.print(f"[red]Archivo no encontrado: {guide_path}[/red]")
        raise typer.Exit(1)

    db.load_text_file(guide_path)
    console.print(f"[green]✅ Guía cargada al RAG: {guide_path.name}[/green]")


if __name__ == "__main__":
    app()
