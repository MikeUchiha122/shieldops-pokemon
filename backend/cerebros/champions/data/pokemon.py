"""
cerebros/champions/data/pokemon.py
Catálogo Pokémon Champions — formato Singles competitivo multi-generación.

Pokémon Champions es un juego de batallas competitivas con acceso a Pokémon
de todas las generaciones. Formato Singles (1v1 en campo), equipos de 6.
Sin Terastalization, sin Mega Evolution, sin Dynamax — mecánica Champions propia.
Tabla de tipos: estándar Gen IX (×2.0 / ×0.5 / ×0.0).
Habilidades activas. EVs/IVs/Naturaleza igual que serie principal.
"""
from __future__ import annotations
from core.types import TipoElemental, efectividad_base


def efectividad_champions(tipo_ataque: str, tipos_defensor: list[str]) -> float:
    """
    Tabla de tipos Champions — multiplicadores estándar Gen IX.
    ×2.0 supereficaz | ×0.5 poco eficaz | ×0.0 sin efecto
    Mismos valores que la serie principal. Habilidades pueden modificarlos.
    """
    mult = 1.0
    for t in tipos_defensor:
        mult *= efectividad_base(TipoElemental(tipo_ataque), TipoElemental(t))
    return mult


POKEMON_CHAMPIONS: dict[str, dict] = {

    # ── TIER S — Los más dominantes del meta Champions ────────────────────────
    "flutter_mane_ch": {
        "nombre": "Flutter Mane",
        "tipos": ["fantasma", "hada"],
        "stats": {"hp": 55, "atq_fis": 55, "def_fis": 55, "atq_esp": 135, "def_esp": 135, "vel": 135},
        "habilidades": ["protosintesis"],
        "habilidad_oculta": None,
        "movimientos": [
            "confusion_lunar", "brillo_magico", "voz_cautivadora", "sombra_ball",
            "campo_de_hadas", "pantalla_de_luz", "reflejo", "truco", "proteccion",
        ],
        "peso_kg": 4.0, "tier": "S", "generacion": 9,
    },
    "iron_bundle_ch": {
        "nombre": "Iron Bundle",
        "tipos": ["hielo", "agua"],
        "stats": {"hp": 56, "atq_fis": 80, "def_fis": 114, "atq_esp": 124, "def_esp": 60, "vel": 136},
        "habilidades": ["propulsion_cuantica"],
        "habilidad_oculta": None,
        "movimientos": [
            "canto_helado", "hidrobomba", "surf", "ventisca", "rayo_hielo",
            "rayo", "proteccion", "aguante",
        ],
        "peso_kg": 10.5, "tier": "S", "generacion": 9,
    },
    "landorus_therian_ch": {
        "nombre": "Landorus-Tótem",
        "tipos": ["tierra", "volador"],
        "stats": {"hp": 89, "atq_fis": 145, "def_fis": 90, "atq_esp": 105, "def_esp": 80, "vel": 91},
        "habilidades": ["intimidacion"],
        "habilidad_oculta": None,
        "movimientos": [
            "terremoto", "roca_afilada", "bofeton_lodo", "vendaval",
            "acrobacia", "danza_espada", "proteccion", "ida_y_vuelta",
        ],
        "peso_kg": 68.0, "tier": "S", "generacion": 5,
    },
    "heatran_ch": {
        "nombre": "Heatran",
        "tipos": ["fuego", "acero"],
        "stats": {"hp": 91, "atq_fis": 90, "def_fis": 106, "atq_esp": 130, "def_esp": 106, "vel": 77},
        "habilidades": ["volcan"],
        "habilidad_oculta": None,
        "movimientos": [
            "llamarada", "lanzallamas", "flash_cannon", "bola_tierra",
            "campo_electrico", "tormenta_de_arena", "proteccion", "descanso",
        ],
        "peso_kg": 430.0, "tier": "S", "generacion": 4,
    },
    "toxapex_ch": {
        "nombre": "Toxapex",
        "tipos": ["agua", "veneno"],
        "stats": {"hp": 50, "atq_fis": 63, "def_fis": 152, "atq_esp": 53, "def_esp": 142, "vel": 35},
        "habilidades": ["regeneracion", "bayoneta"],
        "habilidad_oculta": "toxicidad",
        "movimientos": [
            "ola_acida", "puas_toxicas", "recuperacion", "neblina",
            "oleaje_oscuro", "acua_jet", "proteccion",
        ],
        "peso_kg": 14.5, "tier": "S", "generacion": 7,
    },
    "dragapult_ch": {
        "nombre": "Dragapult",
        "tipos": ["dragon", "fantasma"],
        "stats": {"hp": 88, "atq_fis": 120, "def_fis": 75, "atq_esp": 100, "def_esp": 75, "vel": 142},
        "habilidades": ["transparen", "infiltrador"],
        "habilidad_oculta": "cursor",
        "movimientos": [
            "pulso_dragon", "sombra_ball", "garra_dragon", "puño_sombra",
            "golpe_bajo", "vendaval", "danza_dragon", "proteccion",
        ],
        "peso_kg": 50.0, "tier": "S", "generacion": 8,
    },
    "cinderace_ch": {
        "nombre": "Cinderace",
        "tipos": ["fuego"],
        "stats": {"hp": 80, "atq_fis": 116, "def_fis": 75, "atq_esp": 65, "def_esp": 75, "vel": 119},
        "habilidades": ["libero"],
        "habilidad_oculta": None,
        "movimientos": [
            "bola_fuego", "patada_igneo", "acua_jet", "ida_y_vuelta",
            "velocidad_extrema", "roca_afilada", "danza_espada", "proteccion",
        ],
        "peso_kg": 33.0, "tier": "S", "generacion": 8,
    },
    "rillaboom_ch": {
        "nombre": "Rillaboom",
        "tipos": ["planta"],
        "stats": {"hp": 100, "atq_fis": 125, "def_fis": 90, "atq_esp": 60, "def_esp": 70, "vel": 85},
        "habilidades": ["zona_de_hierba"],
        "habilidad_oculta": None,
        "movimientos": [
            "tamborileo", "golpe_hierba", "terremoto", "acua_tail",
            "ida_y_vuelta", "danza_espada", "proteccion",
        ],
        "peso_kg": 90.0, "tier": "S", "generacion": 8,
    },

    # ── TIER A — Muy usados y efectivos ──────────────────────────────────────
    "garchomp_ch": {
        "nombre": "Garchomp",
        "tipos": ["dragon", "tierra"],
        "stats": {"hp": 108, "atq_fis": 130, "def_fis": 95, "atq_esp": 80, "def_esp": 85, "vel": 102},
        "habilidades": ["piel_arenosa", "arena_escudo"],
        "habilidad_oculta": "piel_tosca",
        "movimientos": [
            "terremoto", "garra_dragon", "draco_meteoro", "roca_afilada",
            "bofeton_lodo", "danza_espada", "danza_dragon", "proteccion",
        ],
        "peso_kg": 95.0, "tier": "A", "generacion": 4,
    },
    "urshifu_single_ch": {
        "nombre": "Urshifu-Golpe Único",
        "tipos": ["lucha", "siniestro"],
        "stats": {"hp": 100, "atq_fis": 130, "def_fis": 100, "atq_esp": 63, "def_esp": 60, "vel": 97},
        "habilidades": ["puno_fantasma"],
        "habilidad_oculta": None,
        "movimientos": [
            "golpe_maestro", "a_bocajarro", "acua_tail", "terremoto",
            "puño_hielo", "danza_espada", "proteccion",
        ],
        "peso_kg": 105.0, "tier": "A", "generacion": 8,
    },
    "volcarona_ch": {
        "nombre": "Volcarona",
        "tipos": ["bicho", "fuego"],
        "stats": {"hp": 85, "atq_fis": 60, "def_fis": 65, "atq_esp": 135, "def_esp": 105, "vel": 100},
        "habilidades": ["manto_llama"],
        "habilidad_oculta": "clorofila",
        "movimientos": [
            "danza_llama", "lanzallamas", "llamarada", "energibola",
            "psicorrayo", "antena", "proteccion",
        ],
        "peso_kg": 46.0, "tier": "A", "generacion": 5,
    },
    "tyranitar_ch": {
        "nombre": "Tyranitar",
        "tipos": ["roca", "siniestro"],
        "stats": {"hp": 100, "atq_fis": 134, "def_fis": 110, "atq_esp": 95, "def_esp": 100, "vel": 61},
        "habilidades": ["arena_activada"],
        "habilidad_oculta": "presion",
        "movimientos": [
            "roca_afilada", "terremoto", "envite_feroz", "cascada",
            "puño_hielo", "avalancha", "danza_espada", "proteccion",
        ],
        "peso_kg": 202.0, "tier": "A", "generacion": 2,
    },
    "clefable_ch": {
        "nombre": "Clefable",
        "tipos": ["hada"],
        "stats": {"hp": 95, "atq_fis": 70, "def_fis": 73, "atq_esp": 95, "def_esp": 90, "vel": 60},
        "habilidades": ["cuerpo_magico"],
        "habilidad_oculta": "levitacion",
        "movimientos": [
            "campo_de_hadas", "brillo_magico", "voz_cautivadora", "confusion_lunar",
            "pantalla_de_luz", "reflejo", "luz_lunar", "proteccion",
        ],
        "peso_kg": 40.0, "tier": "A", "generacion": 1,
    },
    "kyurem_black_ch": {
        "nombre": "Kyurem-Negro",
        "tipos": ["dragon", "hielo"],
        "stats": {"hp": 125, "atq_fis": 170, "def_fis": 100, "atq_esp": 120, "def_esp": 90, "vel": 95},
        "habilidades": ["turboblaze"],
        "habilidad_oculta": None,
        "movimientos": [
            "cabezazo_hielo", "draco_meteoro", "terremoto", "puño_trueno",
            "avalancha", "danza_espada", "proteccion",
        ],
        "peso_kg": 325.0, "tier": "A", "generacion": 5,
    },
    "zamazenta_hero_ch": {
        "nombre": "Zamazenta",
        "tipos": ["lucha"],
        "stats": {"hp": 92, "atq_fis": 130, "def_fis": 115, "atq_esp": 80, "def_esp": 115, "vel": 138},
        "habilidades": ["presion"],
        "habilidad_oculta": None,
        "movimientos": [
            "a_bocajarro", "terremoto", "cabeza_hierro", "velocidad_extrema",
            "roca_afilada", "avalancha", "proteccion",
        ],
        "peso_kg": 210.0, "tier": "A", "generacion": 8,
    },
    "palafin_hero_ch": {
        "nombre": "Palafin-Héroe",
        "tipos": ["agua"],
        "stats": {"hp": 100, "atq_fis": 160, "def_fis": 97, "atq_esp": 106, "def_esp": 87, "vel": 100},
        "habilidades": ["cero_a_heroe"],
        "habilidad_oculta": None,
        "movimientos": [
            "cascada", "acua_jet", "a_bocajarro", "puño_hielo",
            "velocidad_extrema", "danza_espada", "proteccion",
        ],
        "peso_kg": 97.4, "tier": "A", "generacion": 9,
    },
    "roaring_moon_ch": {
        "nombre": "Roaring Moon",
        "tipos": ["dragon", "siniestro"],
        "stats": {"hp": 105, "atq_fis": 139, "def_fis": 71, "atq_esp": 55, "def_esp": 71, "vel": 119},
        "habilidades": ["protosintesis"],
        "habilidad_oculta": None,
        "movimientos": [
            "danza_dragon", "garra_dragon", "envite_feroz", "terremoto",
            "puño_hielo", "danza_espada", "proteccion",
        ],
        "peso_kg": 380.0, "tier": "A", "generacion": 9,
    },

    # ── TIER B — Usados situacionalmente ─────────────────────────────────────
    "blissey_ch": {
        "nombre": "Blissey",
        "tipos": ["normal"],
        "stats": {"hp": 255, "atq_fis": 10, "def_fis": 10, "atq_esp": 75, "def_esp": 135, "vel": 55},
        "habilidades": ["espiritu_vital", "sereno_gracia"],
        "habilidad_oculta": "suerte",
        "movimientos": [
            "psicorrayo", "luz_lunar", "pantalla_de_luz", "reflejo",
            "descanso", "neblina", "trueno", "proteccion",
        ],
        "peso_kg": 46.8, "tier": "B", "generacion": 2,
    },
    "scizor_ch": {
        "nombre": "Scizor",
        "tipos": ["bicho", "acero"],
        "stats": {"hp": 70, "atq_fis": 130, "def_fis": 100, "atq_esp": 55, "def_esp": 80, "vel": 65},
        "habilidades": ["torque_tecnologico"],
        "habilidad_oculta": "ligereza",
        "movimientos": [
            "tijera_x", "puño_bala", "acrobacia", "velocidad_extrema",
            "golpe_bis", "danza_espada", "proteccion",
        ],
        "peso_kg": 118.0, "tier": "B", "generacion": 2,
    },
    "slowking_galar_ch": {
        "nombre": "Slowking de Galar",
        "tipos": ["veneno", "psiquico"],
        "stats": {"hp": 95, "atq_fis": 65, "def_fis": 80, "atq_esp": 110, "def_esp": 110, "vel": 30},
        "habilidades": ["baba_venenosa", "regeneracion"],
        "habilidad_oculta": "presagiooscuro",
        "movimientos": [
            "psicorrayo", "ola_acida", "descanso", "puas_toxicas",
            "campo_psiquico", "neblina", "proteccion",
        ],
        "peso_kg": 79.5, "tier": "B", "generacion": 8,
    },
    "iron_valiant_ch": {
        "nombre": "Iron Valiant",
        "tipos": ["hada", "lucha"],
        "stats": {"hp": 74, "atq_fis": 130, "def_fis": 90, "atq_esp": 120, "def_esp": 60, "vel": 116},
        "habilidades": ["propulsion_cuantica"],
        "habilidad_oculta": None,
        "movimientos": [
            "brillo_magico", "a_bocajarro", "tijera_x", "sombra_ball",
            "campo_de_hadas", "danza_espada", "proteccion",
        ],
        "peso_kg": 35.0, "tier": "B", "generacion": 9,
    },
    "ting_lu_ch": {
        "nombre": "Ting-Lu",
        "tipos": ["siniestro", "tierra"],
        "stats": {"hp": 155, "atq_fis": 110, "def_fis": 75, "atq_esp": 55, "def_esp": 69, "vel": 45},
        "habilidades": ["vasija_de_ruina"],
        "habilidad_oculta": None,
        "movimientos": [
            "terremoto", "envite_feroz", "puas_toxicas", "cantotembloroso",
            "avalancha", "descanso", "proteccion",
        ],
        "peso_kg": 699.7, "tier": "B", "generacion": 9,
    },
    "mewtwo_ch": {
        "nombre": "Mewtwo",
        "tipos": ["psiquico"],
        "stats": {"hp": 106, "atq_fis": 110, "def_fis": 90, "atq_esp": 154, "def_esp": 90, "vel": 130},
        "habilidades": ["presion"],
        "habilidad_oculta": None,
        "movimientos": [
            "psicorrayo", "sombra_ball", "lanzamiento_magico", "rayo",
            "foco_blast", "recuperacion", "proteccion",
        ],
        "peso_kg": 122.0, "tier": "S", "generacion": 1,
    },
}


def buscar_pokemon_champions(nombre: str) -> dict | None:
    # Normalizar: agregar sufijo _ch o buscar por nombre
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    if key in POKEMON_CHAMPIONS:
        return POKEMON_CHAMPIONS[key]
    # Buscar sin sufijo _ch
    key_ch = key + "_ch"
    if key_ch in POKEMON_CHAMPIONS:
        return POKEMON_CHAMPIONS[key_ch]
    # Buscar por nombre exacto
    for v in POKEMON_CHAMPIONS.values():
        if v["nombre"].lower() == nombre.lower():
            return v
    return None


def listar_pokemon_champions() -> list[str]:
    return [v["nombre"] for v in POKEMON_CHAMPIONS.values()]


def listar_por_tier_champions(tier: str) -> list[str]:
    return [v["nombre"] for v in POKEMON_CHAMPIONS.values() if v.get("tier") == tier.upper()]
