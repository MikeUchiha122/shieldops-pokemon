"""
cerebros/eyp/data/movimientos.py
Catálogo de movimientos disponibles en Escarlata y Púrpura (Gen IX).
SOLO movimientos que existen en SV — NO mezclar con otros juegos.

Formato: potencia=None para movimientos de estado.
         precision=None para movimientos que nunca fallan.
"""
from __future__ import annotations

MOVIMIENTOS_EYP: dict[str, dict] = {

    # ── TIPO NORMAL ──────────────────────────────────────────────────────────
    "velocidad_extrema": {
        "nombre": "Velocidad Extrema", "tipo": "normal", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 5, "prioridad": 2,
    },
    "hiperrayo": {
        "nombre": "Hiperrayo", "tipo": "normal", "categoria": "especial",
        "potencia": 150, "precision": 90, "pp": 5, "prioridad": 0,
    },
    "cuerpo_a_cuerpo": {
        "nombre": "Cuerpo a Cuerpo", "tipo": "normal", "categoria": "fisico",
        "potencia": 85, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "danza_espada": {
        "nombre": "Danza Espada", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 0,
    },
    "proteccion": {
        "nombre": "Protección", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 4,
    },
    "estoico": {
        "nombre": "Estoico", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 4,
    },
    "ida_y_vuelta": {
        "nombre": "Ida y Vuelta", "tipo": "normal", "categoria": "fisico",
        "potencia": 70, "precision": 100, "pp": 20, "prioridad": 0,
    },
    "neblina": {
        "nombre": "Neblina", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 30, "prioridad": 0,
    },
    "recuperacion": {
        "nombre": "Recuperación", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 5, "prioridad": 0,
    },
    "descanso": {
        "nombre": "Descanso", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },
    "rugido": {
        "nombre": "Rugido", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": 100, "pp": 40, "prioridad": -6,
    },
    "truco": {
        "nombre": "Truco", "tipo": "psiquico", "categoria": "estado",
        "potencia": None, "precision": 100, "pp": 10, "prioridad": 0,
    },

    # ── TIPO FUEGO ───────────────────────────────────────────────────────────
    "llamarada": {
        "nombre": "Llamarada", "tipo": "fuego", "categoria": "especial",
        "potencia": 110, "precision": 85, "pp": 5, "prioridad": 0,
    },
    "lanzallamas": {
        "nombre": "Lanzallamas", "tipo": "fuego", "categoria": "especial",
        "potencia": 90, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "envite_igneo": {
        "nombre": "Envite Ígneo", "tipo": "fuego", "categoria": "fisico",
        "potencia": 65, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "espada_solar": {
        "nombre": "Espada Solar", "tipo": "planta", "categoria": "especial",
        "potencia": 120, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "vendaval_ignito": {
        "nombre": "Vendaval Ígnito", "tipo": "fuego", "categoria": "especial",
        "potencia": 130, "precision": 90, "pp": 5, "prioridad": 0,
    },
    "llamarada_oscura": {
        "nombre": "Llamarada Oscura", "tipo": "siniestro", "categoria": "especial",
        "potencia": 140, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "llamarada_eterna": {
        "nombre": "Llamarada Eterna", "tipo": "veneno", "categoria": "especial",
        "potencia": 100, "precision": 100, "pp": 5, "prioridad": 0,
    },

    # ── TIPO AGUA ────────────────────────────────────────────────────────────
    "hidrobomba": {
        "nombre": "Hidrobomba", "tipo": "agua", "categoria": "especial",
        "potencia": 110, "precision": 80, "pp": 5, "prioridad": 0,
    },
    "surf": {
        "nombre": "Surf", "tipo": "agua", "categoria": "especial",
        "potencia": 90, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "cascada": {
        "nombre": "Cascada", "tipo": "agua", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "acua_tail": {
        "nombre": "Acua Tail", "tipo": "agua", "categoria": "fisico",
        "potencia": 90, "precision": 90, "pp": 10, "prioridad": 0,
    },
    "acua_jet": {
        "nombre": "Acua Jet", "tipo": "agua", "categoria": "fisico",
        "potencia": 40, "precision": 100, "pp": 20, "prioridad": 1,
    },
    "liquidacion": {
        "nombre": "Liquidación", "tipo": "agua", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "aguante_origen": {
        "nombre": "Aguante Origen", "tipo": "agua", "categoria": "especial",
        "potencia": 110, "precision": 85, "pp": 5, "prioridad": 0,
    },
    "orden_de_mando": {
        "nombre": "Orden de Mando", "tipo": "agua", "categoria": "fisico",
        "potencia": 150, "precision": 100, "pp": 5, "prioridad": 0,
    },

    # ── TIPO ELÉCTRICO ───────────────────────────────────────────────────────
    "trueno": {
        "nombre": "Trueno", "tipo": "electrico", "categoria": "especial",
        "potencia": 110, "precision": 70, "pp": 10, "prioridad": 0,
    },
    "rayo": {
        "nombre": "Rayo", "tipo": "electrico", "categoria": "especial",
        "potencia": 90, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "bola_voltio": {
        "nombre": "Bola Voltio", "tipo": "electrico", "categoria": "especial",
        "potencia": 70, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "voltio_cruel": {
        "nombre": "Voltio Cruel", "tipo": "electrico", "categoria": "especial",
        "potencia": 120, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "tormenta_electrica": {
        "nombre": "Tormenta Eléctrica", "tipo": "electrico", "categoria": "especial",
        "potencia": 110, "precision": 70, "pp": 10, "prioridad": 0,
    },
    "campo_electrico": {
        "nombre": "Campo Eléctrico", "tipo": "electrico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },

    # ── TIPO PLANTA ──────────────────────────────────────────────────────────
    "tormenta_de_hojas": {
        "nombre": "Tormenta de Hojas", "tipo": "planta", "categoria": "especial",
        "potencia": 130, "precision": 90, "pp": 5, "prioridad": 0,
    },
    "energibola": {
        "nombre": "Energibola", "tipo": "planta", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "golpe_hierba": {
        "nombre": "Golpe Hierba", "tipo": "planta", "categoria": "fisico",
        "potencia": 70, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "tamborileo": {
        "nombre": "Tamborileo", "tipo": "planta", "categoria": "fisico",
        "potencia": 120, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "drenadoras": {
        "nombre": "Drenadoras", "tipo": "planta", "categoria": "estado",
        "potencia": None, "precision": 90, "pp": 20, "prioridad": 0,
    },
    "espada_hiedra": {
        "nombre": "Espada Hiedra", "tipo": "planta", "categoria": "fisico",
        "potencia": 55, "precision": 100, "pp": 15, "prioridad": 0,
    },

    # ── TIPO HIELO ───────────────────────────────────────────────────────────
    "ventisca": {
        "nombre": "Ventisca", "tipo": "hielo", "categoria": "especial",
        "potencia": 110, "precision": 70, "pp": 5, "prioridad": 0,
    },
    "rayo_hielo": {
        "nombre": "Rayo Hielo", "tipo": "hielo", "categoria": "especial",
        "potencia": 90, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "avalancha": {
        "nombre": "Avalancha", "tipo": "hielo", "categoria": "fisico",
        "potencia": 60, "precision": 100, "pp": 20, "prioridad": -4,
    },
    "puño_hielo": {
        "nombre": "Puño Hielo", "tipo": "hielo", "categoria": "fisico",
        "potencia": 75, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "canto_helado": {
        "nombre": "Canto Helado", "tipo": "hielo", "categoria": "especial",
        "potencia": 60, "precision": 100, "pp": 20, "prioridad": 0,
    },
    "golpe_hielo": {
        "nombre": "Golpe Hielo", "tipo": "hielo", "categoria": "fisico",
        "potencia": 70, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "cuchillada_helada": {
        "nombre": "Cuchillada Helada", "tipo": "hielo", "categoria": "fisico",
        "potencia": 65, "precision": 100, "pp": 20, "prioridad": 0,
    },

    # ── TIPO LUCHA ───────────────────────────────────────────────────────────
    "a_bocajarro": {
        "nombre": "A Bocajarro", "tipo": "lucha", "categoria": "fisico",
        "potencia": 150, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "patada_salto": {
        "nombre": "Patada Salto", "tipo": "lucha", "categoria": "fisico",
        "potencia": 100, "precision": 85, "pp": 10, "prioridad": 0,
    },
    "combate": {
        "nombre": "Combate", "tipo": "lucha", "categoria": "especial",
        "potencia": 90, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "golpe_karate": {
        "nombre": "Golpe Karate", "tipo": "lucha", "categoria": "fisico",
        "potencia": 50, "precision": 100, "pp": 25, "prioridad": 0,
    },
    "ciclotorrente": {
        "nombre": "Ciclotorrente", "tipo": "lucha", "categoria": "fisico",
        "potencia": 100, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "golpe_maestro": {
        "nombre": "Golpe Maestro", "tipo": "lucha", "categoria": "fisico",
        "potencia": 100, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "golpe_maestro_agua": {
        "nombre": "Golpe Maestro-Agua", "tipo": "agua", "categoria": "fisico",
        "potencia": 100, "precision": 100, "pp": 10, "prioridad": 0,
    },

    # ── TIPO VENENO ──────────────────────────────────────────────────────────
    "ola_acida": {
        "nombre": "Ola Ácida", "tipo": "veneno", "categoria": "especial",
        "potencia": 40, "precision": 100, "pp": 20, "prioridad": 0,
    },
    "puas_toxicas": {
        "nombre": "Púas Tóxicas", "tipo": "veneno", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 0,
    },
    "lanzamiento_lodo": {
        "nombre": "Lanzamiento Lodo", "tipo": "tierra", "categoria": "especial",
        "potencia": 20, "precision": 100, "pp": 10, "prioridad": 0,
    },

    # ── TIPO TIERRA ──────────────────────────────────────────────────────────
    "terremoto": {
        "nombre": "Terremoto", "tipo": "tierra", "categoria": "fisico",
        "potencia": 100, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "fisura": {
        "nombre": "Fisura", "tipo": "tierra", "categoria": "fisico",
        "potencia": None, "precision": 30, "pp": 5, "prioridad": 0,
    },
    "fisura_origen": {
        "nombre": "Fisura Origen", "tipo": "tierra", "categoria": "fisico",
        "potencia": 100, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "bofeton_lodo": {
        "nombre": "Bofetón Lodo", "tipo": "tierra", "categoria": "especial",
        "potencia": 20, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "cantotembloroso": {
        "nombre": "Cantotembloroso", "tipo": "tierra", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },
    "pantano": {
        "nombre": "Pantano", "tipo": "tierra", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },

    # ── TIPO VOLADOR ─────────────────────────────────────────────────────────
    "vendaval": {
        "nombre": "Vendaval", "tipo": "volador", "categoria": "especial",
        "potencia": 110, "precision": 70, "pp": 5, "prioridad": 0,
    },
    "acrobacia": {
        "nombre": "Acrobacia", "tipo": "volador", "categoria": "fisico",
        "potencia": 55, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "viento_cola": {
        "nombre": "Viento Cola", "tipo": "volador", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 15, "prioridad": 0,
    },
    "ciclone": {
        "nombre": "Ciclón", "tipo": "volador", "categoria": "especial",
        "potencia": 40, "precision": 100, "pp": 20, "prioridad": 0,
    },

    # ── TIPO PSÍQUICO ────────────────────────────────────────────────────────
    "psiquico": {
        "nombre": "Psíquico", "tipo": "psiquico", "categoria": "especial",
        "potencia": 90, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "psicorrayo": {
        "nombre": "Psicorrayo", "tipo": "psiquico", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "psicocarga": {
        "nombre": "Psicocarga", "tipo": "psiquico", "categoria": "fisico",
        "potencia": 130, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "psicoataque": {
        "nombre": "Psicoataque", "tipo": "psiquico", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "poder_lunar": {
        "nombre": "Poder Lunar", "tipo": "psiquico", "categoria": "especial",
        "potencia": 95, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "expansion_psiquica": {
        "nombre": "Expansión Psíquica", "tipo": "psiquico", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "campo_psiquico": {
        "nombre": "Campo Psíquico", "tipo": "psiquico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },
    "pantalla_de_luz": {
        "nombre": "Pantalla de Luz", "tipo": "psiquico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 30, "prioridad": 0,
    },
    "ola_mental": {
        "nombre": "Ola Mental", "tipo": "psiquico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 15, "prioridad": 0,
    },

    # ── TIPO ROCA ────────────────────────────────────────────────────────────
    "roca_afilada": {
        "nombre": "Roca Afilada", "tipo": "roca", "categoria": "fisico",
        "potencia": 100, "precision": 80, "pp": 5, "prioridad": 0,
    },
    "punio_roca": {
        "nombre": "Puño Roca", "tipo": "roca", "categoria": "fisico",
        "potencia": 50, "precision": 90, "pp": 15, "prioridad": 0,
    },
    "estocada_roca": {
        "nombre": "Estocada Roca", "tipo": "roca", "categoria": "fisico",
        "potencia": 75, "precision": 90, "pp": 10, "prioridad": 0,
    },
    "sal_marina": {
        "nombre": "Sal Marina", "tipo": "roca", "categoria": "fisico",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },

    # ── TIPO FANTASMA ────────────────────────────────────────────────────────
    "sombra_ball": {
        "nombre": "Sombra Ball", "tipo": "fantasma", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "rayo_umbrio": {
        "nombre": "Rayo Umbrío", "tipo": "fantasma", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "hex": {
        "nombre": "Hex", "tipo": "fantasma", "categoria": "especial",
        "potencia": 65, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "puño_sombra": {
        "nombre": "Puño Sombra", "tipo": "fantasma", "categoria": "fisico",
        "potencia": 70, "precision": None, "pp": 20, "prioridad": 0,
    },
    "rabia_espectral": {
        "nombre": "Rabia Espectral", "tipo": "fantasma", "categoria": "fisico",
        "potencia": 100, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "galopar_espectral": {
        "nombre": "Galopar Espectral", "tipo": "fantasma", "categoria": "fisico",
        "potencia": 90, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "premonicion": {
        "nombre": "Premonición", "tipo": "psiquico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 15, "prioridad": 0,
    },

    # ── TIPO DRAGÓN ──────────────────────────────────────────────────────────
    "draco_meteoro": {
        "nombre": "Draco Meteoro", "tipo": "dragon", "categoria": "especial",
        "potencia": 130, "precision": 90, "pp": 5, "prioridad": 0,
    },
    "pulso_dragon": {
        "nombre": "Pulso Dragón", "tipo": "dragon", "categoria": "especial",
        "potencia": 85, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "garra_dragon": {
        "nombre": "Garra Dragón", "tipo": "dragon", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "danza_dragon": {
        "nombre": "Danza Dragón", "tipo": "dragon", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 0,
    },
    "tormenta_draco": {
        "nombre": "Tormenta Draco", "tipo": "dragon", "categoria": "especial",
        "potencia": 100, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "galopar_glacial": {
        "nombre": "Galopar Glacial", "tipo": "psiquico", "categoria": "fisico",
        "potencia": 90, "precision": 100, "pp": 10, "prioridad": 0,
    },

    # ── TIPO SINIESTRO ───────────────────────────────────────────────────────
    "envite_feroz": {
        "nombre": "Envite Feroz", "tipo": "siniestro", "categoria": "fisico",
        "potencia": 120, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "golpe_bajo": {
        "nombre": "Golpe Bajo", "tipo": "siniestro", "categoria": "fisico",
        "potencia": 65, "precision": 100, "pp": 20, "prioridad": 0,
    },
    "cuchillada": {
        "nombre": "Cuchillada", "tipo": "siniestro", "categoria": "fisico",
        "potencia": 70, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "torbellino_oscuro": {
        "nombre": "Torbellino Oscuro", "tipo": "siniestro", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "cambia_ya": {
        "nombre": "Cambia Ya", "tipo": "siniestro", "categoria": "estado",
        "potencia": None, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "hiperrayo_oscuro": {
        "nombre": "Hiperrayo Oscuro", "tipo": "siniestro", "categoria": "especial",
        "potencia": 130, "precision": 90, "pp": 5, "prioridad": 0,
    },
    "sifon_siniestro": {
        "nombre": "Sifón Siniestro", "tipo": "siniestro", "categoria": "especial",
        "potencia": 140, "precision": 100, "pp": 5, "prioridad": 0,
    },

    # ── TIPO ACERO ───────────────────────────────────────────────────────────
    "cabeza_hierro": {
        "nombre": "Cabeza Hierro", "tipo": "acero", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "flash_cannon": {
        "nombre": "Flash Cannon", "tipo": "acero", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "defensa_ferrea": {
        "nombre": "Defensa Férrea", "tipo": "acero", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 15, "prioridad": 0,
    },
    "tiro_fortaleza": {
        "nombre": "Tiro Fortaleza", "tipo": "acero", "categoria": "fisico",
        "potencia": 140, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "esfuerzo_supremo": {
        "nombre": "Esfuerzo Supremo", "tipo": "acero", "categoria": "especial",
        "potencia": 140, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "lanzamiento_magico": {
        "nombre": "Lanzamiento Mágico", "tipo": "acero", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "disparo_demora": {
        "nombre": "Disparo Demora", "tipo": "acero", "categoria": "especial",
        "potencia": 60, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "tajo_sagrado": {
        "nombre": "Tajo Sagrado", "tipo": "hada", "categoria": "fisico",
        "potencia": 90, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "hoja_espada": {
        "nombre": "Hoja Espada", "tipo": "planta", "categoria": "fisico",
        "potencia": 90, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "puño_meteorico": {
        "nombre": "Puño Meteórico", "tipo": "acero", "categoria": "fisico",
        "potencia": 100, "precision": 100, "pp": 10, "prioridad": 0,
    },

    # ── TIPO HADA ────────────────────────────────────────────────────────────
    "brillo_magico": {
        "nombre": "Brillo Mágico", "tipo": "hada", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "voz_cautivadora": {
        "nombre": "Voz Cautivadora", "tipo": "hada", "categoria": "especial",
        "potencia": 90, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "campo_de_hadas": {
        "nombre": "Campo de Hadas", "tipo": "hada", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },
    "rayo_aurora": {
        "nombre": "Rayo Aurora", "tipo": "hada", "categoria": "especial",
        "potencia": 65, "precision": 100, "pp": 20, "prioridad": 0,
    },
    "fuerza_lunar": {
        "nombre": "Fuerza Lunar", "tipo": "hada", "categoria": "fisico",
        "potencia": 95, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "confusion_lunar": {
        "nombre": "Confusión Lunar", "tipo": "psiquico", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "geomancia": {
        "nombre": "Geomancia", "tipo": "hada", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },

    # ── TIPO BICHO ───────────────────────────────────────────────────────────
    "tijera_x": {
        "nombre": "Tijera X", "tipo": "bicho", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "espora": {
        "nombre": "Espora", "tipo": "planta", "categoria": "estado",
        "potencia": None, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "espora_cotton": {
        "nombre": "Espora Cotton", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 40, "prioridad": 0,
    },
    "bascula_acida": {
        "nombre": "Báscula Ácida", "tipo": "veneno", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 0,
    },
    "gema_tera": {
        "nombre": "Gema Tera", "tipo": "normal", "categoria": "especial",
        "potencia": 80, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "foco_energia": {
        "nombre": "Foco Energía", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 30, "prioridad": 0,
    },
    "pantalla_aurora": {
        "nombre": "Pantalla Aurora", "tipo": "hielo", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 0,
    },
    "reflejo": {
        "nombre": "Reflejo", "tipo": "psiquico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 0,
    },
    "luz_lunar": {
        "nombre": "Luz Lunar", "tipo": "hada", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 5, "prioridad": 0,
    },
    "sigueme": {
        "nombre": "Sígueme", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 2,
    },
    "contragolpe": {
        "nombre": "Contragolpe", "tipo": "normal", "categoria": "fisico",
        "potencia": None, "precision": 100, "pp": 20, "prioridad": -6,
    },
    "aguante": {
        "nombre": "Aguante", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 4,
    },
    "cabezazo_hielo": {
        "nombre": "Cabezazo Hielo", "tipo": "hielo", "categoria": "fisico",
        "potencia": 100, "precision": 90, "pp": 5, "prioridad": 0,
    },
    "puerta_dimensional": {
        "nombre": "Puerta Dimensional", "tipo": "electrico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },
    "viento_misterioso": {
        "nombre": "Viento Misterioso", "tipo": "psiquico", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },
    "medidor_voltios": {
        "nombre": "Medidor Voltios", "tipo": "electrico", "categoria": "especial",
        "potencia": 140, "precision": 100, "pp": 5, "prioridad": 0,
    },
    "danza_lluvia": {
        "nombre": "Danza Lluvia", "tipo": "agua", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 5, "prioridad": 0,
    },
    "rayo_solar": {
        "nombre": "Rayo Solar", "tipo": "planta", "categoria": "especial",
        "potencia": 120, "precision": 100, "pp": 10, "prioridad": 0,
    },
    "humo_blanco": {
        "nombre": "Humo Blanco", "tipo": "fuego", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 20, "prioridad": 0,
    },
    "relax": {
        "nombre": "Relax", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 0,
    },
    "golpe_bello": {
        "nombre": "Golpe Bello", "tipo": "normal", "categoria": "fisico",
        "potencia": 70, "precision": 100, "pp": 20, "prioridad": 0,
    },
    "fuerza_bruta": {
        "nombre": "Fuerza Bruta", "tipo": "normal", "categoria": "fisico",
        "potencia": 80, "precision": 100, "pp": 15, "prioridad": 0,
    },
    "estoico_v2": {
        "nombre": "Estoicismo", "tipo": "normal", "categoria": "estado",
        "potencia": None, "precision": None, "pp": 10, "prioridad": 4,
    },
}


def buscar_movimiento_eyp(nombre: str) -> dict | None:
    """Busca un movimiento en el catálogo EyP."""
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return MOVIMIENTOS_EYP.get(key)


def movimientos_por_tipo_eyp(tipo: str) -> list[str]:
    """Lista movimientos de un tipo específico disponibles en EyP."""
    return [v["nombre"] for v in MOVIMIENTOS_EYP.values() if v["tipo"] == tipo]
