"""
cerebros/go/data/pokemon.py
Catálogo de Pokémon competitivos en Pokémon GO — GO Battle League.

IMPORTANTE: Los stats GO son COMPLETAMENTE DISTINTOS a la serie principal.
  - Stats GO: Ataque / Defensa / Resistencia (Stamina/HP) — escala diferente
  - IVs: 0-15 (no 0-31)
  - Sin naturaleza, sin EVs
  - STAB GO: ×1.2 (no ×1.5)
  - Supereficaz GO: ×1.6 (no ×2.0)
  - Poco eficaz GO: ×0.625 (no ×0.5)
  - Sin efecto GO: ×0.391 (no ×0.0 — no hay inmunidades reales en GO)
  - Sin habilidades (no existen en GO)
  - Sin objetos retenidos (no existen en GO)

Ligas:
  - Great League: CP ≤ 1500
  - Ultra League: CP ≤ 2500
  - Master League: sin límite de CP

Pokémon Shadow: Ataque ×1.2, Defensa ×0.833
"""
from __future__ import annotations
from core.types import TipoElemental, efectividad_base


# ── Tabla de tipos GO — multiplicadores Niantic ───────────────────────────────
# CRÍTICO: GO NO tiene ×2.0/×0.5/×0.0. Usa sus propios valores.
def efectividad_go(tipo_ataque: str, tipos_defensor: list[str]) -> float:
    """
    Tabla de tipos Pokémon GO — multiplicadores Niantic.
    ×1.6 supereficaz | ×0.625 poco eficaz | ×0.391 'sin efecto' (no es 0 real)
    Doble SE: ×2.56 | Doble NVE: ×0.391
    """
    mult = 1.0
    for t in tipos_defensor:
        base = efectividad_base(TipoElemental(tipo_ataque), TipoElemental(t))
        if base == 2.0:
            mult *= 1.6
        elif base == 0.5:
            mult *= 0.625
        elif base == 0.0:
            mult *= 0.391   # GO no tiene inmunidades reales
        # base 1.0 → no cambia
    return round(mult, 4)


