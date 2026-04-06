"""
main.py — CLI ShieldOps Pokémon GO
"""
from __future__ import annotations
import json
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

app = Console()
cli = typer.Typer(name="shieldops-go", help="🎮 ShieldOps Pokémon GO — GBL Season 26")


@cli.command()
def team(
    league: str = typer.Argument("great", help="great | ultra | master"),
    style:  str = typer.Argument("balanced", help="aggro | balanced | budget"),
):
    """Genera el equipo meta para una liga y estilo."""
    from core.models import League, PlayStyle
    from core.teams.generator import generate_team, team_to_text
    try:
        t = generate_team(League(league), PlayStyle(style))
        app.print(Panel(team_to_text(t), title=f"[bold yellow]{t.name}[/]", border_style="yellow"))
    except Exception as e:
        app.print(f"[red]Error:[/] {e}")


@cli.command()
def damage(
    attacker_json: Path = typer.Argument(..., help="JSON del atacante"),
    defender_json: Path = typer.Argument(..., help="JSON del defensor"),
    move_name:     str  = typer.Argument(..., help="Nombre del movimiento"),
):
    """Calcula el daño de un movimiento."""
    from core.models import GoPokemon, GoMove, MoveCategory
    from core.damage.engine import calculate_damage
    try:
        atk_data = json.loads(attacker_json.read_text())
        def_data = json.loads(defender_json.read_text())
        atk = GoPokemon(**atk_data)
        def_ = GoPokemon(**def_data)
        move = next((m for m in (atk.fast_move, *atk.charged_moves) if m and m.name == move_name), None)
        if not move:
            app.print(f"[red]Movimiento '{move_name}' no encontrado en el atacante.[/]")
            raise typer.Exit(1)
        result = calculate_damage(atk, def_, move)
        t = Table(box=box.SIMPLE, show_header=False)
        t.add_row("[dim]Movimiento[/]", result.move_name)
        t.add_row("[dim]Daño[/]",      f"[bold yellow]{result.damage}[/]")
        t.add_row("[dim]HP defensor[/]", str(result.defender_hp))
        t.add_row("[dim]% HP[/]",      f"[bold {'green' if result.is_ko else 'cyan'}]{result.pct_of_hp}%[/]")
        t.add_row("[dim]KO[/]",        "[green]SÍ[/]" if result.is_ko else "[red]NO[/]")
        t.add_row("[dim]Efectividad[/]", f"×{result.type_eff}")
        t.add_row("[dim]STAB[/]",      "[green]SÍ[/]" if result.stab_applied else "NO")
        app.print(Panel(t, title="[bold]Resultado de daño GO[/]", border_style="cyan"))
    except Exception as e:
        app.print(f"[red]Error:[/] {e}")


@cli.command("iv-check")
def iv_check(
    pokemon_json: Path  = typer.Argument(..., help="JSON del Pokémon"),
    league:       str   = typer.Argument("great", help="great | ultra | master"),
):
    """Evalúa los IVs de un Pokémon para una liga."""
    from core.models import GoPokemon, League
    from core.ivs.calculator import evaluate_ivs
    try:
        data = json.loads(pokemon_json.read_text())
        pokemon = GoPokemon(**data)
        report = evaluate_ivs(pokemon, League(league))
        color = "green" if report.is_optimal else "yellow" if report.is_legal_cp else "red"
        app.print(Panel(
            f"[bold]IVs:[/] {report.ivs.attack}/{report.ivs.defense}/{report.ivs.hp}\n"
            f"[bold]CP:[/] {report.cp}\n"
            f"[bold]Legal:[/] {'[green]SÍ[/]' if report.is_legal_cp else '[red]NO[/]'}\n"
            f"[bold]Óptimo:[/] {'[green]SÍ[/]' if report.is_optimal else '[yellow]NO[/]'}\n\n"
            + "\n".join(report.notes + report.suggestions),
            title=f"[bold {color}]IV Report — {pokemon.name} ({league})[/]",
            border_style=color,
        ))
    except Exception as e:
        app.print(f"[red]Error:[/] {e}")


@cli.command("hack-check")
def hack_check(
    pokemon_json: Path = typer.Argument(..., help="JSON del Pokémon"),
    league:       str  = typer.Argument("great", help="great | ultra | master"),
):
    """Valida la legalidad de un Pokémon para GBL."""
    from core.models import GoPokemon, League
    from core.hack_check.validator import validate_pokemon
    try:
        data = json.loads(pokemon_json.read_text())
        pokemon = GoPokemon(**data)
        result = validate_pokemon(pokemon, League(league))
        color = "green" if result.passed else "red"
        lines = []
        for e in result.errors:   lines.append(f"[red]✗ {e}[/]")
        for w in result.warnings: lines.append(f"[yellow]⚠ {w}[/]")
        for n in result.notes:    lines.append(f"[cyan]  {n}[/]")
        app.print(Panel("\n".join(lines) or "[green]Sin problemas[/]",
                        title=f"[bold {color}]Hack-Check — {pokemon.name}[/]",
                        border_style=color))
    except Exception as e:
        app.print(f"[red]Error:[/] {e}")


if __name__ == "__main__":
    cli()
