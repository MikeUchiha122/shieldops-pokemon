"""
core/teams/generator.py — Generador de equipos GBL Season 26
Datos del meta: PvPoke + Dexerto S26 (Mar–Jun 2026)
"""
from __future__ import annotations
from core.models import GoTeam, GoPokemon, GoIVSpread, GoMove, MoveCategory, League, PlayStyle, TeamRole


# ── Base de datos meta S26 ────────────────────────────────────────
META_TEAMS: dict[str, dict[str, dict]] = {
    "great": {
        "aggro": {
            "name": "Great League Agresivo — S26",
            "desc": "Presión máxima desde el turno 1. Malamar abre con Night Slash bait. Empoleon pivotea con sus 10 resistencias. Forretress cierra con Earthquake.",
            "members": [
                {"name":"Malamar",  "types":["dark","psychic"],"ba":144,"bd":109,"bhp":190,
                 "ivs":(1,15,15),"level":38.5,"cp":1489,"role":"lead",
                 "fast":("Foul Play","dark","fast",12,7,500),
                 "charged":[("Night Slash","dark","charged",50,35,500),("Superpower","fighting","charged",85,40,500)]},
                {"name":"Empoleon","types":["water","steel"],"ba":210,"bd":213,"bhp":197,
                 "ivs":(0,13,15),"level":22.0,"cp":1497,"role":"safe_switch",
                 "fast":("Waterfall","water","fast",12,8,800),
                 "charged":[("Hydro Cannon","water","charged",80,40,500),("Flash Cannon","steel","charged",100,70,500)]},
                {"name":"Forretress","types":["bug","steel"],"ba":161,"bd":205,"bhp":190,
                 "ivs":(0,15,14),"level":30.0,"cp":1495,"role":"closer",
                 "fast":("Bug Bite","bug","fast",3,3,500),
                 "charged":[("Heavy Slam","steel","charged",70,50,500),("Earthquake","ground","charged",120,65,500)]},
            ]
        },
        "balanced": {
            "name": "Great League Balanceado — S26",
            "desc": "El equipo más sólido del meta. G-Stunfisk como safe switch universal con 10 resistencias. Obstagoon genera energía con Counter. Swampert solo tiene 1 counter (Grass).",
            "members": [
                {"name":"Galarian Stunfisk","types":["ground","steel"],"ba":144,"bd":179,"bhp":198,
                 "ivs":(0,15,15),"level":29.0,"cp":1500,"role":"lead",
                 "fast":("Mud Shot","ground","fast",3,4,500),
                 "charged":[("Rock Slide","rock","charged",75,45,500),("Earthquake","ground","charged",120,65,500)]},
                {"name":"Obstagoon","types":["dark","normal"],"ba":190,"bd":185,"bhp":230,
                 "ivs":(1,14,15),"level":22.5,"cp":1492,"role":"safe_switch",
                 "fast":("Counter","fighting","fast",8,7,900),
                 "charged":[("Night Slash","dark","charged",50,35,500),("Hyper Beam","normal","charged",150,80,500)]},
                {"name":"Swampert","types":["water","ground"],"ba":208,"bd":175,"bhp":225,
                 "ivs":(0,14,15),"level":19.5,"cp":1498,"role":"closer",
                 "fast":("Mud Shot","ground","fast",3,4,500),
                 "charged":[("Hydro Cannon","water","charged",80,40,500),("Earthquake","ground","charged",120,65,500)]},
            ]
        },
        "budget": {
            "name": "Great League Budget — S26",
            "desc": "Sin Legendarios ni Elite TMs. Galarian Stunfisk es farmeable en GBL rewards. Obstagoon se evoluciona desde Zigzagoon de Galar. Poliwrath es accesible y cubre a Walrein.",
            "members": [
                {"name":"Galarian Stunfisk","types":["ground","steel"],"ba":144,"bd":179,"bhp":198,
                 "ivs":(0,15,15),"level":29.0,"cp":1500,"role":"lead",
                 "fast":("Mud Shot","ground","fast",3,4,500),
                 "charged":[("Rock Slide","rock","charged",75,45,500),("Earthquake","ground","charged",120,65,500)]},
                {"name":"Obstagoon","types":["dark","normal"],"ba":190,"bd":185,"bhp":230,
                 "ivs":(1,14,15),"level":22.5,"cp":1492,"role":"safe_switch",
                 "fast":("Counter","fighting","fast",8,7,900),
                 "charged":[("Night Slash","dark","charged",50,35,500),("Hyper Beam","normal","charged",150,80,500)]},
                {"name":"Poliwrath","types":["water","fighting"],"ba":182,"bd":187,"bhp":207,
                 "ivs":(0,15,14),"level":23.5,"cp":1494,"role":"closer",
                 "fast":("Mud Shot","ground","fast",3,4,500),
                 "charged":[("Dynamic Punch","fighting","charged",90,50,500),("Ice Punch","ice","charged",55,40,500)]},
            ]
        },
    },
    "ultra": {
        "aggro": {
            "name": "Ultra League Agresivo — S26",
            "desc": "Walrein abre con Icicle Spear spam para quemar shields en 2 turnos. Cresselia es el safe switch más bulky del juego. Giratina-A cierra sin shields abajo.",
            "members": [
                {"name":"Walrein","types":["ice","water"],"ba":182,"bd":176,"bhp":260,
                 "ivs":(0,14,15),"level":50.0,"cp":2497,"role":"lead",
                 "fast":("Powder Snow","ice","fast",5,8,500),
                 "charged":[("Icicle Spear","ice","charged",60,40,500),("Earthquake","ground","charged",120,65,500)]},
                {"name":"Cresselia","types":["psychic"],"ba":152,"bd":258,"bhp":260,
                 "ivs":(0,15,15),"level":29.0,"cp":2499,"role":"safe_switch",
                 "fast":("Psycho Cut","psychic","fast",3,9,500),
                 "charged":[("Moonblast","fairy","charged",130,70,500),("Grass Knot","grass","charged",90,50,500)]},
                {"name":"Giratina-A","types":["ghost","dragon"],"ba":187,"bd":225,"bhp":284,
                 "ivs":(0,15,15),"level":28.5,"cp":2493,"role":"closer",
                 "fast":("Shadow Claw","ghost","fast",9,8,700),
                 "charged":[("Shadow Ball","ghost","charged",100,55,500),("Dragon Claw","dragon","charged",50,35,500)]},
            ]
        },
        "balanced": {
            "name": "Ultra League Balanceado — S26",
            "desc": "Giratina-A define Ultra League con Ghost/Dragon + bulk extraordinario. Florges cubre Dragon/Dark/Fighting. Galarian Moltres destroza a Cresselia con Payback.",
            "members": [
                {"name":"Giratina-A","types":["ghost","dragon"],"ba":187,"bd":225,"bhp":284,
                 "ivs":(0,15,15),"level":28.5,"cp":2493,"role":"lead",
                 "fast":("Shadow Claw","ghost","fast",9,8,700),
                 "charged":[("Shadow Ball","ghost","charged",100,55,500),("Dragon Claw","dragon","charged",50,35,500)]},
                {"name":"Florges","types":["fairy"],"ba":169,"bd":244,"bhp":223,
                 "ivs":(0,15,14),"level":45.0,"cp":2494,"role":"safe_switch",
                 "fast":("Fairy Wind","fairy","fast",3,9,500),
                 "charged":[("Disarming Voice","fairy","charged",70,45,500),("Moonblast","fairy","charged",130,70,500)]},
                {"name":"Galarian Moltres","types":["dark","flying"],"ba":240,"bd":185,"bhp":207,
                 "ivs":(0,15,15),"level":25.5,"cp":2499,"role":"closer",
                 "fast":("Wing Attack","flying","fast",5,9,500),
                 "charged":[("Payback","dark","charged",110,60,500),("Ancient Power","rock","charged",70,45,500)]},
            ]
        },
        "budget": {
            "name": "Ultra League Budget — S26",
            "desc": "Sin Legendarios. Obstagoon abre con Counter rapidísimo. G-Stunfisk como safe switch universal. Poliwrath cierra contra Walrein y Dark types.",
            "members": [
                {"name":"Obstagoon","types":["dark","normal"],"ba":190,"bd":185,"bhp":230,
                 "ivs":(2,15,15),"level":35.5,"cp":2489,"role":"lead",
                 "fast":("Counter","fighting","fast",8,7,900),
                 "charged":[("Night Slash","dark","charged",50,35,500),("Cross Chop","fighting","charged",50,35,500)]},
                {"name":"Galarian Stunfisk","types":["ground","steel"],"ba":144,"bd":179,"bhp":198,
                 "ivs":(0,15,15),"level":40.5,"cp":2494,"role":"safe_switch",
                 "fast":("Mud Shot","ground","fast",3,4,500),
                 "charged":[("Rock Slide","rock","charged",75,45,500),("Earthquake","ground","charged",120,65,500)]},
                {"name":"Poliwrath","types":["water","fighting"],"ba":182,"bd":187,"bhp":207,
                 "ivs":(0,14,15),"level":38.5,"cp":2492,"role":"closer",
                 "fast":("Mud Shot","ground","fast",3,4,500),
                 "charged":[("Dynamic Punch","fighting","charged",90,50,500),("Ice Punch","ice","charged",55,40,500)]},
            ]
        },
    },
    "master": {
        "aggro": {
            "name": "Master League Agresivo — S26",
            "desc": "Zacian-C es el Pokémon más temido de Master. Origin Palkia tiene cobertura Water/Dragon incomparable. Zekrom cierra con Wild Charge + Dragon Breath.",
            "members": [
                {"name":"Zacian-C","types":["fairy","steel"],"ba":332,"bd":250,"bhp":192,
                 "ivs":(15,15,15),"level":50.0,"cp":4444,"role":"lead",
                 "fast":("Snarl","dark","fast",5,12,800),
                 "charged":[("Play Rough","fairy","charged",90,60,500),("Close Combat","fighting","charged",100,45,500)]},
                {"name":"Origin Palkia","types":["water","dragon"],"ba":280,"bd":215,"bhp":189,
                 "ivs":(15,15,15),"level":50.0,"cp":4336,"role":"safe_switch",
                 "fast":("Dragon Breath","dragon","fast",4,9,500),
                 "charged":[("Aqua Tail","water","charged",50,35,500),("Draco Meteor","dragon","charged",150,65,500)]},
                {"name":"Zekrom","types":["dragon","electric"],"ba":275,"bd":211,"bhp":216,
                 "ivs":(15,15,15),"level":50.0,"cp":4038,"role":"closer",
                 "fast":("Dragon Breath","dragon","fast",4,9,500),
                 "charged":[("Wild Charge","electric","charged",90,45,500),("Crunch","dark","charged",70,45,500)]},
            ]
        },
        "balanced": {
            "name": "Master League Balanceado — S26",
            "desc": "Zacian-C + Lunala + Reshiram. Lunala tiene Shadow Claw para energía rápida y Mooblast baja Ataque del rival. Reshiram cierra con Fusion Flare — uno de los mejores DPE del juego.",
            "members": [
                {"name":"Zacian-C","types":["fairy","steel"],"ba":332,"bd":250,"bhp":192,
                 "ivs":(15,15,15),"level":50.0,"cp":4444,"role":"lead",
                 "fast":("Snarl","dark","fast",5,12,800),
                 "charged":[("Play Rough","fairy","charged",90,60,500),("Close Combat","fighting","charged",100,45,500)]},
                {"name":"Lunala","types":["psychic","ghost"],"ba":261,"bd":211,"bhp":264,
                 "ivs":(15,15,15),"level":50.0,"cp":4186,"role":"safe_switch",
                 "fast":("Shadow Claw","ghost","fast",9,8,700),
                 "charged":[("Moonblast","fairy","charged",130,70,500),("Shadow Ball","ghost","charged",100,55,500)]},
                {"name":"Reshiram","types":["dragon","fire"],"ba":275,"bd":211,"bhp":205,
                 "ivs":(15,15,15),"level":50.0,"cp":4038,"role":"closer",
                 "fast":("Dragon Breath","dragon","fast",4,9,500),
                 "charged":[("Fusion Flare","fire","charged",90,40,500),("Draco Meteor","dragon","charged",150,65,500)]},
            ]
        },
        "budget": {
            "name": "Master League Budget (sin Legendarios) — S26",
            "desc": "Metagross + Dragonite + Florges. Sin Legendarios ni Míticos. Metagross tiene 10 resistencias y Meteor Mash es brutal. Dragonite con Superpower mata a Steel types.",
            "members": [
                {"name":"Metagross","types":["steel","psychic"],"ba":257,"bd":228,"bhp":190,
                 "ivs":(15,15,15),"level":50.0,"cp":3791,"role":"lead",
                 "fast":("Bullet Punch","steel","fast",6,7,500),
                 "charged":[("Meteor Mash","steel","charged",100,50,500),("Earthquake","ground","charged",120,65,500)]},
                {"name":"Dragonite","types":["dragon","flying"],"ba":263,"bd":198,"bhp":209,
                 "ivs":(15,15,15),"level":50.0,"cp":3792,"role":"safe_switch",
                 "fast":("Dragon Breath","dragon","fast",4,9,500),
                 "charged":[("Dragon Claw","dragon","charged",50,35,500),("Superpower","fighting","charged",85,40,500)]},
                {"name":"Florges","types":["fairy"],"ba":169,"bd":244,"bhp":223,
                 "ivs":(15,15,15),"level":50.0,"cp":2757,"role":"closer",
                 "fast":("Fairy Wind","fairy","fast",3,9,500),
                 "charged":[("Moonblast","fairy","charged",130,70,500),("Psychic","psychic","charged",90,55,500)]},
            ]
        },
    },
}