# ── Stats GO oficiales (Ataque/Defensa/Resistencia) ──────────────────────────
# ATENCIÓN: Escala completamente distinta de la serie principal.
# Fuente: datos Niantic oficiales
POKEMON_GO: dict[str, dict] = {

    # ── GREAT LEAGUE TIER S (CP ≤ 1500) ─────────────────────────────────────
    "galarian_stunfisk": {
        "nombre": "Galarian Stunfisk",
        "tipos": ["tierra", "acero"],
        "stats_go": {"ataque": 144, "defensa": 182, "resistencia": 198},
        "fast_moves": ["barro", "puño_de_acero"],
        "charged_moves": ["avalancha", "bloqueo_de_roca", "puño_de_acero"],
        "ligas": ["great"],
        "shadow": False,
    },
    "medicham": {
        "nombre": "Medicham",
        "tipos": ["lucha", "psiquico"],
        "stats_go": {"ataque": 121, "defensa": 152, "resistencia": 155},
        "fast_moves": ["contraataque", "psico_corte"],
        "charged_moves": ["golpe_dinamico", "gelido", "bola_hielo_prioridad"],
        "ligas": ["great"],
        "shadow": False,
    },
    "registeel": {
        "nombre": "Registeel",
        "tipos": ["acero"],
        "stats_go": {"ataque": 143, "defensa": 285, "resistencia": 190},
        "fast_moves": ["candado_frente", "carga_metal"],
        "charged_moves": ["foco_blast", "flash_cannon", "hiperrayo"],
        "ligas": ["great", "ultra"],
        "shadow": False,
    },
    "azumarill": {
        "nombre": "Azumarill",
        "tipos": ["agua", "hada"],
        "stats_go": {"ataque": 112, "defensa": 152, "resistencia": 225},
        "fast_moves": ["burbuja", "puas_veneno"],
        "charged_moves": ["hidrobomba", "juego_sucio", "ice_beam"],
        "ligas": ["great"],
        "shadow": False,
    },
    "walrein": {
        "nombre": "Walrein",
        "tipos": ["hielo", "agua"],
        "stats_go": {"ataque": 182, "defensa": 176, "resistencia": 220},
        "fast_moves": ["puas_hielo", "pistola_agua"],
        "charged_moves": ["brecha_glacial", "avalancha", "salmuera"],
        "ligas": ["great", "ultra"],
        "shadow": False,
    },
    "talonflame": {
        "nombre": "Talonflame",
        "tipos": ["fuego", "volador"],
        "stats_go": {"ataque": 176, "defensa": 155, "resistencia": 186},
        "fast_moves": ["ala_de_acero", "fuego_rapido"],
        "charged_moves": ["fuego_acrobacia", "llamarada", "voltereta"],
        "ligas": ["great"],
        "shadow": False,
    },
    "swampert": {
        "nombre": "Swampert",
        "tipos": ["agua", "tierra"],
        "stats_go": {"ataque": 208, "defensa": 175, "resistencia": 225},
        "fast_moves": ["pistola_agua", "barro"],
        "charged_moves": ["cannon_hidro", "avalancha", "terremoto"],
        "ligas": ["great", "ultra", "master"],
        "shadow": False,
    },
    "bastiodon": {
        "nombre": "Bastiodon",
        "tipos": ["roca", "acero"],
        "stats_go": {"ataque": 94, "defensa": 286, "resistencia": 155},
        "fast_moves": ["carga_metal", "pisoteo"],
        "charged_moves": ["bloqueo_de_roca", "flash_cannon", "aguante"],
        "ligas": ["great"],
        "shadow": False,
    },
    "lanturn": {
        "nombre": "Lanturn",
        "tipos": ["agua", "electrico"],
        "stats_go": {"ataque": 146, "defensa": 136, "resistencia": 268},
        "fast_moves": ["pistola_agua", "chispa"],
        "charged_moves": ["surf", "trueno_bola", "ice_beam"],
        "ligas": ["great"],
        "shadow": False,
    },
    "shadow_swampert": {
        "nombre": "Shadow Swampert",
        "tipos": ["agua", "tierra"],
        "stats_go": {"ataque": 208, "defensa": 175, "resistencia": 225},
        "fast_moves": ["pistola_agua", "barro"],
        "charged_moves": ["cannon_hidro", "avalancha", "terremoto"],
        "ligas": ["great", "ultra", "master"],
        "shadow": True,
    },

    # ── ULTRA LEAGUE TIER S (CP ≤ 2500) ─────────────────────────────────────
    "cresselia": {
        "nombre": "Cresselia",
        "tipos": ["psiquico"],
        "stats_go": {"ataque": 152, "defensa": 258, "resistencia": 260},
        "fast_moves": ["psico_corte", "confusión"],
        "charged_moves": ["luna_bola", "aurora_viga", "futuro_ojo"],
        "ligas": ["ultra"],
        "shadow": False,
    },
    "obstagoon": {
        "nombre": "Obstagoon",
        "tipos": ["siniestro", "normal"],
        "stats_go": {"ataque": 190, "defensa": 185, "resistencia": 225},
        "fast_moves": ["rastreo", "contador"],
        "charged_moves": ["crunch", "crush_claw", "hiperrayo"],
        "ligas": ["ultra"],
        "shadow": False,
    },
    "alolan_muk": {
        "nombre": "Alolan Muk",
        "tipos": ["veneno", "siniestro"],
        "stats_go": {"ataque": 190, "defensa": 172, "resistencia": 210},
        "fast_moves": ["acido", "mordisco"],
        "charged_moves": ["crunch", "bomba_lodo", "tormenta_oscura"],
        "ligas": ["ultra"],
        "shadow": False,
    },
    "trevenant": {
        "nombre": "Trevenant",
        "tipos": ["fantasma", "planta"],
        "stats_go": {"ataque": 201, "defensa": 154, "resistencia": 198},
        "fast_moves": ["sombra_garrazo", "embrollo"],
        "charged_moves": ["drenadoras_cargado", "bola_sombra", "avalancha"],
        "ligas": ["ultra"],
        "shadow": False,
    },
    "jellicent": {
        "nombre": "Jellicent",
        "tipos": ["agua", "fantasma"],
        "stats_go": {"ataque": 159, "defensa": 178, "resistencia": 225},
        "fast_moves": ["burbuja", "hex"],
        "charged_moves": ["bola_sombra", "surf", "burbuja_bomba"],
        "ligas": ["ultra"],
        "shadow": False,
    },
    "giratina_altered": {
        "nombre": "Giratina-Alternativo",
        "tipos": ["fantasma", "dragon"],
        "stats_go": {"ataque": 187, "defensa": 225, "resistencia": 284},
        "fast_moves": ["sombra_garrazo", "dragon_breath"],
        "charged_moves": ["zancada_sombra", "garra_dragon", "bola_sombra"],
        "ligas": ["ultra", "master"],
        "shadow": False,
    },

    # ── MASTER LEAGUE TIER S (sin límite CP) ─────────────────────────────────
    "zacian": {
        "nombre": "Zacian",
        "tipos": ["hada"],
        "stats_go": {"ataque": 254, "defensa": 216, "resistencia": 192},
        "fast_moves": ["mordisco", "ráfaga_acero"],
        "charged_moves": ["juego_sucio", "hoja_espada", "cierre"],
        "ligas": ["master"],
        "shadow": False,
    },
    "kyogre": {
        "nombre": "Kyogre",
        "tipos": ["agua"],
        "stats_go": {"ataque": 270, "defensa": 228, "resistencia": 205},
        "fast_moves": ["cascada", "pistola_agua"],
        "charged_moves": ["hidrobomba_origen", "trueno", "glacial_lanza"],
        "ligas": ["master"],
        "shadow": False,
    },
    "groudon": {
        "nombre": "Groudon",
        "tipos": ["tierra"],
        "stats_go": {"ataque": 270, "defensa": 228, "resistencia": 205},
        "fast_moves": ["barro", "cola_dragon"],
        "charged_moves": ["fisura_origen", "terremoto", "fuego_lanzamiento"],
        "ligas": ["master"],
        "shadow": False,
    },
    "dialga": {
        "nombre": "Dialga",
        "tipos": ["acero", "dragon"],
        "stats_go": {"ataque": 275, "defensa": 211, "resistencia": 205},
        "fast_moves": ["aliento_dragon", "carga_metal"],
        "charged_moves": ["aullido_temporal", "flash_cannon", "trueno"],
        "ligas": ["master"],
        "shadow": False,
    },
    "palkia": {
        "nombre": "Palkia",
        "tipos": ["agua", "dragon"],
        "stats_go": {"ataque": 280, "defensa": 215, "resistencia": 189},
        "fast_moves": ["aliento_dragon", "pistola_agua"],
        "charged_moves": ["rugido_espacial", "hidrobomba", "laser_dragon"],
        "ligas": ["master"],
        "shadow": False,
    },
    "mewtwo": {
        "nombre": "Mewtwo",
        "tipos": ["psiquico"],
        "stats_go": {"ataque": 300, "defensa": 182, "resistencia": 214},
        "fast_moves": ["confusion", "psico_corte"],
        "charged_moves": ["psicorayo_cargado", "bola_sombra", "foco_blast"],
        "ligas": ["master"],
        "shadow": False,
    },
    "shadow_mewtwo": {
        "nombre": "Shadow Mewtwo",
        "tipos": ["psiquico"],
        "stats_go": {"ataque": 300, "defensa": 182, "resistencia": 214},
        "fast_moves": ["confusion", "psico_corte"],
        "charged_moves": ["psicorayo_cargado", "bola_sombra", "foco_blast"],
        "ligas": ["master"],
        "shadow": True,
    },
    "eternatus": {
        "nombre": "Eternatus",
        "tipos": ["veneno", "dragon"],
        "stats_go": {"ataque": 278, "defensa": 200, "resistencia": 220},
        "fast_moves": ["llamarada_eterna", "cola_dragon"],
        "charged_moves": ["tormenta_veneno", "laser_dragon", "llama_infernal"],
        "ligas": ["master"],
        "shadow": False,
    },
    "garchomp": {
        "nombre": "Garchomp",
        "tipos": ["dragon", "tierra"],
        "stats_go": {"ataque": 261, "defensa": 193, "resistencia": 239},
        "fast_moves": ["fango", "cola_dragon"],
        "charged_moves": ["terremoto", "garra_dragon_cargado", "bola_de_lodo"],
        "ligas": ["master"],
        "shadow": False,
    },
    "dragonite": {
        "nombre": "Dragonite",
        "tipos": ["dragon", "volador"],
        "stats_go": {"ataque": 263, "defensa": 198, "resistencia": 209},
        "fast_moves": ["aliento_dragon", "ala_de_acero"],
        "charged_moves": ["laser_dragon", "huracan", "super_movimiento"],
        "ligas": ["master"],
        "shadow": False,
    },
    "togekiss": {
        "nombre": "Togekiss",
        "tipos": ["hada", "volador"],
        "stats_go": {"ataque": 225, "defensa": 217, "resistencia": 198},
        "fast_moves": ["encanto", "golpe_aereo"],
        "charged_moves": ["deslumbrante", "poder_antiguo", "fuego_helado"],
        "ligas": ["master", "ultra"],
        "shadow": False,
    },
    "giratina_origin": {
        "nombre": "Giratina-Origen",
        "tipos": ["fantasma", "dragon"],
        "stats_go": {"ataque": 225, "defensa": 187, "resistencia": 284},
        "fast_moves": ["sombra_garrazo", "aliento_dragon"],
        "charged_moves": ["bola_sombra", "onirico", "laser_dragon"],
        "ligas": ["master"],
        "shadow": False,
    },
    "lugia": {
        "nombre": "Lugia",
        "tipos": ["psiquico", "volador"],
        "stats_go": {"ataque": 193, "defensa": 310, "resistencia": 235},
        "fast_moves": ["dragón_cola", "extrasensorial"],
        "charged_moves": ["aeroballista", "futuro_ojo", "ciclón"],
        "ligas": ["master"],
        "shadow": False,
    },

    # ── ALL-ROUNDER (multi-liga) ──────────────────────────────────────────────
    "shadow_chansey": {
        "nombre": "Shadow Chansey",
        "tipos": ["normal"],
        "stats_go": {"ataque": 60, "defensa": 128, "resistencia": 487},
        "fast_moves": ["zurra", "libra"],
        "charged_moves": ["deslumbrante", "psico_boost", "huevo_bomba"],
        "ligas": ["great", "ultra"],
        "shadow": True,
    },
    "umbreon": {
        "nombre": "Umbreon",
        "tipos": ["siniestro"],
        "stats_go": {"ataque": 126, "defensa": 240, "resistencia": 216},
        "fast_moves": ["snarl", "zurra"],
        "charged_moves": ["foul_play", "último_recurso", "magia_sombra"],
        "ligas": ["great", "ultra"],
        "shadow": False,
    },
}


def buscar_pokemon_go(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_").replace("é", "e").replace("ó", "o")
    return POKEMON_GO.get(key)


def listar_pokemon_go() -> list[str]:
    return [v["nombre"] for v in POKEMON_GO.values()]


def pokemon_go_por_liga(liga: str) -> list[str]:
    return [v["nombre"] for v in POKEMON_GO.values() if liga in v.get("ligas", [])]
