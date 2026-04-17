"""
cerebros/eyp/data/pokemon.py
Catálogo de Pokémon exclusivos de Escarlata y Púrpura (VGC 2026 Regulación G/H).
SOLO Pokémon de la Pokédex de Paldea + DLC Máscara Teal + Disco Índigo.
NO mezclar con LZA, GO ni Champions.

Stats base: HP / Atq_Fis / Def_Fis / Atq_Esp / Def_Esp / Vel
"""
from __future__ import annotations
from core.types import TipoElemental, efectividad_base

# ── Tabla de tipos con multiplicadores EyP (estándar serie principal) ──────────
# ×2.0 supereficaz | ×0.5 poco eficaz | ×0.0 sin efecto
def efectividad_eyp(tipo_ataque: str, tipos_defensor: list[str]) -> float:
    """Calcula multiplicador de tipo para EyP (Gen IX). Sin modificar valores base."""
    mult = 1.0
    for t in tipos_defensor:
        mult *= efectividad_base(TipoElemental(tipo_ataque), TipoElemental(t))
    return mult


# ── Catálogo de Pokémon EyP ────────────────────────────────────────────────────
# Formato: stats = {hp, atq_fis, def_fis, atq_esp, def_esp, vel}
POKEMON_EYP: dict[str, dict] = {

    # ── LEGENDARIOS RESTRINGIDOS (máx. 1 por equipo VGC Reg. G) ──────────────
    "miraidon": {
        "nombre": "Miraidon",
        "tipos": ["electrico", "dragon"],
        "stats": {"hp": 100, "atq_fis": 85, "def_fis": 100, "atq_esp": 135, "def_esp": 115, "vel": 135},
        "habilidades": ["motor_hadron"],
        "habilidad_oculta": None,
        "movimientos": [
            "voltio_cruel", "trueno", "rayo", "tormenta_electrica",
            "pulso_dragon", "draco_meteoro", "garra_dragon",
            "proteccion", "campo_electrico", "medidor_voltios",
            "puerta_dimensional", "viento_misterioso",
        ],
        "peso_kg": 240.0, "restringido": True, "paradoja": False,
    },
    "koraidon": {
        "nombre": "Koraidon",
        "tipos": ["lucha", "dragon"],
        "stats": {"hp": 100, "atq_fis": 135, "def_fis": 115, "atq_esp": 85, "def_esp": 100, "vel": 135},
        "habilidades": ["motor_orichalco"],
        "habilidad_oculta": None,
        "movimientos": [
            "ciclotorrente", "combate", "a_bocajarro", "patada_salto",
            "draco_meteoro", "garra_dragon", "pulso_dragon",
            "terremoto", "roca_afilada", "avalancha",
            "proteccion", "estoico", "danza_espada",
        ],
        "peso_kg": 303.0, "restringido": True, "paradoja": False,
    },
    "calyrex_shadow": {
        "nombre": "Calyrex-Espectral",
        "tipos": ["psiquico", "fantasma"],
        "stats": {"hp": 100, "atq_fis": 85, "def_fis": 80, "atq_esp": 165, "def_esp": 100, "vel": 150},
        "habilidades": ["jinete_espectral"],
        "habilidad_oculta": None,
        "movimientos": [
            "galopar_espectral", "psicocarga", "psicoataque", "poder_lunar",
            "sombra_ball", "rayo_umbrio", "premonicion",
            "proteccion", "descanso", "luz_lunar",
        ],
        "peso_kg": 53.6, "restringido": True, "paradoja": False,
    },
    "calyrex_ice": {
        "nombre": "Calyrex-Gélido",
        "tipos": ["psiquico", "hielo"],
        "stats": {"hp": 100, "atq_fis": 165, "def_fis": 150, "atq_esp": 85, "def_esp": 130, "vel": 50},
        "habilidades": ["jinete_gelido"],
        "habilidad_oculta": None,
        "movimientos": [
            "galopar_glacial", "cabezazo_hielo", "granizo", "avalancha",
            "psicocarga", "psicorrayo", "luz_lunar",
            "proteccion", "aguante", "roca_afilada",
        ],
        "peso_kg": 809.0, "restringido": True, "paradoja": False,
    },
    "zacian_crowned": {
        "nombre": "Zacian-Corona",
        "tipos": ["hada", "acero"],
        "stats": {"hp": 92, "atq_fis": 170, "def_fis": 115, "atq_esp": 80, "def_esp": 115, "vel": 148},
        "habilidades": ["espada_intrepida"],
        "habilidad_oculta": None,
        "movimientos": [
            "tajo_sagrado", "hoja_espada", "cabeza_hierro", "puño_meteorico",
            "a_bocajarro", "estoico", "danza_espada",
            "velocidad_extrema", "proteccion", "vendaval",
        ],
        "peso_kg": 355.0, "restringido": True, "paradoja": False,
    },
    "zamazenta_crowned": {
        "nombre": "Zamazenta-Corona",
        "tipos": ["lucha", "acero"],
        "stats": {"hp": 92, "atq_fis": 130, "def_fis": 145, "atq_esp": 80, "def_esp": 145, "vel": 128},
        "habilidades": ["escudo_intrepido"],
        "habilidad_oculta": None,
        "movimientos": [
            "defensa_ferrea", "a_bocajarro", "cabeza_hierro", "estoico",
            "terremoto", "avalancha", "aguante",
            "velocidad_extrema", "proteccion", "roca_afilada",
        ],
        "peso_kg": 785.0, "restringido": True, "paradoja": False,
    },
    "kyogre": {
        "nombre": "Kyogre",
        "tipos": ["agua"],
        "stats": {"hp": 100, "atq_fis": 100, "def_fis": 90, "atq_esp": 150, "def_esp": 140, "vel": 90},
        "habilidades": ["lluvia_primordial"],
        "habilidad_oculta": None,
        "movimientos": [
            "hidrobomba", "surf", "aguante_origen", "rayo_hielo",
            "trueno", "cascada", "proteccion",
            "ventisca", "ola_mental",
        ],
        "peso_kg": 352.0, "restringido": True, "paradoja": False,
    },
    "groudon": {
        "nombre": "Groudon",
        "tipos": ["tierra"],
        "stats": {"hp": 100, "atq_fis": 150, "def_fis": 140, "atq_esp": 100, "def_esp": 90, "vel": 90},
        "habilidades": ["sol_abrasador"],
        "habilidad_oculta": None,
        "movimientos": [
            "terremoto", "fisura_origen", "lanzallamas", "llamarada",
            "roca_afilada", "avalancha", "proteccion",
            "estocada_roca", "espada_solar",
        ],
        "peso_kg": 950.0, "restringido": True, "paradoja": False,
    },
    "eternatus": {
        "nombre": "Eternatus",
        "tipos": ["veneno", "dragon"],
        "stats": {"hp": 140, "atq_fis": 85, "def_fis": 95, "atq_esp": 145, "def_esp": 95, "vel": 130},
        "habilidades": ["presion"],
        "habilidad_oculta": None,
        "movimientos": [
            "llamarada_eterna", "draco_meteoro", "pulso_dragon", "sombra_ball",
            "llamarada", "lanzallamas", "ola_acida",
            "proteccion", "recuperacion",
        ],
        "peso_kg": 950.0, "restringido": True, "paradoja": False,
    },
    "xerneas": {
        "nombre": "Xerneas",
        "tipos": ["hada"],
        "stats": {"hp": 126, "atq_fis": 131, "def_fis": 95, "atq_esp": 131, "def_esp": 98, "vel": 99},
        "habilidades": ["ritmo_activo", "encanto_hada"],
        "habilidad_oculta": None,
        "movimientos": [
            "geomancia", "rayo_aurora", "brillo_magico", "voz_cautivadora",
            "campo_de_hadas", "fuerza_lunar", "proteccion",
            "pantalla_de_luz", "reflejo",
        ],
        "peso_kg": 215.0, "restringido": True, "paradoja": False,
    },
    "yveltal": {
        "nombre": "Yveltal",
        "tipos": ["siniestro", "volador"],
        "stats": {"hp": 126, "atq_fis": 131, "def_fis": 95, "atq_esp": 131, "def_esp": 98, "vel": 99},
        "habilidades": ["reapertura"],
        "habilidad_oculta": None,
        "movimientos": [
            "sifon_siniestro", "vendaval", "sombra_ball", "psicorrayo",
            "contragolpe", "espacio_extraño", "proteccion",
            "torbellino_oscuro",
        ],
        "peso_kg": 203.0, "restringido": True, "paradoja": False,
    },

    # ── PARADOJA FUTURO (Regulación G: permitidos) ────────────────────────────
    "flutter_mane": {
        "nombre": "Flutter Mane",
        "tipos": ["fantasma", "hada"],
        "stats": {"hp": 55, "atq_fis": 55, "def_fis": 55, "atq_esp": 135, "def_esp": 135, "vel": 135},
        "habilidades": ["protosintesis"],
        "habilidad_oculta": None,
        "movimientos": [
            "confusion_lunar", "poder_lunar", "brillo_magico", "voz_cautivadora",
            "sombra_ball", "rayo_umbrio", "hex", "premonicion",
            "campo_de_hadas", "pantalla_de_luz", "proteccion",
            "truco", "encanto",
        ],
        "peso_kg": 4.0, "restringido": False, "paradoja": True,
    },
    "iron_bundle": {
        "nombre": "Iron Bundle",
        "tipos": ["hielo", "agua"],
        "stats": {"hp": 56, "atq_fis": 80, "def_fis": 114, "atq_esp": 124, "def_esp": 60, "vel": 136},
        "habilidades": ["propulsion_cuantica"],
        "habilidad_oculta": None,
        "movimientos": [
            "canto_helado", "hidrobomba", "surf", "ventisca",
            "lanzamiento_hielo", "rayo_hielo", "rayo",
            "viento_hielo", "proteccion", "aguante",
        ],
        "peso_kg": 10.5, "restringido": False, "paradoja": True,
    },
    "roaring_moon": {
        "nombre": "Roaring Moon",
        "tipos": ["dragon", "siniestro"],
        "stats": {"hp": 105, "atq_fis": 139, "def_fis": 71, "atq_esp": 55, "def_esp": 71, "vel": 119},
        "habilidades": ["protosintesis"],
        "habilidad_oculta": None,
        "movimientos": [
            "danza_dragon", "garra_dragon", "envite_feroz",
            "terremoto", "puño_hielo", "acrobacia",
            "bofeton_lodo", "proteccion", "danza_espada",
        ],
        "peso_kg": 380.0, "restringido": False, "paradoja": True,
    },
    "iron_valiant": {
        "nombre": "Iron Valiant",
        "tipos": ["hada", "lucha"],
        "stats": {"hp": 74, "atq_fis": 130, "def_fis": 90, "atq_esp": 120, "def_esp": 60, "vel": 116},
        "habilidades": ["propulsion_cuantica"],
        "habilidad_oculta": None,
        "movimientos": [
            "campo_de_hadas", "brillo_magico", "a_bocajarro",
            "tijera_x", "acrobacia", "danza_espada",
            "sombra_ball", "voz_cautivadora", "proteccion",
        ],
        "peso_kg": 35.0, "restringido": False, "paradoja": True,
    },

    # ── BESTIAS DE LA RUINA ────────────────────────────────────────────────────
    "chi_yu": {
        "nombre": "Chi-Yu",
        "tipos": ["siniestro", "fuego"],
        "stats": {"hp": 55, "atq_fis": 80, "def_fis": 80, "atq_esp": 135, "def_esp": 120, "vel": 100},
        "habilidades": ["perlas_de_malicia"],
        "habilidad_oculta": None,
        "movimientos": [
            "llamarada_oscura", "vendaval_ignito", "lanzallamas", "llamarada",
            "sombra_ball", "rayo_umbrio", "proteccion", "truco",
            "hiperrayo_oscuro",
        ],
        "peso_kg": 4.9, "restringido": False, "paradoja": False,
    },
    "chien_pao": {
        "nombre": "Chien-Pao",
        "tipos": ["siniestro", "hielo"],
        "stats": {"hp": 80, "atq_fis": 120, "def_fis": 80, "atq_esp": 90, "def_esp": 65, "vel": 135},
        "habilidades": ["espada_de_ruina"],
        "habilidad_oculta": None,
        "movimientos": [
            "golpe_hielo", "cuchillada_helada", "envite_feroz",
            "terremoto", "avalancha", "defensa_ferrea",
            "danza_espada", "proteccion",
        ],
        "peso_kg": 152.2, "restringido": False, "paradoja": False,
    },
    "ting_lu": {
        "nombre": "Ting-Lu",
        "tipos": ["siniestro", "tierra"],
        "stats": {"hp": 155, "atq_fis": 110, "def_fis": 75, "atq_esp": 55, "def_esp": 69, "vel": 45},
        "habilidades": ["vasija_de_ruina"],
        "habilidad_oculta": None,
        "movimientos": [
            "terremoto", "fisura", "puas_toxicas", "avalancha",
            "envite_feroz", "cantotembloroso", "descanso",
            "proteccion",
        ],
        "peso_kg": 699.7, "restringido": False, "paradoja": False,
    },
    "wo_chien": {
        "nombre": "Wo-Chien",
        "tipos": ["siniestro", "planta"],
        "stats": {"hp": 85, "atq_fis": 85, "def_fis": 100, "atq_esp": 95, "def_esp": 135, "vel": 70},
        "habilidades": ["tablillas_de_ruina"],
        "habilidad_oculta": None,
        "movimientos": [
            "tormenta_de_hojas", "energibola", "sombra_ball",
            "neblina", "drenadoras", "pantalla_de_luz",
            "reflexo", "proteccion",
        ],
        "peso_kg": 74.2, "restringido": False, "paradoja": False,
    },

    # ── META VGC — APOYO Y OFENSIVOS ──────────────────────────────────────────
    "incineroar": {
        "nombre": "Incineroar",
        "tipos": ["fuego", "siniestro"],
        "stats": {"hp": 95, "atq_fis": 115, "def_fis": 90, "atq_esp": 80, "def_esp": 90, "vel": 60},
        "habilidades": ["intimidacion", "explosividad"],
        "habilidad_oculta": "presion",
        "movimientos": [
            "golpe_karate", "envite_feroz", "lanzallamas", "llamarada",
            "golpe_bajo", "rugido", "cambia_ya", "ida_y_vuelta",
            "estoico", "acua_jet", "proteccion", "danza_espada",
        ],
        "peso_kg": 83.0, "restringido": False, "paradoja": False,
    },
    "rillaboom": {
        "nombre": "Rillaboom",
        "tipos": ["planta"],
        "stats": {"hp": 100, "atq_fis": 125, "def_fis": 90, "atq_esp": 60, "def_esp": 70, "vel": 85},
        "habilidades": ["zona_de_hierba", "frondosidad"],
        "habilidad_oculta": "deslizador",
        "movimientos": [
            "golpe_hierba", "tormenta_de_hojas", "tamborileo",
            "terremoto", "acua_tail", "puño_trueno",
            "ida_y_vuelta", "estoico", "proteccion", "danza_espada",
        ],
        "peso_kg": 90.0, "restringido": False, "paradoja": False,
    },
    "urshifu_single": {
        "nombre": "Urshifu-Golpe Único",
        "tipos": ["lucha", "siniestro"],
        "stats": {"hp": 100, "atq_fis": 130, "def_fis": 100, "atq_esp": 63, "def_esp": 60, "vel": 97},
        "habilidades": ["puno_fantasma"],
        "habilidad_oculta": "aguante_inner",
        "movimientos": [
            "golpe_maestro", "combate", "a_bocajarro", "acua_tail",
            "terremoto", "puño_hielo", "envite_feroz",
            "ciclone", "danza_espada", "proteccion",
        ],
        "peso_kg": 105.0, "restringido": False, "paradoja": False,
    },
    "urshifu_rapid": {
        "nombre": "Urshifu-Golpe Veloz",
        "tipos": ["lucha", "agua"],
        "stats": {"hp": 100, "atq_fis": 130, "def_fis": 100, "atq_esp": 63, "def_esp": 60, "vel": 97},
        "habilidades": ["raudal_constante"],
        "habilidad_oculta": "aguante_inner",
        "movimientos": [
            "golpe_maestro_agua", "acua_tail", "cascada", "a_bocajarro",
            "puño_hielo", "envite_feroz", "terremoto",
            "danza_espada", "proteccion",
        ],
        "peso_kg": 105.0, "restringido": False, "paradoja": False,
    },
    "amoonguss": {
        "nombre": "Amoonguss",
        "tipos": ["planta", "veneno"],
        "stats": {"hp": 114, "atq_fis": 85, "def_fis": 70, "atq_esp": 85, "def_esp": 80, "vel": 30},
        "habilidades": ["regeneracion", "alerta"],
        "habilidad_oculta": None,
        "movimientos": [
            "espora", "rayo_solar", "energibola",
            "drenadoras", "lanzamiento_lodo", "acido",
            "neblina", "ola_mental", "proteccion",
        ],
        "peso_kg": 10.5, "restringido": False, "paradoja": False,
    },
    "landorus_therian": {
        "nombre": "Landorus-Tótem",
        "tipos": ["tierra", "volador"],
        "stats": {"hp": 89, "atq_fis": 145, "def_fis": 90, "atq_esp": 105, "def_esp": 80, "vel": 91},
        "habilidades": ["intimidacion"],
        "habilidad_oculta": None,
        "movimientos": [
            "terremoto", "punio_roca", "roca_afilada", "bofeton_lodo",
            "vendaval", "acrobacia", "ciclone",
            "fuerza_bruta", "danza_espada", "proteccion",
        ],
        "peso_kg": 68.0, "restringido": False, "paradoja": False,
    },
    "thundurus_therian": {
        "nombre": "Thundurus-Tótem",
        "tipos": ["electrico", "volador"],
        "stats": {"hp": 79, "atq_fis": 105, "def_fis": 70, "atq_esp": 145, "def_esp": 80, "vel": 101},
        "habilidades": ["voltaje"],
        "habilidad_oculta": "absorbe_voltios",
        "movimientos": [
            "trueno", "rayo", "bola_voltio", "vendaval",
            "psicorrayo", "ola_mental", "proteccion",
            "danza_lluvia",
        ],
        "peso_kg": 61.0, "restringido": False, "paradoja": False,
    },
    "tornadus_therian": {
        "nombre": "Tornadus-Tótem",
        "tipos": ["volador"],
        "stats": {"hp": 79, "atq_fis": 100, "def_fis": 80, "atq_esp": 110, "def_esp": 90, "vel": 121},
        "habilidades": ["regeneracion"],
        "habilidad_oculta": None,
        "movimientos": [
            "vendaval", "viento_cola", "acrobacia", "ciclone",
            "contragolpe", "psicorrayo", "foco_energia",
            "proteccion", "ida_y_vuelta",
        ],
        "peso_kg": 63.0, "restringido": False, "paradoja": False,
    },
    "gholdengo": {
        "nombre": "Gholdengo",
        "tipos": ["acero", "fantasma"],
        "stats": {"hp": 87, "atq_fis": 60, "def_fis": 95, "atq_esp": 133, "def_esp": 91, "vel": 84},
        "habilidades": ["pasaporte_dorado"],
        "habilidad_oculta": None,
        "movimientos": [
            "esfuerzo_supremo", "sombra_ball", "lanzamiento_magico",
            "disparo_demora", "tiro_fortaleza", "flash_cannon",
            "psicorrayo", "proteccion", "recuperacion",
        ],
        "peso_kg": 30.0, "restringido": False, "paradoja": False,
    },
    "palafin_hero": {
        "nombre": "Palafin-Héroe",
        "tipos": ["agua"],
        "stats": {"hp": 100, "atq_fis": 160, "def_fis": 97, "atq_esp": 106, "def_esp": 87, "vel": 100},
        "habilidades": ["cero_a_heroe"],
        "habilidad_oculta": None,
        "movimientos": [
            "cascada", "acua_jet", "acua_tail", "liquidacion",
            "combate", "a_bocajarro", "puño_hielo",
            "velocidad_extrema", "proteccion", "danza_espada",
        ],
        "peso_kg": 97.4, "restringido": False, "paradoja": False,
    },
    "annihilape": {
        "nombre": "Annihilape",
        "tipos": ["lucha", "fantasma"],
        "stats": {"hp": 110, "atq_fis": 115, "def_fis": 80, "atq_esp": 50, "def_esp": 90, "vel": 90},
        "habilidades": ["enfado", "espiritu_vital"],
        "habilidad_oculta": "defiant",
        "movimientos": [
            "rabia_espectral", "a_bocajarro", "puño_sombra",
            "bascula_acida", "terremoto", "puño_trueno",
            "estoico", "proteccion", "danza_espada",
        ],
        "peso_kg": 56.0, "restringido": False, "paradoja": False,
    },
    "ogerpon_wellspring": {
        "nombre": "Ogerpon-Manantial",
        "tipos": ["planta", "agua"],
        "stats": {"hp": 80, "atq_fis": 120, "def_fis": 84, "atq_esp": 60, "def_esp": 96, "vel": 100},
        "habilidades": ["espectaculo_acuatico"],
        "habilidad_oculta": None,
        "movimientos": [
            "golpe_hierba", "espada_hiedra", "acua_tail", "cascada",
            "terremoto", "estoico", "danza_espada", "proteccion",
        ],
        "peso_kg": 33.7, "restringido": False, "paradoja": False,
    },
    "ogerpon_hearthflame": {
        "nombre": "Ogerpon-Hoguera",
        "tipos": ["planta", "fuego"],
        "stats": {"hp": 80, "atq_fis": 120, "def_fis": 84, "atq_esp": 60, "def_esp": 96, "vel": 100},
        "habilidades": ["espectaculo_de_llamas"],
        "habilidad_oculta": None,
        "movimientos": [
            "golpe_hierba", "espada_hiedra", "lanzallamas", "llamarada",
            "terremoto", "estoico", "danza_espada", "proteccion",
        ],
        "peso_kg": 33.7, "restringido": False, "paradoja": False,
    },
    "ogerpon_cornerstone": {
        "nombre": "Ogerpon-Piedra",
        "tipos": ["planta", "roca"],
        "stats": {"hp": 80, "atq_fis": 120, "def_fis": 84, "atq_esp": 60, "def_esp": 96, "vel": 100},
        "habilidades": ["espectaculo_de_piedra"],
        "habilidad_oculta": None,
        "movimientos": [
            "golpe_hierba", "espada_hiedra", "roca_afilada", "avalancha",
            "terremoto", "estoico", "danza_espada", "proteccion",
        ],
        "peso_kg": 33.7, "restringido": False, "paradoja": False,
    },
    "terapagos_stellar": {
        "nombre": "Terapagos-Estelar",
        "tipos": ["normal"],
        "stats": {"hp": 160, "atq_fis": 105, "def_fis": 110, "atq_esp": 130, "def_esp": 110, "vel": 85},
        "habilidades": ["cambio_tera"],
        "habilidad_oculta": None,
        "movimientos": [
            "gema_tera", "disparo_demora", "rayo", "trueno",
            "psicorrayo", "sombra_ball", "llamarada",
            "recuperacion", "proteccion",
        ],
        "peso_kg": 77.0, "restringido": True, "paradoja": False,
    },
    "clodsire": {
        "nombre": "Clodsire",
        "tipos": ["veneno", "tierra"],
        "stats": {"hp": 130, "atq_fis": 75, "def_fis": 60, "atq_esp": 45, "def_esp": 100, "vel": 20},
        "habilidades": ["absorbe_agua", "punto_toxico"],
        "habilidad_oculta": "presion",
        "movimientos": [
            "ola_acida", "terremoto", "puas_toxicas", "pantano",
            "lanzamiento_lodo", "recuperacion", "neblina",
            "proteccion",
        ],
        "peso_kg": 223.0, "restringido": False, "paradoja": False,
    },
    "garganacl": {
        "nombre": "Garganacl",
        "tipos": ["roca"],
        "stats": {"hp": 100, "atq_fis": 100, "def_fis": 130, "atq_esp": 45, "def_esp": 90, "vel": 60},
        "habilidades": ["pureza_de_sal", "escudo_de_sal"],
        "habilidad_oculta": "piel_mineral",
        "movimientos": [
            "roca_afilada", "avalancha", "cuerpo_a_cuerpo",
            "terremoto", "cascada", "recuperacion",
            "sal_marina", "proteccion",
        ],
        "peso_kg": 840.0, "restringido": False, "paradoja": False,
    },
    "whimsicott": {
        "nombre": "Whimsicott",
        "tipos": ["planta", "hada"],
        "stats": {"hp": 60, "atq_fis": 67, "def_fis": 85, "atq_esp": 77, "def_esp": 75, "vel": 116},
        "habilidades": ["viento_ferrero", "infiltrador"],
        "habilidad_oculta": "clorofila",
        "movimientos": [
            "viento_cola", "campo_de_hadas", "espora_cotton", "neblina",
            "energibola", "brillo_magico", "voz_cautivadora",
            "ola_mental", "truco", "proteccion",
        ],
        "peso_kg": 6.6, "restringido": False, "paradoja": False,
    },
    "pelipper": {
        "nombre": "Pelipper",
        "tipos": ["agua", "volador"],
        "stats": {"hp": 60, "atq_fis": 50, "def_fis": 100, "atq_esp": 85, "def_esp": 70, "vel": 65},
        "habilidades": ["llovizna"],
        "habilidad_oculta": "bolsa_grande",
        "movimientos": [
            "hidrobomba", "surf", "vendaval", "viento_cola",
            "proteccion", "ciclone", "neblina",
            "danza_lluvia",
        ],
        "peso_kg": 28.0, "restringido": False, "paradoja": False,
    },
    "grimmsnarl": {
        "nombre": "Grimmsnarl",
        "tipos": ["siniestro", "hada"],
        "stats": {"hp": 95, "atq_fis": 120, "def_fis": 65, "atq_esp": 95, "def_esp": 75, "vel": 60},
        "habilidades": ["vello_magico"],
        "habilidad_oculta": "distorsion",
        "movimientos": [
            "pantalla_de_luz", "reflejo", "pantalla_aurora",
            "golpe_bello", "golpe_bajo", "envite_feroz",
            "brillo_magico", "voz_cautivadora", "rugido",
            "neblina", "proteccion",
        ],
        "peso_kg": 61.0, "restringido": False, "paradoja": False,
    },
    "torkoal": {
        "nombre": "Torkoal",
        "tipos": ["fuego"],
        "stats": {"hp": 70, "atq_fis": 85, "def_fis": 140, "atq_esp": 85, "def_esp": 70, "vel": 20},
        "habilidades": ["sequia"],
        "habilidad_oculta": "escudo_blanco",
        "movimientos": [
            "llamarada", "lanzallamas", "espada_solar", "rayo_solar",
            "terremoto", "relax", "humo_blanco",
            "proteccion",
        ],
        "peso_kg": 80.4, "restringido": False, "paradoja": False,
    },
    "indeedee_f": {
        "nombre": "Indeedee-♀",
        "tipos": ["normal", "psiquico"],
        "stats": {"hp": 70, "atq_fis": 55, "def_fis": 65, "atq_esp": 95, "def_esp": 95, "vel": 96},
        "habilidades": ["telequinesia", "sinconia"],
        "habilidad_oculta": None,
        "movimientos": [
            "expansion_psiquica", "psicorrayo", "campo_psiquico",
            "pantalla_de_luz", "reflejo", "neblina",
            "voz_cautivadora", "poder_lunar", "sigueme",
            "proteccion",
        ],
        "peso_kg": 28.0, "restringido": False, "paradoja": False,
    },
    "dondozo": {
        "nombre": "Dondozo",
        "tipos": ["agua"],
        "stats": {"hp": 150, "atq_fis": 100, "def_fis": 115, "atq_esp": 65, "def_esp": 65, "vel": 35},
        "habilidades": ["incontrolable", "oblivious"],
        "habilidad_oculta": "voluntad_propia",
        "movimientos": [
            "orden_de_mando", "cascada", "acua_tail", "liquidacion",
            "terremoto", "ola_acida", "descanso",
            "contragolpe", "proteccion",
        ],
        "peso_kg": 220.0, "restringido": False, "paradoja": False,
    },
    "tatsugiri": {
        "nombre": "Tatsugiri",
        "tipos": ["dragon", "agua"],
        "stats": {"hp": 46, "atq_fis": 75, "def_fis": 60, "atq_esp": 81, "def_esp": 60, "vel": 124},
        "habilidades": ["mando", "leve"],
        "habilidad_oculta": None,
        "movimientos": [
            "draco_meteoro", "pulso_dragon", "hidrobomba", "surf",
            "psicorrayo", "proteccion", "neblina",
        ],
        "peso_kg": 8.0, "restringido": False, "paradoja": False,
    },
    "farigiraf": {
        "nombre": "Farigiraf",
        "tipos": ["normal", "psiquico"],
        "stats": {"hp": 120, "atq_fis": 90, "def_fis": 70, "atq_esp": 110, "def_esp": 70, "vel": 60},
        "habilidades": ["cuellilargo", "bloque_mental"],
        "habilidad_oculta": "piel_de_gel",
        "movimientos": [
            "campo_psiquico", "psicorrayo", "psiquico",
            "pantalla_de_luz", "reflejo", "neblina",
            "expansion_psiquica", "trueno", "proteccion",
        ],
        "peso_kg": 160.0, "restringido": False, "paradoja": False,
    },
}


def buscar_pokemon_eyp(nombre: str) -> dict | None:
    """Busca un Pokémon en el catálogo EyP (case-insensitive, snake_case)."""
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return POKEMON_EYP.get(key)


def listar_pokemon_eyp() -> list[str]:
    """Retorna los nombres de todos los Pokémon del catálogo EyP."""
    return [v["nombre"] for v in POKEMON_EYP.values()]


def listar_restringidos_eyp() -> list[str]:
    """Retorna los legendarios restringidos VGC."""
    return [v["nombre"] for v in POKEMON_EYP.values() if v.get("restringido")]
