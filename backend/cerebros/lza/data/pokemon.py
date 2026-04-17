"""
cerebros/lza/data/pokemon.py
Catálogo de Pokémon de Leyendas Z-A — Lumiose City / Kalos + confirmados.
Sistema Action Time: sin EVs/IVs/Naturaleza. Stats directos + Startup Frames + Cooldowns.
Mega Evolución disponible (1 por combate). Sin habilidades activas.
NO mezclar con EyP, GO ni Champions.

Tabla de tipos LZA: ×2.0 supereficaz / ×0.5 poco eficaz / ×0.0 sin efecto
(idéntica a la serie principal — Mega cambia tipos del Pokémon)
"""
from __future__ import annotations
from core.types import TipoElemental, efectividad_base


def efectividad_lza(tipo_ataque: str, tipos_defensor: list[str]) -> float:
    """
    Tabla de tipos LZA — mismos multiplicadores que la serie principal.
    LZA no modifica efectividades — SOLO considera cambios de tipo por Mega Evolución.
    Habilidades DESACTIVADAS: sin Levitación, sin Maravilla, etc.
    """
    mult = 1.0
    for t in tipos_defensor:
        mult *= efectividad_base(TipoElemental(tipo_ataque), TipoElemental(t))
    return mult


# ── Catálogo de Pokémon LZA ───────────────────────────────────────────────────
# stats = {hp, ataque, defensa, vel}  — sistema simplificado LZA (no EVs/IVs)
# startup_frames: frames antes de que el movimiento impacte (>12 = esquivable)
# cooldown_base_ms: milisegundos de espera tras ejecutar el movimiento
POKEMON_LZA: dict[str, dict] = {

    # ── STARTERS KANTO (confirmados en trailers LZA) ──────────────────────────
    "charizard": {
        "nombre": "Charizard",
        "tipos": ["fuego", "volador"],
        "stats": {"hp": 78, "ataque": 84, "defensa": 78, "vel": 100},
        "movimientos": ["ala_de_acero", "lanzallamas", "envite_igneo", "vendaval", "vuelo"],
        "startup_frames_principal": 8,
        "cooldown_base_ms": 1400,
        "puede_mega": True,
        "tipos_mega_x": ["fuego", "dragon"],
        "tipos_mega_y": ["fuego", "volador"],
        "stats_mega_x": {"hp": 78, "ataque": 130, "defensa": 111, "vel": 100},
        "stats_mega_y": {"hp": 78, "ataque": 104, "defensa": 78, "vel": 100},
    },
    "blastoise": {
        "nombre": "Blastoise",
        "tipos": ["agua"],
        "stats": {"hp": 79, "ataque": 83, "defensa": 100, "vel": 78},
        "movimientos": ["hidrobomba", "cascada", "surf", "acua_tail", "rayo_hielo"],
        "startup_frames_principal": 10,
        "cooldown_base_ms": 1500,
        "puede_mega": True,
        "tipos_mega": ["agua"],
        "stats_mega": {"hp": 79, "ataque": 103, "defensa": 120, "vel": 78},
    },
    "venusaur": {
        "nombre": "Venusaur",
        "tipos": ["planta", "veneno"],
        "stats": {"hp": 80, "ataque": 82, "defensa": 83, "vel": 80},
        "movimientos": ["tormenta_de_hojas", "energibola", "lanzamiento_lodo", "espora", "drenadoras"],
        "startup_frames_principal": 12,
        "cooldown_base_ms": 1600,
        "puede_mega": True,
        "tipos_mega": ["planta", "veneno"],
        "stats_mega": {"hp": 80, "ataque": 100, "defensa": 123, "vel": 80},
    },

    # ── LEGENDARIOS KANTO (confirmados) ──────────────────────────────────────
    "mewtwo": {
        "nombre": "Mewtwo",
        "tipos": ["psiquico"],
        "stats": {"hp": 106, "ataque": 110, "defensa": 90, "vel": 130},
        "movimientos": ["psicorrayo", "psiquico", "sombra_ball", "lanzamiento_magico", "rayo"],
        "startup_frames_principal": 6,
        "cooldown_base_ms": 1200,
        "puede_mega": True,
        "tipos_mega_x": ["psiquico", "lucha"],
        "tipos_mega_y": ["psiquico"],
        "stats_mega_x": {"hp": 106, "ataque": 190, "defensa": 100, "vel": 130},
        "stats_mega_y": {"hp": 106, "ataque": 150, "defensa": 90, "vel": 140},
    },

    # ── PSEUDO-LEGENDARIOS Y FUERTES ─────────────────────────────────────────
    "garchomp": {
        "nombre": "Garchomp",
        "tipos": ["dragon", "tierra"],
        "stats": {"hp": 108, "ataque": 130, "defensa": 95, "vel": 102},
        "movimientos": ["terremoto", "garra_dragon", "draco_meteoro", "roca_afilada", "bofeton_lodo"],
        "startup_frames_principal": 7,
        "cooldown_base_ms": 1300,
        "puede_mega": True,
        "tipos_mega": ["dragon", "tierra"],
        "stats_mega": {"hp": 108, "ataque": 170, "defensa": 115, "vel": 92},
    },
    "salamence": {
        "nombre": "Salamence",
        "tipos": ["dragon", "volador"],
        "stats": {"hp": 95, "ataque": 135, "defensa": 80, "vel": 100},
        "movimientos": ["draco_meteoro", "vendaval", "lanzallamas", "garra_dragon", "acrobacia"],
        "startup_frames_principal": 8,
        "cooldown_base_ms": 1350,
        "puede_mega": True,
        "tipos_mega": ["dragon", "volador"],
        "stats_mega": {"hp": 95, "ataque": 145, "defensa": 130, "vel": 120},
    },
    "metagross": {
        "nombre": "Metagross",
        "tipos": ["acero", "psiquico"],
        "stats": {"hp": 80, "ataque": 135, "defensa": 130, "vel": 70},
        "movimientos": ["cabeza_hierro", "psiquico", "terremoto", "puño_meteorico", "puño_bala"],
        "startup_frames_principal": 10,
        "cooldown_base_ms": 1600,
        "puede_mega": True,
        "tipos_mega": ["acero", "psiquico"],
        "stats_mega": {"hp": 80, "ataque": 145, "defensa": 150, "vel": 110},
    },
    "tyranitar": {
        "nombre": "Tyranitar",
        "tipos": ["roca", "siniestro"],
        "stats": {"hp": 100, "ataque": 134, "defensa": 110, "vel": 61},
        "movimientos": ["roca_afilada", "envite_feroz", "terremoto", "avalancha", "tormenta_arena"],
        "startup_frames_principal": 12,
        "cooldown_base_ms": 1700,
        "puede_mega": True,
        "tipos_mega": ["roca", "siniestro"],
        "stats_mega": {"hp": 100, "ataque": 164, "defensa": 150, "vel": 71},
    },
    "dragonite": {
        "nombre": "Dragonite",
        "tipos": ["dragon", "volador"],
        "stats": {"hp": 91, "ataque": 134, "defensa": 95, "vel": 80},
        "movimientos": ["draco_meteoro", "vendaval", "trueno", "velocidad_extrema", "garra_dragon"],
        "startup_frames_principal": 9,
        "cooldown_base_ms": 1450,
        "puede_mega": False,
    },

    # ── MEGA KALOS ────────────────────────────────────────────────────────────
    "lucario": {
        "nombre": "Lucario",
        "tipos": ["lucha", "acero"],
        "stats": {"hp": 70, "ataque": 110, "defensa": 70, "vel": 90},
        "movimientos": ["a_bocajarro", "puño_bala", "golpe_sombra", "psicorrayo", "rayo_oscuro"],
        "startup_frames_principal": 6,
        "cooldown_base_ms": 1100,
        "puede_mega": True,
        "tipos_mega": ["lucha", "acero"],
        "stats_mega": {"hp": 70, "ataque": 145, "defensa": 88, "vel": 112},
    },
    "gardevoir": {
        "nombre": "Gardevoir",
        "tipos": ["psiquico", "hada"],
        "stats": {"hp": 68, "ataque": 65, "defensa": 65, "vel": 80},
        "movimientos": ["psiquico", "psicorrayo", "brillo_magico", "confusion_lunar", "voz_cautivadora"],
        "startup_frames_principal": 9,
        "cooldown_base_ms": 1400,
        "puede_mega": True,
        "tipos_mega": ["psiquico", "hada"],
        "stats_mega": {"hp": 68, "ataque": 85, "defensa": 65, "vel": 100},
    },
    "gengar": {
        "nombre": "Gengar",
        "tipos": ["fantasma", "veneno"],
        "stats": {"hp": 60, "ataque": 65, "defensa": 60, "vel": 110},
        "movimientos": ["sombra_ball", "hex", "energibola", "lanzamiento_lodo", "psicorrayo"],
        "startup_frames_principal": 5,
        "cooldown_base_ms": 1000,
        "puede_mega": True,
        "tipos_mega": ["fantasma", "veneno"],
        "stats_mega": {"hp": 60, "ataque": 95, "defensa": 60, "vel": 130},
    },
    "alakazam": {
        "nombre": "Alakazam",
        "tipos": ["psiquico"],
        "stats": {"hp": 55, "ataque": 50, "defensa": 45, "vel": 120},
        "movimientos": ["psicorrayo", "psiquico", "foco_energia", "rayo", "sombra_ball"],
        "startup_frames_principal": 5,
        "cooldown_base_ms": 1000,
        "puede_mega": True,
        "tipos_mega": ["psiquico"],
        "stats_mega": {"hp": 55, "ataque": 50, "defensa": 65, "vel": 150},
    },
    "scizor": {
        "nombre": "Scizor",
        "tipos": ["bicho", "acero"],
        "stats": {"hp": 70, "ataque": 130, "defensa": 100, "vel": 65},
        "movimientos": ["tijera_x", "puño_bala", "acrobacia", "golpe_bis", "defensa_ferrea"],
        "startup_frames_principal": 8,
        "cooldown_base_ms": 1300,
        "puede_mega": True,
        "tipos_mega": ["bicho", "acero"],
        "stats_mega": {"hp": 70, "ataque": 150, "defensa": 140, "vel": 75},
    },
    "gyarados": {
        "nombre": "Gyarados",
        "tipos": ["agua", "volador"],
        "stats": {"hp": 95, "ataque": 125, "defensa": 79, "vel": 81},
        "movimientos": ["cascada", "acua_tail", "vendaval", "trueno", "terremoto"],
        "startup_frames_principal": 9,
        "cooldown_base_ms": 1400,
        "puede_mega": True,
        "tipos_mega": ["agua", "siniestro"],
        "stats_mega": {"hp": 95, "ataque": 155, "defensa": 109, "vel": 81},
    },
    "aerodactyl": {
        "nombre": "Aerodactyl",
        "tipos": ["roca", "volador"],
        "stats": {"hp": 80, "ataque": 105, "defensa": 65, "vel": 130},
        "movimientos": ["roca_afilada", "vendaval", "acrobacia", "terremoto", "golpe_bis"],
        "startup_frames_principal": 6,
        "cooldown_base_ms": 1100,
        "puede_mega": True,
        "tipos_mega": ["roca", "volador"],
        "stats_mega": {"hp": 80, "ataque": 135, "defensa": 85, "vel": 150},
    },
    "ampharos": {
        "nombre": "Ampharos",
        "tipos": ["electrico"],
        "stats": {"hp": 90, "ataque": 75, "defensa": 85, "vel": 55},
        "movimientos": ["trueno", "rayo", "campo_electrico", "pulso_dragon", "foco_energia"],
        "startup_frames_principal": 11,
        "cooldown_base_ms": 1600,
        "puede_mega": True,
        "tipos_mega": ["electrico", "dragon"],
        "stats_mega": {"hp": 90, "ataque": 95, "defensa": 105, "vel": 45},
    },
    "kangaskhan": {
        "nombre": "Kangaskhan",
        "tipos": ["normal"],
        "stats": {"hp": 105, "ataque": 95, "defensa": 80, "vel": 90},
        "movimientos": ["velocidad_extrema", "golpe_bis", "terremoto", "golpe_bello", "cuerpo_a_cuerpo"],
        "startup_frames_principal": 7,
        "cooldown_base_ms": 1250,
        "puede_mega": True,
        "tipos_mega": ["normal"],
        "stats_mega": {"hp": 105, "ataque": 125, "defensa": 100, "vel": 100},
    },
    "heracross": {
        "nombre": "Heracross",
        "tipos": ["bicho", "lucha"],
        "stats": {"hp": 80, "ataque": 125, "defensa": 75, "vel": 85},
        "movimientos": ["a_bocajarro", "tijera_x", "golpe_bis", "roca_afilada", "terremoto"],
        "startup_frames_principal": 9,
        "cooldown_base_ms": 1400,
        "puede_mega": True,
        "tipos_mega": ["bicho", "lucha"],
        "stats_mega": {"hp": 80, "ataque": 185, "defensa": 115, "vel": 75},
    },
    "houndoom": {
        "nombre": "Houndoom",
        "tipos": ["siniestro", "fuego"],
        "stats": {"hp": 75, "ataque": 90, "defensa": 50, "vel": 95},
        "movimientos": ["lanzallamas", "llamarada", "sombra_ball", "envite_feroz", "vendaval_ignito"],
        "startup_frames_principal": 7,
        "cooldown_base_ms": 1200,
        "puede_mega": True,
        "tipos_mega": ["siniestro", "fuego"],
        "stats_mega": {"hp": 75, "ataque": 90, "defensa": 90, "vel": 115},
    },
    "absol": {
        "nombre": "Absol",
        "tipos": ["siniestro"],
        "stats": {"hp": 65, "ataque": 130, "defensa": 60, "vel": 75},
        "movimientos": ["cuchillada", "envite_feroz", "golpe_bis", "psicorrayo", "danza_espada"],
        "startup_frames_principal": 7,
        "cooldown_base_ms": 1200,
        "puede_mega": True,
        "tipos_mega": ["siniestro"],
        "stats_mega": {"hp": 65, "ataque": 150, "defensa": 60, "vel": 115},
    },
    "aggron": {
        "nombre": "Aggron",
        "tipos": ["acero", "roca"],
        "stats": {"hp": 70, "ataque": 110, "defensa": 180, "vel": 50},
        "movimientos": ["cabeza_hierro", "roca_afilada", "terremoto", "avalancha", "defensa_ferrea"],
        "startup_frames_principal": 13,
        "cooldown_base_ms": 1800,
        "puede_mega": True,
        "tipos_mega": ["acero"],
        "stats_mega": {"hp": 70, "ataque": 140, "defensa": 230, "vel": 50},
    },

    # ── STARTERS KALOS ────────────────────────────────────────────────────────
    "greninja": {
        "nombre": "Greninja",
        "tipos": ["agua", "siniestro"],
        "stats": {"hp": 72, "ataque": 95, "defensa": 67, "vel": 122},
        "movimientos": ["acua_tail", "golpe_bajo", "surf", "sombra_ball", "tijera_x"],
        "startup_frames_principal": 5,
        "cooldown_base_ms": 1000,
        "puede_mega": False,
        "forma_especial": "bond_phenomenon",
    },
    "chesnaught": {
        "nombre": "Chesnaught",
        "tipos": ["planta", "lucha"],
        "stats": {"hp": 88, "ataque": 107, "defensa": 122, "vel": 64},
        "movimientos": ["golpe_hierba", "a_bocajarro", "puya_nociva", "avalancha", "drenadoras"],
        "startup_frames_principal": 11,
        "cooldown_base_ms": 1600,
        "puede_mega": False,
    },
    "delphox": {
        "nombre": "Delphox",
        "tipos": ["fuego", "psiquico"],
        "stats": {"hp": 75, "ataque": 69, "defensa": 72, "vel": 104},
        "movimientos": ["lanzallamas", "psicorrayo", "psiquico", "sombra_ball", "foco_energia"],
        "startup_frames_principal": 7,
        "cooldown_base_ms": 1200,
        "puede_mega": False,
    },

    # ── POKÉMON NATIVOS KALOS ─────────────────────────────────────────────────
    "sylveon": {
        "nombre": "Sylveon",
        "tipos": ["hada"],
        "stats": {"hp": 95, "ataque": 65, "defensa": 65, "vel": 60},
        "movimientos": ["brillo_magico", "voz_cautivadora", "confusion_lunar", "campo_de_hadas", "descanso"],
        "startup_frames_principal": 10,
        "cooldown_base_ms": 1500,
        "puede_mega": False,
    },
    "goodra": {
        "nombre": "Goodra",
        "tipos": ["dragon"],
        "stats": {"hp": 90, "ataque": 100, "defensa": 70, "vel": 80},
        "movimientos": ["draco_meteoro", "surf", "lanzamiento_lodo", "energibola", "trueno"],
        "startup_frames_principal": 10,
        "cooldown_base_ms": 1500,
        "puede_mega": False,
    },
    "talonflame": {
        "nombre": "Talonflame",
        "tipos": ["fuego", "volador"],
        "stats": {"hp": 78, "ataque": 81, "defensa": 71, "vel": 126},
        "movimientos": ["acrobacia", "envite_igneo", "vendaval", "lanzallamas", "acua_jet"],
        "startup_frames_principal": 6,
        "cooldown_base_ms": 1100,
        "puede_mega": False,
    },
    "tyrantrum": {
        "nombre": "Tyrantrum",
        "tipos": ["roca", "dragon"],
        "stats": {"hp": 82, "ataque": 121, "defensa": 119, "vel": 71},
        "movimientos": ["roca_afilada", "garra_dragon", "terremoto", "cabeza_hierro", "danza_dragon"],
        "startup_frames_principal": 10,
        "cooldown_base_ms": 1500,
        "puede_mega": False,
    },
    "aurorus": {
        "nombre": "Aurorus",
        "tipos": ["roca", "hielo"],
        "stats": {"hp": 123, "ataque": 77, "defensa": 72, "vel": 58},
        "movimientos": ["ventisca", "roca_afilada", "trueno", "neblina", "avalancha"],
        "startup_frames_principal": 12,
        "cooldown_base_ms": 1700,
        "puede_mega": False,
    },
    "togekiss": {
        "nombre": "Togekiss",
        "tipos": ["hada", "volador"],
        "stats": {"hp": 85, "ataque": 50, "defensa": 95, "vel": 80},
        "movimientos": ["brillo_magico", "vendaval", "psicorrayo", "campo_de_hadas", "neblina"],
        "startup_frames_principal": 9,
        "cooldown_base_ms": 1400,
        "puede_mega": False,
    },
    "florges": {
        "nombre": "Florges",
        "tipos": ["hada"],
        "stats": {"hp": 78, "ataque": 65, "defensa": 68, "vel": 75},
        "movimientos": ["brillo_magico", "confusion_lunar", "campo_de_hadas", "drenadoras", "neblina"],
        "startup_frames_principal": 10,
        "cooldown_base_ms": 1500,
        "puede_mega": False,
    },
    "gallade": {
        "nombre": "Gallade",
        "tipos": ["psiquico", "lucha"],
        "stats": {"hp": 68, "ataque": 125, "defensa": 65, "vel": 80},
        "movimientos": ["psicocarga", "a_bocajarro", "cuchillada", "golpe_bis", "danza_espada"],
        "startup_frames_principal": 7,
        "cooldown_base_ms": 1200,
        "puede_mega": True,
        "tipos_mega": ["psiquico", "lucha"],
        "stats_mega": {"hp": 68, "ataque": 165, "defensa": 95, "vel": 110},
    },
    "diancie": {
        "nombre": "Diancie",
        "tipos": ["roca", "hada"],
        "stats": {"hp": 50, "ataque": 100, "defensa": 150, "vel": 50},
        "movimientos": ["roca_afilada", "brillo_magico", "confusion_lunar", "avalancha", "campo_de_hadas"],
        "startup_frames_principal": 11,
        "cooldown_base_ms": 1600,
        "puede_mega": True,
        "tipos_mega": ["roca", "hada"],
        "stats_mega": {"hp": 50, "ataque": 160, "defensa": 110, "vel": 110},
    },
}


def buscar_pokemon_lza(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return POKEMON_LZA.get(key)


def listar_pokemon_lza() -> list[str]:
    return [v["nombre"] for v in POKEMON_LZA.values()]


def listar_con_mega_lza() -> list[str]:
    return [v["nombre"] for v in POKEMON_LZA.values() if v.get("puede_mega")]