def _build_pokemon(data: dict) -> GoPokemon:
    fast_d = data["fast"]
    # tuple: (name, type, category_str, power, energy, cooldown_ms)
    fast_move = GoMove(name=fast_d[0], type=fast_d[1], category=MoveCategory.FAST,
                       power=fast_d[3], energy=fast_d[4], cooldown_ms=fast_d[5])
    charged = [GoMove(name=c[0], type=c[1], category=MoveCategory.CHARGED,
                      power=c[3], energy=c[4], cooldown_ms=c[5])
               for c in data["charged"]]
    return GoPokemon(
        name=data["name"], types=data["types"],
        base_attack=data["ba"], base_defense=data["bd"], base_hp=data["bhp"],
        ivs=GoIVSpread(attack=data["ivs"][0], defense=data["ivs"][1], hp=data["ivs"][2]),
        level=data["level"], fast_move=fast_move, charged_moves=charged,
        role=TeamRole(data["role"]),
    )


def generate_team(league: League, style: PlayStyle) -> GoTeam:
    """Genera el equipo meta para la liga y estilo dados."""
    raw = META_TEAMS.get(league.value, {}).get(style.value)
    if not raw:
        raise ValueError(f"No hay equipo para liga={league} style={style}")
    members = [_build_pokemon(m) for m in raw["members"]]
    return GoTeam(name=raw["name"], league=league, style=style, members=members)


def team_to_text(team: GoTeam) -> str:
    """Exporta el equipo a texto legible."""
    lines = [f"=== {team.name} ===", f"Liga: {team.league} | Estilo: {team.style}", ""]
    for i, p in enumerate(team.members, 1):
        role_str = p.role.value.replace("_", " ").title() if p.role else "?"
        fm = p.fast_move
        charged = " / ".join(c.name for c in p.charged_moves)
        lines += [
            f"{i}. {p.name} [{role_str}]",
            f"   Tipos: {'/'.join(p.types)}",
            f"   IVs: {p.ivs.attack}/{p.ivs.defense}/{p.ivs.hp} | Nivel: {p.level}",
            f"   Fast: {fm.name if fm else 'N/A'} | Charged: {charged}",
            "",
        ]
    return "\n".join(lines)
