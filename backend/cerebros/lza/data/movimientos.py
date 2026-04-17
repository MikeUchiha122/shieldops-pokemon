"""
cerebros/lza/data/movimientos.py
Movimientos disponibles en Leyendas Z-A — sistema Action Time.
Cada movimiento tiene startup_frames y cooldown_ms (NO turnos).
startup_frames > 12 = el rival puede esquivar.
"""
from __future__ import annotations

MOVIMIENTOS_LZA: dict[str, dict] = {

    # ── FUEGO ─────────────────────────────────────────────────────────────────
    "lanzallamas": {
        "nombre": "Lanzallamas", "tipo": "fuego", "categoria": "rapido",
        "potencia": 90, "startup_frames": 8, "cooldown_ms": 1400, "alcance": "proyectil",
    },
    "llamarada": {
        "nombre": "Llamarada", "tipo": "fuego", "categoria": "cargado",
        "potencia": 110, "startup_frames": 18, "cooldown_ms": 2200, "alcance": "proyectil",
    },
    "envite_igneo": {
        "nombre": "Envite Ígneo", "tipo": "fuego", "categoria": "rapido",
        "potencia": 65, "startup_frames": 6, "cooldown_ms": 1100, "alcance": "cuerpo_a_cuerpo",
    },
    "vendaval_ignito": {
        "nombre": "Vendaval Ígnito", "tipo": "fuego", "categoria": "cargado",
        "potencia": 130, "startup_frames": 22, "cooldown_ms": 2600, "alcance": "proyectil",
    },
    "ala_de_acero": {
        "nombre": "Ala de Acero", "tipo": "acero", "categoria": "rapido",
        "potencia": 70, "startup_frames": 7, "cooldown_ms": 1200, "alcance": "cuerpo_a_cuerpo",
    },

    # ── AGUA ──────────────────────────────────────────────────────────────────
    "hidrobomba": {
        "nombre": "Hidrobomba", "tipo": "agua", "categoria": "cargado",
        "potencia": 110, "startup_frames": 16, "cooldown_ms": 2000, "alcance": "proyectil",
    },
    "surf": {
        "nombre": "Surf", "tipo": "agua", "categoria": "aoe",
        "potencia": 90, "startup_frames": 14, "cooldown_ms": 1800, "alcance": "area",
    },
    "cascada": {
        "nombre": "Cascada", "tipo": "agua", "categoria": "rapido",
        "potencia": 80, "startup_frames": 9, "cooldown_ms": 1350, "alcance": "cuerpo_a_cuerpo",
    },
    "acua_tail": {
        "nombre": "Acua Tail", "tipo": "agua", "categoria": "rapido",
        "potencia": 90, "startup_frames": 10, "cooldown_ms": 1450, "alcance": "cuerpo_a_cuerpo",
    },
    "acua_jet": {
        "nombre": "Acua Jet", "tipo": "agua", "categoria": "rapido",
        "potencia": 40, "startup_frames": 4, "cooldown_ms": 900, "alcance": "cuerpo_a_cuerpo",
    },

    # ── ELÉCTRICO ─────────────────────────────────────────────────────────────
    "trueno": {
        "nombre": "Trueno", "tipo": "electrico", "categoria": "cargado",
        "potencia": 110, "startup_frames": 17, "cooldown_ms": 2100, "alcance": "proyectil",
    },
    "rayo": {
        "nombre": "Rayo", "tipo": "electrico", "categoria": "rapido",
        "potencia": 90, "startup_frames": 10, "cooldown_ms": 1450, "alcance": "proyectil",
    },
    "campo_electrico": {
        "nombre": "Campo Eléctrico", "tipo": "electrico", "categoria": "estado",
        "potencia": None, "startup_frames": 8, "cooldown_ms": 1200, "alcance": "area",
    },

    # ── PLANTA ────────────────────────────────────────────────────────────────
    "tormenta_de_hojas": {
        "nombre": "Tormenta de Hojas", "tipo": "planta", "categoria": "cargado",
        "potencia": 130, "startup_frames": 20, "cooldown_ms": 2400, "alcance": "proyectil",
    },
    "energibola": {
        "nombre": "Energibola", "tipo": "planta", "categoria": "rapido",
        "potencia": 80, "startup_frames": 10, "cooldown_ms": 1400, "alcance": "proyectil",
    },
    "golpe_hierba": {
        "nombre": "Golpe Hierba", "tipo": "planta", "categoria": "rapido",
        "potencia": 70, "startup_frames": 8, "cooldown_ms": 1250, "alcance": "cuerpo_a_cuerpo",
    },
    "drenadoras": {
        "nombre": "Drenadoras", "tipo": "planta", "categoria": "estado",
        "potencia": None, "startup_frames": 10, "cooldown_ms": 1500, "alcance": "proyectil",
    },
    "espora": {
        "nombre": "Espora", "tipo": "planta", "categoria": "estado",
        "potencia": None, "startup_frames": 12, "cooldown_ms": 1800, "alcance": "proyectil",
    },
    "puya_nociva": {
        "nombre": "Puya Nociva", "tipo": "veneno", "categoria": "rapido",
        "potencia": 65, "startup_frames": 7, "cooldown_ms": 1150, "alcance": "cuerpo_a_cuerpo",
    },

    # ── HIELO ─────────────────────────────────────────────────────────────────
    "ventisca": {
        "nombre": "Ventisca", "tipo": "hielo", "categoria": "cargado",
        "potencia": 110, "startup_frames": 18, "cooldown_ms": 2200, "alcance": "area",
    },
    "rayo_hielo": {
        "nombre": "Rayo Hielo", "tipo": "hielo", "categoria": "rapido",
        "potencia": 90, "startup_frames": 10, "cooldown_ms": 1450, "alcance": "proyectil",
    },
    "avalancha": {
        "nombre": "Avalancha", "tipo": "hielo", "categoria": "rapido",
        "potencia": 60, "startup_frames": 6, "cooldown_ms": 1100, "alcance": "cuerpo_a_cuerpo",
    },
    "neblina": {
        "nombre": "Neblina", "tipo": "hielo", "categoria": "estado",
        "potencia": None, "startup_frames": 8, "cooldown_ms": 1200, "alcance": "area",
    },

    # ── LUCHA ─────────────────────────────────────────────────────────────────
    "a_bocajarro": {
        "nombre": "A Bocajarro", "tipo": "lucha", "categoria": "cargado",
        "potencia": 150, "startup_frames": 24, "cooldown_ms": 2800, "alcance": "cuerpo_a_cuerpo",
    },
    "golpe_bis": {
        "nombre": "Golpe Bis", "tipo": "lucha", "categoria": "rapido",
        "potencia": 40, "startup_frames": 4, "cooldown_ms": 900, "alcance": "cuerpo_a_cuerpo",
    },
    "patada_salto": {
        "nombre": "Patada Salto", "tipo": "lucha", "categoria": "rapido",
        "potencia": 100, "startup_frames": 11, "cooldown_ms": 1550, "alcance": "cuerpo_a_cuerpo",
    },

    # ── PSÍQUICO ──────────────────────────────────────────────────────────────
    "psicorrayo": {
        "nombre": "Psicorrayo", "tipo": "psiquico", "categoria": "rapido",
        "potencia": 80, "startup_frames": 9, "cooldown_ms": 1350, "alcance": "proyectil",
    },
    "psiquico": {
        "nombre": "Psíquico", "tipo": "psiquico", "categoria": "rapido",
        "potencia": 90, "startup_frames": 11, "cooldown_ms": 1550, "alcance": "proyectil",
    },
    "psicocarga": {
        "nombre": "Psicocarga", "tipo": "psiquico", "categoria": "cargado",
        "potencia": 130, "startup_frames": 20, "cooldown_ms": 2400, "alcance": "cuerpo_a_cuerpo",
    },
    "foco_energia": {
        "nombre": "Foco Energía", "tipo": "normal", "categoria": "estado",
        "potencia": None, "startup_frames": 8, "cooldown_ms": 1200, "alcance": "self",
    },

    # ── FANTASMA ──────────────────────────────────────────────────────────────
    "sombra_ball": {
        "nombre": "Sombra Ball", "tipo": "fantasma", "categoria": "rapido",
        "potencia": 80, "startup_frames": 8, "cooldown_ms": 1300, "alcance": "proyectil",
    },
    "hex": {
        "nombre": "Hex", "tipo": "fantasma", "categoria": "rapido",
        "potencia": 65, "startup_frames": 7, "cooldown_ms": 1150, "alcance": "proyectil",
    },
    "golpe_sombra": {
        "nombre": "Golpe Sombra", "tipo": "fantasma", "categoria": "rapido",
        "potencia": 70, "startup_frames": 6, "cooldown_ms": 1100, "alcance": "cuerpo_a_cuerpo",
    },
    "rayo_oscuro": {
        "nombre": "Rayo Oscuro", "tipo": "siniestro", "categoria": "rapido",
        "potencia": 80, "startup_frames": 9, "cooldown_ms": 1350, "alcance": "proyectil",
    },

    # ── DRAGÓN ────────────────────────────────────────────────────────────────
    "draco_meteoro": {
        "nombre": "Draco Meteoro", "tipo": "dragon", "categoria": "cargado",
        "potencia": 130, "startup_frames": 21, "cooldown_ms": 2500, "alcance": "proyectil",
    },
    "garra_dragon": {
        "nombre": "Garra Dragón", "tipo": "dragon", "categoria": "rapido",
        "potencia": 80, "startup_frames": 8, "cooldown_ms": 1300, "alcance": "cuerpo_a_cuerpo",
    },
    "pulso_dragon": {
        "nombre": "Pulso Dragón", "tipo": "dragon", "categoria": "rapido",
        "potencia": 85, "startup_frames": 10, "cooldown_ms": 1450, "alcance": "proyectil",
    },
    "danza_dragon": {
        "nombre": "Danza Dragón", "tipo": "dragon", "categoria": "estado",
        "potencia": None, "startup_frames": 10, "cooldown_ms": 1500, "alcance": "self",
    },
    "tormenta_arena": {
        "nombre": "Tormenta Arena", "tipo": "roca", "categoria": "estado",
        "potencia": None, "startup_frames": 12, "cooldown_ms": 1600, "alcance": "area",
    },

    # ── SINIESTRO ─────────────────────────────────────────────────────────────
    "envite_feroz": {
        "nombre": "Envite Feroz", "tipo": "siniestro", "categoria": "cargado",
        "potencia": 120, "startup_frames": 18, "cooldown_ms": 2200, "alcance": "cuerpo_a_cuerpo",
    },
    "cuchillada": {
        "nombre": "Cuchillada", "tipo": "siniestro", "categoria": "rapido",
        "potencia": 70, "startup_frames": 7, "cooldown_ms": 1200, "alcance": "cuerpo_a_cuerpo",
    },
    "golpe_bajo": {
        "nombre": "Golpe Bajo", "tipo": "siniestro", "categoria": "rapido",
        "potencia": 65, "startup_frames": 6, "cooldown_ms": 1100, "alcance": "cuerpo_a_cuerpo",
    },

    # ── ACERO ─────────────────────────────────────────────────────────────────
    "cabeza_hierro": {
        "nombre": "Cabeza Hierro", "tipo": "acero", "categoria": "rapido",
        "potencia": 80, "startup_frames": 9, "cooldown_ms": 1350, "alcance": "cuerpo_a_cuerpo",
    },
    "puño_bala": {
        "nombre": "Puño Bala", "tipo": "acero", "categoria": "rapido",
        "potencia": 40, "startup_frames": 3, "cooldown_ms": 800, "alcance": "cuerpo_a_cuerpo",
    },
    "puño_meteorico": {
        "nombre": "Puño Meteórico", "tipo": "acero", "categoria": "cargado",
        "potencia": 100, "startup_frames": 16, "cooldown_ms": 2000, "alcance": "cuerpo_a_cuerpo",
    },
    "lanzamiento_magico": {
        "nombre": "Lanzamiento Mágico", "tipo": "acero", "categoria": "rapido",
        "potencia": 80, "startup_frames": 9, "cooldown_ms": 1350, "alcance": "proyectil",
    },
    "defensa_ferrea": {
        "nombre": "Defensa Férrea", "tipo": "acero", "categoria": "estado",
        "potencia": None, "startup_frames": 10, "cooldown_ms": 1400, "alcance": "self",
    },

    # ── HADA ──────────────────────────────────────────────────────────────────
    "brillo_magico": {
        "nombre": "Brillo Mágico", "tipo": "hada", "categoria": "rapido",
        "potencia": 80, "startup_frames": 9, "cooldown_ms": 1350, "alcance": "proyectil",
    },
    "voz_cautivadora": {
        "nombre": "Voz Cautivadora", "tipo": "hada", "categoria": "rapido",
        "potencia": 90, "startup_frames": 10, "cooldown_ms": 1450, "alcance": "proyectil",
    },
    "confusion_lunar": {
        "nombre": "Confusión Lunar", "tipo": "psiquico", "categoria": "rapido",
        "potencia": 80, "startup_frames": 9, "cooldown_ms": 1350, "alcance": "proyectil",
    },
    "campo_de_hadas": {
        "nombre": "Campo de Hadas", "tipo": "hada", "categoria": "estado",
        "potencia": None, "startup_frames": 10, "cooldown_ms": 1500, "alcance": "area",
    },

    # ── ROCA ──────────────────────────────────────────────────────────────────
    "roca_afilada": {
        "nombre": "Roca Afilada", "tipo": "roca", "categoria": "cargado",
        "potencia": 100, "startup_frames": 16, "cooldown_ms": 2000, "alcance": "proyectil",
    },
    "terremoto": {
        "nombre": "Terremoto", "tipo": "tierra", "categoria": "aoe",
        "potencia": 100, "startup_frames": 15, "cooldown_ms": 1900, "alcance": "area",
    },
    "bofeton_lodo": {
        "nombre": "Bofetón Lodo", "tipo": "tierra", "categoria": "rapido",
        "potencia": 20, "startup_frames": 5, "cooldown_ms": 1000, "alcance": "proyectil",
    },

    # ── VOLADOR ───────────────────────────────────────────────────────────────
    "vendaval": {
        "nombre": "Vendaval", "tipo": "volador", "categoria": "cargado",
        "potencia": 110, "startup_frames": 17, "cooldown_ms": 2100, "alcance": "area",
    },
    "vuelo": {
        "nombre": "Vuelo", "tipo": "volador", "categoria": "cargado",
        "potencia": 90, "startup_frames": 20, "cooldown_ms": 2300, "alcance": "cuerpo_a_cuerpo",
    },
    "acrobacia": {
        "nombre": "Acrobacia", "tipo": "volador", "categoria": "rapido",
        "potencia": 55, "startup_frames": 6, "cooldown_ms": 1100, "alcance": "cuerpo_a_cuerpo",
    },

    # ── NORMAL ────────────────────────────────────────────────────────────────
    "velocidad_extrema": {
        "nombre": "Velocidad Extrema", "tipo": "normal", "categoria": "rapido",
        "potencia": 80, "startup_frames": 2, "cooldown_ms": 800, "alcance": "cuerpo_a_cuerpo",
    },
    "golpe_bello": {
        "nombre": "Golpe Bello", "tipo": "normal", "categoria": "rapido",
        "potencia": 70, "startup_frames": 7, "cooldown_ms": 1200, "alcance": "cuerpo_a_cuerpo",
    },
    "cuerpo_a_cuerpo": {
        "nombre": "Cuerpo a Cuerpo", "tipo": "normal", "categoria": "rapido",
        "potencia": 85, "startup_frames": 9, "cooldown_ms": 1400, "alcance": "cuerpo_a_cuerpo",
    },
    "danza_espada": {
        "nombre": "Danza Espada", "tipo": "normal", "categoria": "estado",
        "potencia": None, "startup_frames": 10, "cooldown_ms": 1500, "alcance": "self",
    },
    "tijera_x": {
        "nombre": "Tijera X", "tipo": "bicho", "categoria": "rapido",
        "potencia": 80, "startup_frames": 8, "cooldown_ms": 1300, "alcance": "cuerpo_a_cuerpo",
    },
    "lanzamiento_lodo": {
        "nombre": "Lanzamiento Lodo", "tipo": "tierra", "categoria": "rapido",
        "potencia": 20, "startup_frames": 5, "cooldown_ms": 1000, "alcance": "proyectil",
    },
}


def buscar_movimiento_lza(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return MOVIMIENTOS_LZA.get(key)
