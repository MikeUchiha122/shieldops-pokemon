"""
cerebros/go/data/movimientos.py
Movimientos de Pokémon GO — Fast Moves y Charged Moves.
Mecánicas GO:
  - Fast Moves: generan energía cada uso (energia > 0)
  - Charged Moves: consumen energía (energia < 0)
  - Sin PP — se usan ilimitado. Escudos bloquean Charged Moves (1 HP).
  - Duración en TURNOS GO (1 turno = 0.5s aprox)
NO hay movimientos de estado como en la serie principal.
"""
from __future__ import annotations

FAST_MOVES_GO: dict[str, dict] = {
    # ── AGUA ──────────────────────────────────────────────────────────────────
    "pistola_agua":  {"nombre": "Pistola Agua",  "tipo": "agua",      "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    "burbuja":       {"nombre": "Burbuja",        "tipo": "agua",      "potencia": 8,  "energia": 3,  "duracion_turnos": 3},
    "cascada":       {"nombre": "Cascada",        "tipo": "agua",      "potencia": 12, "energia": 2,  "duracion_turnos": 4},
    # ── TIERRA ────────────────────────────────────────────────────────────────
    "barro":         {"nombre": "Barro",          "tipo": "tierra",    "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    "fango":         {"nombre": "Fango",          "tipo": "tierra",    "potencia": 8,  "energia": 3,  "duracion_turnos": 3},
    # ── LUCHA ─────────────────────────────────────────────────────────────────
    "contraataque":  {"nombre": "Contraataque",   "tipo": "lucha",     "potencia": 12, "energia": 5,  "duracion_turnos": 2},
    "contador":      {"nombre": "Contador",       "tipo": "lucha",     "potencia": 12, "energia": 5,  "duracion_turnos": 2},
    # ── PSÍQUICO ──────────────────────────────────────────────────────────────
    "psico_corte":   {"nombre": "Psico Corte",    "tipo": "psiquico",  "potencia": 5,  "energia": 5,  "duracion_turnos": 2},
    "confusion":     {"nombre": "Confusión",      "tipo": "psiquico",  "potencia": 20, "energia": 3,  "duracion_turnos": 4},
    # ── ELÉCTRICO ─────────────────────────────────────────────────────────────
    "chispa":        {"nombre": "Chispa",         "tipo": "electrico", "potencia": 6,  "energia": 4,  "duracion_turnos": 3},
    # ── ACERO ─────────────────────────────────────────────────────────────────
    "carga_metal":   {"nombre": "Carga Metal",    "tipo": "acero",     "potencia": 8,  "energia": 3,  "duracion_turnos": 3},
    "candado_frente":{"nombre": "Candado Frente", "tipo": "normal",    "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    "puño_de_acero": {"nombre": "Puño de Acero",  "tipo": "acero",     "potencia": 8,  "energia": 3,  "duracion_turnos": 3},
    "ráfaga_acero":  {"nombre": "Ráfaga Acero",   "tipo": "acero",     "potencia": 11, "energia": 5,  "duracion_turnos": 2},
    # ── HIELO ─────────────────────────────────────────────────────────────────
    "puas_hielo":    {"nombre": "Púas Hielo",     "tipo": "hielo",     "potencia": 3,  "energia": 3,  "duracion_turnos": 1},
    "pistola_nieve": {"nombre": "Pistola Nieve",  "tipo": "hielo",     "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    # ── FANTASMA ──────────────────────────────────────────────────────────────
    "sombra_garrazo":{"nombre": "Sombra Garrazo", "tipo": "fantasma",  "potencia": 6,  "energia": 4,  "duracion_turnos": 2},
    "hex":           {"nombre": "Hex",            "tipo": "fantasma",  "potencia": 10, "energia": 3,  "duracion_turnos": 3},
    "embrollo":      {"nombre": "Embrollo",       "tipo": "fantasma",  "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    # ── DRAGÓN ────────────────────────────────────────────────────────────────
    "aliento_dragon":{"nombre": "Aliento Dragón", "tipo": "dragon",    "potencia": 6,  "energia": 4,  "duracion_turnos": 2},
    "cola_dragon":   {"nombre": "Cola Dragón",    "tipo": "dragon",    "potencia": 9,  "energia": 3,  "duracion_turnos": 3},
    # ── SINIESTRO ─────────────────────────────────────────────────────────────
    "mordisco":      {"nombre": "Mordisco",       "tipo": "siniestro", "potencia": 6,  "energia": 4,  "duracion_turnos": 2},
    "snarl":         {"nombre": "Snarl",          "tipo": "siniestro", "potencia": 5,  "energia": 5,  "duracion_turnos": 2},
    "rastreo":       {"nombre": "Rastreo",        "tipo": "siniestro", "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    # ── HADA ──────────────────────────────────────────────────────────────────
    "encanto":       {"nombre": "Encanto",        "tipo": "hada",      "potencia": 20, "energia": 3,  "duracion_turnos": 4},
    # ── VOLADOR ───────────────────────────────────────────────────────────────
    "ala_de_acero":  {"nombre": "Ala de Acero",   "tipo": "acero",     "potencia": 11, "energia": 5,  "duracion_turnos": 2},
    "golpe_aereo":   {"nombre": "Golpe Aéreo",    "tipo": "volador",   "potencia": 8,  "energia": 3,  "duracion_turnos": 3},
    "fuego_rapido":  {"nombre": "Fuego Rápido",   "tipo": "fuego",     "potencia": 9,  "energia": 3,  "duracion_turnos": 3},
    # ── NORMAL ────────────────────────────────────────────────────────────────
    "pisoteo":       {"nombre": "Pisoteo",        "tipo": "normal",    "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    "zurra":         {"nombre": "Zurra",          "tipo": "normal",    "potencia": 3,  "energia": 3,  "duracion_turnos": 2},
    "libra":         {"nombre": "Libra",          "tipo": "normal",    "potencia": 5,  "energia": 5,  "duracion_turnos": 1},
    # ── VENENO ────────────────────────────────────────────────────────────────
    "acido":         {"nombre": "Ácido",          "tipo": "veneno",    "potencia": 9,  "energia": 3,  "duracion_turnos": 3},
    "puas_veneno":   {"nombre": "Púas Veneno",    "tipo": "veneno",    "potencia": 5,  "energia": 4,  "duracion_turnos": 2},
    # ── ROCA ──────────────────────────────────────────────────────────────────
    "golpe_roca":    {"nombre": "Golpe Roca",     "tipo": "roca",      "potencia": 8,  "energia": 3,  "duracion_turnos": 3},
    # ── FUEGO ─────────────────────────────────────────────────────────────────
    "llamarada_eterna":{"nombre":"Llamarada Eterna","tipo": "veneno",  "potencia": 10, "energia": 5,  "duracion_turnos": 2},
    "extrasensorial":{"nombre": "Extrasensorial", "tipo": "psiquico",  "potencia": 12, "energia": 3,  "duracion_turnos": 4},
    "dragón_cola":   {"nombre": "Dragón Cola",    "tipo": "dragon",    "potencia": 9,  "energia": 3,  "duracion_turnos": 3},
}


CHARGED_MOVES_GO: dict[str, dict] = {
    # ── AGUA ──────────────────────────────────────────────────────────────────
    "cannon_hidro":     {"nombre": "Cannon Hidro",    "tipo": "agua",      "potencia": 90,  "energia": -60, "duracion_turnos": 2},
    "hidrobomba":       {"nombre": "Hidrobomba",      "tipo": "agua",      "potencia": 110, "energia": -75, "duracion_turnos": 3},
    "surf":             {"nombre": "Surf",            "tipo": "agua",      "potencia": 65,  "energia": -40, "duracion_turnos": 2},
    "hidrobomba_origen":{"nombre": "Hidrobomba Origen","tipo": "agua",     "potencia": 130, "energia": -75, "duracion_turnos": 4},
    "burbuja_bomba":    {"nombre": "Burbuja Bomba",   "tipo": "agua",      "potencia": 100, "energia": -60, "duracion_turnos": 3},
    # ── TIERRA ────────────────────────────────────────────────────────────────
    "terremoto":        {"nombre": "Terremoto",       "tipo": "tierra",    "potencia": 120, "energia": -65, "duracion_turnos": 3},
    "fisura_origen":    {"nombre": "Fisura Origen",   "tipo": "tierra",    "potencia": 100, "energia": -50, "duracion_turnos": 3},
    "avalancha":        {"nombre": "Avalancha",       "tipo": "hielo",     "potencia": 90,  "energia": -45, "duracion_turnos": 3},
    "bola_de_lodo":     {"nombre": "Bola de Lodo",    "tipo": "veneno",    "potencia": 70,  "energia": -35, "duracion_turnos": 2},
    # ── HIELO ─────────────────────────────────────────────────────────────────
    "brecha_glacial":   {"nombre": "Brecha Glacial",  "tipo": "hielo",     "potencia": 130, "energia": -75, "duracion_turnos": 4},
    "ice_beam":         {"nombre": "Ice Beam",        "tipo": "hielo",     "potencia": 90,  "energia": -55, "duracion_turnos": 3},
    "glacial_lanza":    {"nombre": "Glacial Lanza",   "tipo": "hielo",     "potencia": 65,  "energia": -40, "duracion_turnos": 2},
    "salmuera":         {"nombre": "Salmuera",        "tipo": "hielo",     "potencia": 60,  "energia": -40, "duracion_turnos": 2},
    # ── LUCHA ─────────────────────────────────────────────────────────────────
    "golpe_dinamico":   {"nombre": "Golpe Dinámico",  "tipo": "lucha",     "potencia": 90,  "energia": -50, "duracion_turnos": 2},
    "foco_blast":       {"nombre": "Foco Blast",      "tipo": "lucha",     "potencia": 140, "energia": -75, "duracion_turnos": 4},
    "gelido":           {"nombre": "Gélido",          "tipo": "hielo",     "potencia": 55,  "energia": -40, "duracion_turnos": 2},
    # ── PSÍQUICO ──────────────────────────────────────────────────────────────
    "luna_bola":        {"nombre": "Luna Bola",       "tipo": "psiquico",  "potencia": 130, "energia": -75, "duracion_turnos": 4},
    "aurora_viga":      {"nombre": "Aurora Viga",     "tipo": "hielo",     "potencia": 80,  "energia": -60, "duracion_turnos": 3},
    "futuro_ojo":       {"nombre": "Futuro Ojo",      "tipo": "psiquico",  "potencia": 120, "energia": -65, "duracion_turnos": 3},
    "psicorayo_cargado":{"nombre": "Psicorayo",       "tipo": "psiquico",  "potencia": 100, "energia": -55, "duracion_turnos": 3},
    "psico_boost":      {"nombre": "Psico Boost",     "tipo": "psiquico",  "potencia": 70,  "energia": -35, "duracion_turnos": 2},
    # ── FANTASMA ──────────────────────────────────────────────────────────────
    "bola_sombra":      {"nombre": "Bola Sombra",     "tipo": "fantasma",  "potencia": 100, "energia": -55, "duracion_turnos": 3},
    "zancada_sombra":   {"nombre": "Zancada Sombra",  "tipo": "fantasma",  "potencia": 50,  "energia": -35, "duracion_turnos": 2},
    "onirico":          {"nombre": "Onírico",         "tipo": "fantasma",  "potencia": 90,  "energia": -60, "duracion_turnos": 3},
    "magia_sombra":     {"nombre": "Magia Sombra",    "tipo": "fantasma",  "potencia": 100, "energia": -60, "duracion_turnos": 3},
    # ── DRAGÓN ────────────────────────────────────────────────────────────────
    "laser_dragon":     {"nombre": "Láser Dragón",    "tipo": "dragon",    "potencia": 150, "energia": -80, "duracion_turnos": 4},
    "garra_dragon_cargado":{"nombre":"Garra Dragón",  "tipo": "dragon",    "potencia": 50,  "energia": -35, "duracion_turnos": 2},
    "rugido_espacial":  {"nombre": "Rugido Espacial", "tipo": "agua",      "potencia": 130, "energia": -60, "duracion_turnos": 4},
    "aullido_temporal": {"nombre": "Aullido Temporal","tipo": "dragon",    "potencia": 100, "energia": -50, "duracion_turnos": 3},
    # ── HADA ──────────────────────────────────────────────────────────────────
    "deslumbrante":     {"nombre": "Deslumbrante",    "tipo": "hada",      "potencia": 110, "energia": -70, "duracion_turnos": 3},
    "juego_sucio":      {"nombre": "Juego Sucio",     "tipo": "siniestro", "potencia": 70,  "energia": -45, "duracion_turnos": 2},
    "hoja_espada":      {"nombre": "Hoja Espada",     "tipo": "planta",    "potencia": 55,  "energia": -35, "duracion_turnos": 2},
    # ── ACERO ─────────────────────────────────────────────────────────────────
    "flash_cannon":     {"nombre": "Flash Cannon",    "tipo": "acero",     "potencia": 100, "energia": -70, "duracion_turnos": 3},
    "bloqueo_de_roca":  {"nombre": "Bloqueo de Roca", "tipo": "roca",      "potencia": 70,  "energia": -45, "duracion_turnos": 2},
    "crush_claw":       {"nombre": "Crush Claw",      "tipo": "normal",    "potencia": 65,  "energia": -45, "duracion_turnos": 2},
    # ── ELÉCTRICO ─────────────────────────────────────────────────────────────
    "trueno_bola":      {"nombre": "Trueno Bola",     "tipo": "electrico", "potencia": 80,  "energia": -45, "duracion_turnos": 3},
    "trueno":           {"nombre": "Trueno",          "tipo": "electrico", "potencia": 100, "energia": -60, "duracion_turnos": 3},
    # ── FUEGO ─────────────────────────────────────────────────────────────────
    "fuego_acrobacia":  {"nombre": "Fuego Acrobacia", "tipo": "fuego",     "potencia": 110, "energia": -55, "duracion_turnos": 3},
    "llamarada":        {"nombre": "Llamarada",       "tipo": "fuego",     "potencia": 140, "energia": -75, "duracion_turnos": 4},
    "fuego_lanzamiento":{"nombre": "Fuego Lanzamiento","tipo": "fuego",    "potencia": 100, "energia": -55, "duracion_turnos": 3},
    "llama_infernal":   {"nombre": "Llama Infernal",  "tipo": "fuego",     "potencia": 140, "energia": -80, "duracion_turnos": 4},
    "tormenta_veneno":  {"nombre": "Tormenta Veneno", "tipo": "veneno",    "potencia": 120, "energia": -70, "duracion_turnos": 3},
    # ── NORMAL ────────────────────────────────────────────────────────────────
    "hiperrayo":        {"nombre": "Hiperrayo",       "tipo": "normal",    "potencia": 150, "energia": -80, "duracion_turnos": 4},
    "último_recurso":   {"nombre": "Último Recurso",  "tipo": "normal",    "potencia": 70,  "energia": -45, "duracion_turnos": 2},
    "huevo_bomba":      {"nombre": "Huevo Bomba",     "tipo": "normal",    "potencia": 100, "energia": -60, "duracion_turnos": 3},
    # ── VOLADOR ───────────────────────────────────────────────────────────────
    "aeroballista":     {"nombre": "Aeroballista",    "tipo": "volador",   "potencia": 170, "energia": -75, "duracion_turnos": 4},
    "huracan":          {"nombre": "Huracán",         "tipo": "volador",   "potencia": 110, "energia": -65, "duracion_turnos": 3},
    "ciclón":           {"nombre": "Ciclón",          "tipo": "volador",   "potencia": 50,  "energia": -35, "duracion_turnos": 2},
    "voltereta":        {"nombre": "Voltereta",       "tipo": "volador",   "potencia": 60,  "energia": -45, "duracion_turnos": 2},
    # ── SINIESTRO ─────────────────────────────────────────────────────────────
    "crunch":           {"nombre": "Crunch",          "tipo": "siniestro", "potencia": 70,  "energia": -45, "duracion_turnos": 2},
    "foul_play":        {"nombre": "Foul Play",       "tipo": "siniestro", "potencia": 70,  "energia": -45, "duracion_turnos": 2},
    "tormenta_oscura":  {"nombre": "Tormenta Oscura", "tipo": "siniestro", "potencia": 70,  "energia": -45, "duracion_turnos": 2},
    # ── PLANTA ────────────────────────────────────────────────────────────────
    "drenadoras_cargado":{"nombre":"Drenadoras",      "tipo": "planta",    "potencia": 50,  "energia": -33, "duracion_turnos": 2},
    "super_movimiento":  {"nombre":"Super Movimiento","tipo": "lucha",     "potencia": 85,  "energia": -50, "duracion_turnos": 3},
    "cierre":           {"nombre": "Cierre",          "tipo": "acero",     "potencia": 65,  "energia": -40, "duracion_turnos": 2},
    "fuego_helado":     {"nombre": "Fuego Helado",    "tipo": "hielo",     "potencia": 90,  "energia": -55, "duracion_turnos": 3},
    "aguante":          {"nombre": "Aguante",         "tipo": "roca",      "potencia": 60,  "energia": -35, "duracion_turnos": 2},
    "poder_antiguo":    {"nombre": "Poder Antiguo",   "tipo": "roca",      "potencia": 60,  "energia": -45, "duracion_turnos": 2},
    "bomba_lodo":       {"nombre": "Bomba Lodo",      "tipo": "veneno",    "potencia": 80,  "energia": -50, "duracion_turnos": 2},
    "bola_hielo_prioridad":{"nombre":"Bola Hielo",    "tipo": "hielo",     "potencia": 55,  "energia": -40, "duracion_turnos": 2},
}


def buscar_fast_go(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_").replace("é", "e").replace("ó", "o")
    return FAST_MOVES_GO.get(key)


def buscar_charged_go(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_").replace("é", "e").replace("ó", "o")
    return CHARGED_MOVES_GO.get(key)
