"""
cerebros/eyp/data/objetos.py
Objetos competitivos disponibles en Escarlata y Púrpura.
SOLO objetos que existen en SV — sin Z-Cristales ni Mega Stones.
"""
from __future__ import annotations

OBJETOS_EYP: dict[str, dict] = {

    # ── BOOST OFENSIVO ───────────────────────────────────────────────────────
    "orbe_de_vida": {
        "nombre": "Orbe de Vida",
        "descripcion": "Aumenta el daño de los movimientos en ×1.3. Cuesta 10% HP al atacar.",
        "multiplicador_dano": 1.3, "costo_hp_pct": 0.1,
        "categoria": "ofensivo",
    },
    "cinta_de_decision": {
        "nombre": "Cinta de Decisión",
        "descripcion": "Ataque físico ×1.5. Solo se puede usar un movimiento.",
        "multiplicador_atq_fis": 1.5, "bloquea_cambio": True,
        "categoria": "ofensivo",
    },
    "lentes_de_decision": {
        "nombre": "Lentes de Decisión",
        "descripcion": "Ataque especial ×1.5. Solo se puede usar un movimiento.",
        "multiplicador_atq_esp": 1.5, "bloquea_cambio": True,
        "categoria": "ofensivo",
    },
    "cinturon_de_experto": {
        "nombre": "Cinturón de Experto",
        "descripcion": "Movimientos supereficaces hacen ×1.2 daño adicional.",
        "bono_supereficaz": 1.2,
        "categoria": "ofensivo",
    },
    "energia_propulsora": {
        "nombre": "Energía Propulsora",
        "descripcion": "Activa Motor Hadrón / Motor Orichalco / Protosíntesis / Propulsión Cuántica sin clima.",
        "activa_booster": True,
        "categoria": "ofensivo",
    },

    # ── CONTROL DE VELOCIDAD ─────────────────────────────────────────────────
    "panuelo_elegante": {
        "nombre": "Pañuelo Elegante",
        "descripcion": "Velocidad ×1.5. Solo se puede usar un movimiento.",
        "multiplicador_vel": 1.5, "bloquea_cambio": True,
        "categoria": "velocidad",
    },

    # ── DEFENSA / BULK ───────────────────────────────────────────────────────
    "faja_fuerza": {
        "nombre": "Faja Fuerza",
        "descripcion": "Defensa especial ×1.5. No se pueden usar movimientos de estado.",
        "multiplicador_def_esp": 1.5, "bloquea_estado": True,
        "categoria": "defensivo",
    },
    "faja_de_enfoque": {
        "nombre": "Faja de Enfoque",
        "descripcion": "Sobrevive con 1 HP si estaba a HP completo.",
        "sobrevive_ohko": True,
        "categoria": "defensivo",
    },
    "restos": {
        "nombre": "Restos",
        "descripcion": "Recupera 1/16 del HP máximo al final de cada turno.",
        "recupera_hp_pct": 0.0625,
        "categoria": "defensivo",
    },
    "baya_sitrus": {
        "nombre": "Baya Sitrus",
        "descripcion": "Recupera 25% del HP máximo cuando el HP cae por debajo del 50%.",
        "umbral_hp": 0.5, "recupera_hp_pct": 0.25,
        "categoria": "defensivo",
    },
    "globo": {
        "nombre": "Globo",
        "descripcion": "Inmune a movimientos de tipo Tierra hasta recibir un golpe.",
        "inmunidad_tierra": True,
        "categoria": "defensivo",
    },
    "montura_cuadrada": {
        "nombre": "Montura Cuadrada",
        "descripcion": "El rival recibe 1/6 de su HP al golpear con movimiento de contacto.",
        "dano_contacto_pct": 0.1667,
        "categoria": "defensivo",
    },
    "cuentas_blancas": {
        "nombre": "Cuentas Blancas",
        "descripcion": "Restaura estadísticas bajadas una vez.",
        "restaura_stats": True, "un_uso": True,
        "categoria": "defensivo",
    },

    # ── BAYAS DE TIPO (reducen daño supereficaz ×0.5 una vez) ───────────────
    "baya_occa": {
        "nombre": "Baya Occa", "descripcion": "Reduce daño supereficaz de tipo Fuego ×0.5.",
        "tipo_reducido": "fuego", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_passho": {
        "nombre": "Baya Passho", "descripcion": "Reduce daño supereficaz de tipo Agua ×0.5.",
        "tipo_reducido": "agua", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_wacan": {
        "nombre": "Baya Wacan", "descripcion": "Reduce daño supereficaz de tipo Eléctrico ×0.5.",
        "tipo_reducido": "electrico", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_rindo": {
        "nombre": "Baya Rindo", "descripcion": "Reduce daño supereficaz de tipo Planta ×0.5.",
        "tipo_reducido": "planta", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_yache": {
        "nombre": "Baya Yache", "descripcion": "Reduce daño supereficaz de tipo Hielo ×0.5.",
        "tipo_reducido": "hielo", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_chople": {
        "nombre": "Baya Chople", "descripcion": "Reduce daño supereficaz de tipo Lucha ×0.5.",
        "tipo_reducido": "lucha", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_kebia": {
        "nombre": "Baya Kebia", "descripcion": "Reduce daño supereficaz de tipo Veneno ×0.5.",
        "tipo_reducido": "veneno", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_shuca": {
        "nombre": "Baya Shuca", "descripcion": "Reduce daño supereficaz de tipo Tierra ×0.5.",
        "tipo_reducido": "tierra", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_coba": {
        "nombre": "Baya Coba", "descripcion": "Reduce daño supereficaz de tipo Volador ×0.5.",
        "tipo_reducido": "volador", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_payapa": {
        "nombre": "Baya Payapa", "descripcion": "Reduce daño supereficaz de tipo Psíquico ×0.5.",
        "tipo_reducido": "psiquico", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_tanga": {
        "nombre": "Baya Tanga", "descripcion": "Reduce daño supereficaz de tipo Bicho ×0.5.",
        "tipo_reducido": "bicho", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_charti": {
        "nombre": "Baya Charti", "descripcion": "Reduce daño supereficaz de tipo Roca ×0.5.",
        "tipo_reducido": "roca", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_kasib": {
        "nombre": "Baya Kasib", "descripcion": "Reduce daño supereficaz de tipo Fantasma ×0.5.",
        "tipo_reducido": "fantasma", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_haban": {
        "nombre": "Baya Haban", "descripcion": "Reduce daño supereficaz de tipo Dragón ×0.5.",
        "tipo_reducido": "dragon", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_colbur": {
        "nombre": "Baya Colbur", "descripcion": "Reduce daño supereficaz de tipo Siniestro ×0.5.",
        "tipo_reducido": "siniestro", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_babiri": {
        "nombre": "Baya Babiri", "descripcion": "Reduce daño supereficaz de tipo Acero ×0.5.",
        "tipo_reducido": "acero", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_roseli": {
        "nombre": "Baya Roseli", "descripcion": "Reduce daño supereficaz de tipo Hada ×0.5.",
        "tipo_reducido": "hada", "reduccion": 0.5, "categoria": "baya_tipo",
    },

    # ── SEMILLAS DE TERRENO ──────────────────────────────────────────────────
    "semilla_electrica": {
        "nombre": "Semilla Eléctrica",
        "descripcion": "Aumenta Defensa +1 cuando se activa el Campo Eléctrico.",
        "terreno": "electrico", "stat_boost": "def_fis", "etapas": 1,
        "categoria": "semilla",
    },
    "semilla_de_hierba": {
        "nombre": "Semilla de Hierba",
        "descripcion": "Aumenta Defensa Especial +1 con el Terreno de Hierba activo.",
        "terreno": "hierba", "stat_boost": "def_esp", "etapas": 1,
        "categoria": "semilla",
    },
    "semilla_psiquica": {
        "nombre": "Semilla Psíquica",
        "descripcion": "Aumenta Defensa Especial +1 con el Campo Psíquico activo.",
        "terreno": "psiquico", "stat_boost": "def_esp", "etapas": 1,
        "categoria": "semilla",
    },
    "semilla_de_niebla": {
        "nombre": "Semilla de Niebla",
        "descripcion": "Aumenta Defensa Especial +1 con el Terreno de Niebla activo.",
        "terreno": "niebla", "stat_boost": "def_esp", "etapas": 1,
        "categoria": "semilla",
    },

    # ── MÁSCARAS OGERPON (cambian tipo y habilidad) ──────────────────────────
    "mascara_de_pozo": {
        "nombre": "Máscara de Pozo",
        "descripcion": "Exclusiva de Ogerpon. Cambia su tipo a Planta/Agua y activa Espectáculo Acuático.",
        "exclusivo": "ogerpon_wellspring", "categoria": "mascara",
    },
    "mascara_de_brasas": {
        "nombre": "Máscara de Brasas",
        "descripcion": "Exclusiva de Ogerpon. Cambia su tipo a Planta/Fuego y activa Espectáculo de Llamas.",
        "exclusivo": "ogerpon_hearthflame", "categoria": "mascara",
    },
    "mascara_de_piedra": {
        "nombre": "Máscara de Piedra",
        "descripcion": "Exclusiva de Ogerpon. Cambia su tipo a Planta/Roca y activa Espectáculo de Piedra.",
        "exclusivo": "ogerpon_cornerstone", "categoria": "mascara",
    },

    # ── APOYO ────────────────────────────────────────────────────────────────
    "hierba_magica": {
        "nombre": "Hierba Mágica",
        "descripcion": "Cura estados alterados al final de cada turno.",
        "cura_estados": True,
        "categoria": "apoyo",
    },
    "bocanegra": {
        "nombre": "Bocanegra",
        "descripcion": "Previene reducciones de estadísticas por el rival.",
        "previene_bajada_stats": True,
        "categoria": "apoyo",
    },
}


def buscar_objeto_eyp(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return OBJETOS_EYP.get(key)


def objetos_por_categoria_eyp(categoria: str) -> list[str]:
    return [v["nombre"] for v in OBJETOS_EYP.values() if v.get("categoria") == categoria]
