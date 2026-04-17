"""
cerebros/champions/data/objetos.py
Objetos competitivos para Pokémon Champions (Singles multi-generacional).
"""
from __future__ import annotations

OBJETOS_CHAMPIONS: dict[str, dict] = {
    # ── Potenciadores de daño ─────────────────────────────────────────────────
    "orbe_de_vida": {
        "nombre": "Orbe de Vida",
        "efecto": "daño_propio",
        "multiplicador_ataque": 1.3,
        "recoil_porcentaje": 10,
        "descripcion": "Aumenta el daño un 30 % pero el portador pierde el 10 % de su HP máx cada turno.",
    },
    "garra_eleccion": {
        "nombre": "Garra Elección",
        "efecto": "eleccion_fisico",
        "multiplicador_ataque_especial": None,
        "multiplicador_ataque": 1.5,
        "restriccion": "bloquea_movimiento",
        "descripcion": "Aumenta Ataque un 50 % pero solo puede usar el movimiento elegido.",
    },
    "gafas_eleccion": {
        "nombre": "Gafas Elección",
        "efecto": "eleccion_especial",
        "multiplicador_ataque_especial": 1.5,
        "multiplicador_ataque": None,
        "restriccion": "bloquea_movimiento",
        "descripcion": "Aumenta Atq. Especial un 50 % pero solo puede usar el movimiento elegido.",
    },
    "panuelo_eleccion": {
        "nombre": "Pañuelo Elección",
        "efecto": "eleccion_velocidad",
        "multiplicador_velocidad": 1.5,
        "restriccion": "bloquea_movimiento",
        "descripcion": "Aumenta Velocidad un 50 % pero solo puede usar el movimiento elegido.",
    },
    "musculo_banda": {
        "nombre": "Músculo Banda",
        "efecto": "potencia_fisico",
        "multiplicador_ataque": 1.1,
        "descripcion": "Aumenta el daño de movimientos físicos un 10 %.",
    },
    "gafas_sabias": {
        "nombre": "Gafas Sabias",
        "efecto": "potencia_especial",
        "multiplicador_ataque_especial": 1.1,
        "descripcion": "Aumenta el daño de movimientos especiales un 10 %.",
    },
    "placa_negra": {
        "nombre": "Placa Negra",
        "efecto": "tipo_boost",
        "tipo": "siniestro",
        "multiplicador": 1.2,
        "descripcion": "Aumenta el daño de movimientos de tipo Siniestro un 20 %.",
    },
    "carbon": {
        "nombre": "Carbón",
        "efecto": "tipo_boost",
        "tipo": "fuego",
        "multiplicador": 1.2,
        "descripcion": "Aumenta el daño de movimientos de tipo Fuego un 20 %.",
    },
    "gema_dragon": {
        "nombre": "Gema Dragón",
        "efecto": "tipo_boost_consumible",
        "tipo": "dragon",
        "multiplicador": 1.3,
        "usos": 1,
        "descripcion": "Potencia el primer movimiento de tipo Dragón un 30 % (consumible).",
    },

    # ── Supervivencia / defensa ───────────────────────────────────────────────
    "faja_asalto": {
        "nombre": "Faja Asalto",
        "efecto": "resistencia_especial",
        "multiplicador_defensa_especial": 1.5,
        "restriccion": "no_puede_usar_estados",
        "descripcion": "Aumenta Def. Especial un 50 % pero impide usar movimientos de estado.",
    },
    "fajin_focus": {
        "nombre": "Fajín Focus",
        "efecto": "sobrevivir_1hp",
        "condicion": "hp_lleno",
        "descripcion": "Si el Pokémon tiene el HP lleno, sobrevive con 1 HP a cualquier golpe.",
    },
    "bayas_sitrus": {
        "nombre": "Bayas Sitrus",
        "efecto": "cura_hp",
        "cura_porcentaje": 25,
        "activacion": "hp_por_debajo_50",
        "descripcion": "Restaura el 25 % del HP máx cuando el HP cae por debajo del 50 %.",
    },
    "bayas_frambu": {
        "nombre": "Bayas Frambu",
        "efecto": "cura_hp",
        "cura_porcentaje": 50,
        "activacion": "hp_por_debajo_25",
        "descripcion": "Restaura el 50 % del HP máx cuando el HP cae por debajo del 25 %.",
    },
    "resto_sobras": {
        "nombre": "Restos",
        "efecto": "regeneracion",
        "cura_porcentaje_por_turno": 6.25,
        "descripcion": "Restaura 1/16 del HP máx al final de cada turno.",
    },
    "casco_rocoso": {
        "nombre": "Casco Rocoso",
        "efecto": "recoil_contacto",
        "dano_recoil_porcentaje": 16.67,
        "descripcion": "Inflige el 1/6 del HP del portador como daño a quien lo golpee con contacto.",
    },
    "balon_aire": {
        "nombre": "Globo Aire",
        "efecto": "inmunidad_tierra",
        "descripcion": "Hace inmune a movimientos de Tierra; se rompe al recibir cualquier daño.",
    },
    "escudo_mental": {
        "nombre": "Escudo Mental",
        "efecto": "absorber_boost",
        "descripcion": "Absorbe las bajadas de stats causadas por el oponente (vacío en Champions sin VGC).",
    },

    # ── Berries de reducción de tipo (curan el 50 % del HP) ──────────────────
    "baya_cheri": {
        "nombre": "Baya Cheri",
        "efecto": "cura_estado",
        "cura": "paralisis",
        "descripcion": "Cura la parálisis al activarse.",
    },
    "baya_rawst": {
        "nombre": "Baya Rawst",
        "efecto": "cura_estado",
        "cura": "quemadura",
        "descripcion": "Cura la quemadura al activarse.",
    },
    "baya_pecha": {
        "nombre": "Baya Pecha",
        "efecto": "cura_estado",
        "cura": "veneno",
        "descripcion": "Cura el envenenamiento al activarse.",
    },
    "baya_occa": {
        "nombre": "Baya Occa",
        "efecto": "reduccion_tipo",
        "tipo": "fuego",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Fuego a la mitad.",
    },
    "baya_passho": {
        "nombre": "Baya Passho",
        "efecto": "reduccion_tipo",
        "tipo": "agua",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Agua a la mitad.",
    },
    "baya_wacan": {
        "nombre": "Baya Wacan",
        "efecto": "reduccion_tipo",
        "tipo": "electrico",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Eléctrico a la mitad.",
    },
    "baya_rindo": {
        "nombre": "Baya Rindo",
        "efecto": "reduccion_tipo",
        "tipo": "planta",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Planta a la mitad.",
    },
    "baya_yache": {
        "nombre": "Baya Yache",
        "efecto": "reduccion_tipo",
        "tipo": "hielo",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Hielo a la mitad.",
    },
    "baya_chople": {
        "nombre": "Baya Chople",
        "efecto": "reduccion_tipo",
        "tipo": "lucha",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Lucha a la mitad.",
    },
    "baya_kebia": {
        "nombre": "Baya Kebia",
        "efecto": "reduccion_tipo",
        "tipo": "veneno",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Veneno a la mitad.",
    },
    "baya_shuca": {
        "nombre": "Baya Shuca",
        "efecto": "reduccion_tipo",
        "tipo": "tierra",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Tierra a la mitad.",
    },
    "baya_coba": {
        "nombre": "Baya Coba",
        "efecto": "reduccion_tipo",
        "tipo": "volador",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Volador a la mitad.",
    },
    "baya_payapa": {
        "nombre": "Baya Payapa",
        "efecto": "reduccion_tipo",
        "tipo": "psiquico",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Psíquico a la mitad.",
    },
    "baya_tanga": {
        "nombre": "Baya Tanga",
        "efecto": "reduccion_tipo",
        "tipo": "bicho",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Bicho a la mitad.",
    },
    "baya_charti": {
        "nombre": "Baya Charti",
        "efecto": "reduccion_tipo",
        "tipo": "roca",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Roca a la mitad.",
    },
    "baya_colbur": {
        "nombre": "Baya Colbur",
        "efecto": "reduccion_tipo",
        "tipo": "siniestro",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Siniestro a la mitad.",
    },
    "baya_babiri": {
        "nombre": "Baya Babiri",
        "efecto": "reduccion_tipo",
        "tipo": "acero",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Acero a la mitad.",
    },
    "baya_roseli": {
        "nombre": "Baya Roseli",
        "efecto": "reduccion_tipo",
        "tipo": "hada",
        "reduccion": 0.5,
        "descripcion": "Reduce el daño de un golpe súper-efectivo de Hada a la mitad.",
    },

    # ── Utilidad / Setup ──────────────────────────────────────────────────────
    "hierba_blanca": {
        "nombre": "Hierba Blanca",
        "efecto": "restaurar_stats",
        "activacion": "bajada_stat",
        "descripcion": "Restaura las estadísticas bajadas una vez (consumible).",
    },
    "banda_focus": {
        "nombre": "Banda Focus",
        "efecto": "sobrevivir_10_pct",
        "probabilidad": 0.1,
        "descripcion": "10 % de posibilidad de sobrevivir con 1 HP a cualquier golpe.",
    },
    "polvo_celeste": {
        "nombre": "Polvo Celestial",
        "efecto": "bloquear_estados",
        "descripcion": "Impide que el portador sufra condiciones de estado.",
    },
    "panuelo_sedoso": {
        "nombre": "Pañuelo Sedoso",
        "efecto": "velocidad",
        "multiplicador_velocidad": 1.1,
        "descripcion": "Aumenta la Velocidad un 10 %.",
    },
    "tubo_exp": {
        "nombre": "Tubo EXP",
        "efecto": "ninguno",
        "descripcion": "Sin efecto en combate competitivo.",
    },
    "amuleto_aclaro": {
        "nombre": "Amuleto Claro",
        "efecto": "bloquear_bajada_stats_rival",
        "descripcion": "Impide que el rival baje las estadísticas del portador.",
    },
    "booster_energia": {
        "nombre": "Booster Energía",
        "efecto": "paradoja_boost",
        "descripcion": "Activa la habilidad Prototipo Antiguo / Motor Cuántico de Pokémon Paradoja.",
    },
}


def buscar_objeto_champions(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return OBJETOS_CHAMPIONS.get(key)


def listar_objetos_champions() -> list[str]:
    return [v["nombre"] for v in OBJETOS_CHAMPIONS.values()]
