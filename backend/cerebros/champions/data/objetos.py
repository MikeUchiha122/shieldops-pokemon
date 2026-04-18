"""
cerebros/champions/data/objetos.py
Objetos competitivos + Megapiedras para Pokemon Champions (Singles multi-gen).

Fuente objetos: Eurogamer + NextN (Pokemon Champions 1.0.2, abril 2026).
Fuente megapiedras: Vandal + Eurogamer (lista de 64 megapiedras).
"""
from __future__ import annotations

OBJETOS_CHAMPIONS: dict[str, dict] = {
    # ── Potenciadores de dano ─────────────────────────────────────────────────
    "orbe_de_vida": {
        "nombre": "Orbe de Vida",
        "efecto": "dano_propio",
        "multiplicador_ataque": 1.3,
        "recoil_porcentaje": 10,
        "descripcion": "Aumenta el dano un 30 % pero el portador pierde el 10 % de su HP max cada turno.",
    },
    "garra_eleccion": {
        "nombre": "Garra Eleccion",
        "efecto": "eleccion_fisico",
        "multiplicador_ataque_especial": None,
        "multiplicador_ataque": 1.5,
        "restriccion": "bloquea_movimiento",
        "descripcion": "Aumenta Ataque un 50 % pero solo puede usar el movimiento elegido.",
    },
    "gafas_eleccion": {
        "nombre": "Gafas Eleccion",
        "efecto": "eleccion_especial",
        "multiplicador_ataque_especial": 1.5,
        "multiplicador_ataque": None,
        "restriccion": "bloquea_movimiento",
        "descripcion": "Aumenta Atq. Especial un 50 % pero solo puede usar el movimiento elegido.",
    },
    "panuelo_eleccion": {
        "nombre": "Panuelo Eleccion",
        "efecto": "eleccion_velocidad",
        "multiplicador_velocidad": 1.5,
        "restriccion": "bloquea_movimiento",
        "descripcion": "Aumenta Velocidad un 50 % pero solo puede usar el movimiento elegido.",
    },
    "musculo_banda": {
        "nombre": "Musculo Banda",
        "efecto": "potencia_fisico",
        "multiplicador_ataque": 1.1,
        "descripcion": "Aumenta el dano de movimientos fisicos un 10 %.",
    },
    "gafas_sabias": {
        "nombre": "Gafas Sabias",
        "efecto": "potencia_especial",
        "multiplicador_ataque_especial": 1.1,
        "descripcion": "Aumenta el dano de movimientos especiales un 10 %.",
    },
    "placa_negra": {
        "nombre": "Placa Negra",
        "efecto": "tipo_boost",
        "tipo": "siniestro",
        "multiplicador": 1.2,
        "descripcion": "Aumenta el dano de movimientos de tipo Siniestro un 20 %.",
    },
    "carbon": {
        "nombre": "Carbon",
        "efecto": "tipo_boost",
        "tipo": "fuego",
        "multiplicador": 1.2,
        "descripcion": "Aumenta el dano de movimientos de tipo Fuego un 20 %.",
    },
    "gema_dragon": {
        "nombre": "Gema Dragon",
        "efecto": "tipo_boost_consumible",
        "tipo": "dragon",
        "multiplicador": 1.3,
        "usos": 1,
        "descripcion": "Potencia el primer movimiento de tipo Dragon un 30 % (consumible).",
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
        "nombre": "Fajin Focus",
        "efecto": "sobrevivir_1hp",
        "condicion": "hp_lleno",
        "descripcion": "Si el Pokemon tiene el HP lleno, sobrevive con 1 HP a cualquier golpe.",
    },
    "bayas_sitrus": {
        "nombre": "Bayas Sitrus",
        "efecto": "cura_hp",
        "cura_porcentaje": 25,
        "activacion": "hp_por_debajo_50",
        "descripcion": "Restaura el 25 % del HP max cuando el HP cae por debajo del 50 %.",
    },
    "bayas_frambu": {
        "nombre": "Bayas Frambu",
        "efecto": "cura_hp",
        "cura_porcentaje": 50,
        "activacion": "hp_por_debajo_25",
        "descripcion": "Restaura el 50 % del HP max cuando el HP cae por debajo del 25 %.",
    },
    "resto_sobras": {
        "nombre": "Restos",
        "efecto": "regeneracion",
        "cura_porcentaje_por_turno": 6.25,
        "descripcion": "Restaura 1/16 del HP max al final de cada turno.",
    },
    "casco_rocoso": {
        "nombre": "Casco Rocoso",
        "efecto": "recoil_contacto",
        "dano_recoil_porcentaje": 16.67,
        "descripcion": "Inflige el 1/6 del HP del portador como dano a quien lo golpee con contacto.",
    },
    "balon_aire": {
        "nombre": "Globo Aire",
        "efecto": "inmunidad_tierra",
        "descripcion": "Hace inmune a movimientos de Tierra; se rompe al recibir cualquier dano.",
    },
    "escudo_mental": {
        "nombre": "Escudo Mental",
        "efecto": "absorber_boost",
        "descripcion": "Absorbe las bajadas de stats causadas por el oponente.",
    },

    # ── Berries curativas y de reduccion de tipo ─────────────────────────────
    "baya_cheri": {
        "nombre": "Baya Cheri",
        "efecto": "cura_estado",
        "cura": "paralisis",
        "descripcion": "Cura la paralisis al activarse.",
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
    "baya_occa":    {"nombre":"Baya Occa","efecto":"reduccion_tipo","tipo":"fuego","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Fuego a la mitad."},
    "baya_passho":  {"nombre":"Baya Passho","efecto":"reduccion_tipo","tipo":"agua","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Agua a la mitad."},
    "baya_wacan":   {"nombre":"Baya Wacan","efecto":"reduccion_tipo","tipo":"electrico","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Electrico a la mitad."},
    "baya_rindo":   {"nombre":"Baya Rindo","efecto":"reduccion_tipo","tipo":"planta","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Planta a la mitad."},
    "baya_yache":   {"nombre":"Baya Yache","efecto":"reduccion_tipo","tipo":"hielo","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Hielo a la mitad."},
    "baya_chople":  {"nombre":"Baya Chople","efecto":"reduccion_tipo","tipo":"lucha","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Lucha a la mitad."},
    "baya_kebia":   {"nombre":"Baya Kebia","efecto":"reduccion_tipo","tipo":"veneno","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Veneno a la mitad."},
    "baya_shuca":   {"nombre":"Baya Shuca","efecto":"reduccion_tipo","tipo":"tierra","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Tierra a la mitad."},
    "baya_coba":    {"nombre":"Baya Coba","efecto":"reduccion_tipo","tipo":"volador","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Volador a la mitad."},
    "baya_payapa":  {"nombre":"Baya Payapa","efecto":"reduccion_tipo","tipo":"psiquico","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Psiquico a la mitad."},
    "baya_tanga":   {"nombre":"Baya Tanga","efecto":"reduccion_tipo","tipo":"bicho","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Bicho a la mitad."},
    "baya_charti":  {"nombre":"Baya Charti","efecto":"reduccion_tipo","tipo":"roca","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Roca a la mitad."},
    "baya_colbur":  {"nombre":"Baya Colbur","efecto":"reduccion_tipo","tipo":"siniestro","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Siniestro a la mitad."},
    "baya_babiri":  {"nombre":"Baya Babiri","efecto":"reduccion_tipo","tipo":"acero","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Acero a la mitad."},
    "baya_roseli":  {"nombre":"Baya Roseli","efecto":"reduccion_tipo","tipo":"hada","reduccion":0.5,"descripcion":"Reduce el dano de un golpe super-efectivo de Hada a la mitad."},

    # ── Utilidad / Setup ──────────────────────────────────────────────────────
    "hierba_blanca": {
        "nombre": "Hierba Blanca",
        "efecto": "restaurar_stats",
        "activacion": "bajada_stat",
        "descripcion": "Restaura las estadisticas bajadas una vez (consumible).",
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
        "nombre": "Panuelo Sedoso",
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
        "descripcion": "Impide que el rival baje las estadisticas del portador.",
    },
    "booster_energia": {
        "nombre": "Booster Energia",
        "efecto": "paradoja_boost",
        "descripcion": "Activa la habilidad Prototipo Antiguo / Motor Cuantico de Pokemon Paradoja.",
    },

    # ── Bayas curativas adicionales (Pokemon Champions) ──────────────────────
    "baya_zreza": {"nombre": "Baya Zreza", "efecto": "cura_estado", "cura": "suenio", "descripcion": "Cura el suenio al activarse."},
    "baya_atania": {"nombre": "Baya Atania", "efecto": "cura_estado", "cura": "confusion", "descripcion": "Cura la confusion al activarse."},
    "baya_meloc": {"nombre": "Baya Meloc", "efecto": "cura_estado", "cura": "paralisis", "descripcion": "Cura la paralisis (variante de cheri). Raiz para competitivo."},
    "baya_safre": {"nombre": "Baya Safre", "efecto": "cura_estado", "cura": "congelacion", "descripcion": "Cura la congelacion al activarse."},
    "baya_perasi": {"nombre": "Baya Perasi", "efecto": "cura_estado", "cura": "todos_menores", "descripcion": "Cura cualquier estado menor."},
    "baya_ziuela": {"nombre": "Baya Ziuela", "efecto": "cura_estado", "cura": "todos", "descripcion": "Cura todos los problemas de estado al activarse."},
    "baya_zidra": {"nombre": "Baya Zidra", "efecto": "cura_hp_pct", "cura": "hp_por_debajo_50", "descripcion": "Restaura 1/4 del HP maximo al caer por debajo del 50 % de HP."},
    "baya_aranja": {"nombre": "Baya Aranja", "efecto": "cura_hp_fijo", "cura": "hp_por_debajo_50", "descripcion": "Cura 10 HP al caer a la mitad de vida."},

    # ── Objetos de potencia de tipo (+20 %) ──────────────────────────────────
    "iman": {"nombre": "Iman", "efecto": "tipo_boost", "tipo": "electrico", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Electrico un 20 %."},
    "agua_mistica": {"nombre": "Agua Mistica", "efecto": "tipo_boost", "tipo": "agua", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Agua un 20 %."},
    "pico_afilado": {"nombre": "Pico Afilado", "efecto": "tipo_boost", "tipo": "volador", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Volador un 20 %."},
    "piedra_dura": {"nombre": "Piedra Dura", "efecto": "tipo_boost", "tipo": "roca", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Roca un 20 %."},
    "pua_veneno": {"nombre": "Pua Venenosa", "efecto": "tipo_boost", "tipo": "veneno", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Veneno un 20 %."},
    "seda_insecto": {"nombre": "Seda Insecto", "efecto": "tipo_boost", "tipo": "bicho", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Bicho un 20 %."},
    "cinta_fantasma": {"nombre": "Cinta Fantasma", "efecto": "tipo_boost", "tipo": "fantasma", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Fantasma un 20 %."},
    "pieza_metalica": {"nombre": "Pieza Metalica", "efecto": "tipo_boost", "tipo": "acero", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Acero un 20 %."},
    "hechizo_hada": {"nombre": "Hechizo Hada", "efecto": "tipo_boost", "tipo": "hada", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Hada un 20 %."},
    "semilla_milagrosa": {"nombre": "Semilla Milagrosa", "efecto": "tipo_boost", "tipo": "planta", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Planta un 20 %."},
    "roca_suave": {"nombre": "Roca Suave", "efecto": "tipo_boost", "tipo": "hielo", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Hielo un 20 %."},
    "cinta_siniestra": {"nombre": "Cinta Siniestra", "efecto": "tipo_boost", "tipo": "siniestro", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Siniestro un 20 %."},
    "aguijon_rey": {"nombre": "Aguijon Rey", "efecto": "tipo_boost", "tipo": "tierra", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Tierra un 20 %."},
    "puno_experto": {"nombre": "Puno Experto", "efecto": "tipo_boost", "tipo": "lucha", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Lucha un 20 %."},
    "cuchara_torcida": {"nombre": "Cuchara Torcida", "efecto": "tipo_boost", "tipo": "psiquico", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Psiquico un 20 %."},
    "cinta_normal": {"nombre": "Cinta Normal", "efecto": "tipo_boost", "tipo": "normal", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Normal un 20 %."},
    "escama_dragon": {"nombre": "Escama Dragon", "efecto": "tipo_boost", "tipo": "dragon", "multiplicador": 1.2, "descripcion": "Aumenta el dano de movimientos de tipo Dragon un 20 %."},

    # ── Objetos especiales competitivos ──────────────────────────────────────
    "garra_rapida": {"nombre": "Garra Rapida", "efecto": 'prioridad_probabilidad', "probabilidad": 0.2, "descripcion": '20 % de probabilidad de atacar primero independientemente de la velocidad.'},
    "cinta_aguante": {"nombre": "Cinta Aguante", "efecto": 'sobrevivir_1hp_pct', "probabilidad": 0.1, "descripcion": '10 % de probabilidad de sobrevivir con 1 HP a un ataque letal.'},
    "banda_aguante": {"nombre": "Banda Aguante", "efecto": 'sobrevivir_1hp', "condicion": 'hp_lleno', "descripcion": 'Si el portador esta con el HP al maximo, sobrevive con 1 HP a cualquier ataque letal.'},
    "botas_gruesas": {"nombre": "Botas Gruesas", "efecto": 'inmune_entry_hazards', "descripcion": 'Inmune a Puas, Puas Toxicas, Trampa Rocas y Red Viscosa al entrar.'},
    "chaleco_asalto": {"nombre": "Chaleco Asalto", "efecto": 'resistencia_especial', "multiplicador_defensa_especial": 1.5, "restriccion": 'no_puede_usar_estados', "descripcion": 'Aumenta Def. Especial un 50 % pero impide usar movimientos de estado.'},
    "herb_estimulante": {"nombre": "Hierba Mental", "efecto": 'cura_confusion_automatico', "descripcion": 'Cura la confusion al activarse (consumible, una sola vez).'},
    "herb_poder": {"nombre": "Hierba Poder", "efecto": 'precarga_ataque', "descripcion": 'Permite usar en un turno un ataque que normalmente requiere dos (consumible).'},

    # ── MEGAPIEDRAS (64 disponibles en Pokemon Champions) ────────────────────
    "venusaurita": {"nombre": "Venusaurita", "efecto": "megapiedra", "pokemon": "Venusaur", "mega_forma": "mega_venusaur_ch", "descripcion": "Permite la Mega Evolucion de Venusaur durante el combate."},
    "charizardita_x": {"nombre": "Charizardita X", "efecto": "megapiedra", "pokemon": "Charizard", "mega_forma": "mega_charizard_x_ch", "descripcion": "Permite la Mega Evolucion de Charizard durante el combate."},
    "charizardita_y": {"nombre": "Charizardita Y", "efecto": "megapiedra", "pokemon": "Charizard", "mega_forma": "mega_charizard_y_ch", "descripcion": "Permite la Mega Evolucion de Charizard durante el combate."},
    "blastoisita": {"nombre": "Blastoisita", "efecto": "megapiedra", "pokemon": "Blastoise", "mega_forma": "mega_blastoise_ch", "descripcion": "Permite la Mega Evolucion de Blastoise durante el combate."},
    "beedrillita": {"nombre": "Beedrillita", "efecto": "megapiedra", "pokemon": "Beedrill", "mega_forma": "mega_beedrill_ch", "descripcion": "Permite la Mega Evolucion de Beedrill durante el combate."},
    "pidgeotita": {"nombre": "Pidgeotita", "efecto": "megapiedra", "pokemon": "Pidgeot", "mega_forma": "mega_pidgeot_ch", "descripcion": "Permite la Mega Evolucion de Pidgeot durante el combate."},
    "alakazamita": {"nombre": "Alakazamita", "efecto": "megapiedra", "pokemon": "Alakazam", "mega_forma": "mega_alakazam_ch", "descripcion": "Permite la Mega Evolucion de Alakazam durante el combate."},
    "slowbronita": {"nombre": "Slowbronita", "efecto": "megapiedra", "pokemon": "Slowbro", "mega_forma": "mega_slowbro_ch", "descripcion": "Permite la Mega Evolucion de Slowbro durante el combate."},
    "gengarita": {"nombre": "Gengarita", "efecto": "megapiedra", "pokemon": "Gengar", "mega_forma": "mega_gengar_ch", "descripcion": "Permite la Mega Evolucion de Gengar durante el combate."},
    "kangaskhanita": {"nombre": "Kangaskhanita", "efecto": "megapiedra", "pokemon": "Kangaskhan", "mega_forma": "mega_kangaskhan_ch", "descripcion": "Permite la Mega Evolucion de Kangaskhan durante el combate."},
    "pinsirita": {"nombre": "Pinsirita", "efecto": "megapiedra", "pokemon": "Pinsir", "mega_forma": "mega_pinsir_ch", "descripcion": "Permite la Mega Evolucion de Pinsir durante el combate."},
    "gyaradosita": {"nombre": "Gyaradosita", "efecto": "megapiedra", "pokemon": "Gyarados", "mega_forma": "mega_gyarados_ch", "descripcion": "Permite la Mega Evolucion de Gyarados durante el combate."},
    "aerodactylita": {"nombre": "Aerodactylita", "efecto": "megapiedra", "pokemon": "Aerodactyl", "mega_forma": "mega_aerodactyl_ch", "descripcion": "Permite la Mega Evolucion de Aerodactyl durante el combate."},
    "ampharosita": {"nombre": "Ampharosita", "efecto": "megapiedra", "pokemon": "Ampharos", "mega_forma": "mega_ampharos_ch", "descripcion": "Permite la Mega Evolucion de Ampharos durante el combate."},
    "steelixita": {"nombre": "Steelixita", "efecto": "megapiedra", "pokemon": "Steelix", "mega_forma": "mega_steelix_ch", "descripcion": "Permite la Mega Evolucion de Steelix durante el combate."},
    "scizorita": {"nombre": "Scizorita", "efecto": "megapiedra", "pokemon": "Scizor", "mega_forma": "mega_scizor_ch", "descripcion": "Permite la Mega Evolucion de Scizor durante el combate."},
    "heracronita": {"nombre": "Heracronita", "efecto": "megapiedra", "pokemon": "Heracross", "mega_forma": "mega_heracross_ch", "descripcion": "Permite la Mega Evolucion de Heracross durante el combate."},
    "houndoomita": {"nombre": "Houndoomita", "efecto": "megapiedra", "pokemon": "Houndoom", "mega_forma": "mega_houndoom_ch", "descripcion": "Permite la Mega Evolucion de Houndoom durante el combate."},
    "tyranitarita": {"nombre": "Tyranitarita", "efecto": "megapiedra", "pokemon": "Tyranitar", "mega_forma": "mega_tyranitar_ch", "descripcion": "Permite la Mega Evolucion de Tyranitar durante el combate."},
    "gardevoirita": {"nombre": "Gardevoirita", "efecto": "megapiedra", "pokemon": "Gardevoir", "mega_forma": "mega_gardevoir_ch", "descripcion": "Permite la Mega Evolucion de Gardevoir durante el combate."},
    "sableynita": {"nombre": "Sableynita", "efecto": "megapiedra", "pokemon": "Sableye", "mega_forma": "mega_sableye_ch", "descripcion": "Permite la Mega Evolucion de Sableye durante el combate."},
    "mawilita": {"nombre": "Mawilita", "efecto": "megapiedra", "pokemon": "Mawile", "mega_forma": "mega_mawile_ch", "descripcion": "Permite la Mega Evolucion de Mawile durante el combate."},
    "aggronita": {"nombre": "Aggronita", "efecto": "megapiedra", "pokemon": "Aggron", "mega_forma": "mega_aggron_ch", "descripcion": "Permite la Mega Evolucion de Aggron durante el combate."},
    "medichamita": {"nombre": "Medichamita", "efecto": "megapiedra", "pokemon": "Medicham", "mega_forma": "mega_medicham_ch", "descripcion": "Permite la Mega Evolucion de Medicham durante el combate."},
    "manectricita": {"nombre": "Manectricita", "efecto": "megapiedra", "pokemon": "Manectric", "mega_forma": "mega_manectric_ch", "descripcion": "Permite la Mega Evolucion de Manectric durante el combate."},
    "sharpedonita": {"nombre": "Sharpedonita", "efecto": "megapiedra", "pokemon": "Sharpedo", "mega_forma": "mega_sharpedo_ch", "descripcion": "Permite la Mega Evolucion de Sharpedo durante el combate."},
    "cameruptita": {"nombre": "Cameruptita", "efecto": "megapiedra", "pokemon": "Camerupt", "mega_forma": "mega_camerupt_ch", "descripcion": "Permite la Mega Evolucion de Camerupt durante el combate."},
    "altariaita": {"nombre": "Altariaita", "efecto": "megapiedra", "pokemon": "Altaria", "mega_forma": "mega_altaria_ch", "descripcion": "Permite la Mega Evolucion de Altaria durante el combate."},
    "banettita": {"nombre": "Banettita", "efecto": "megapiedra", "pokemon": "Banette", "mega_forma": "mega_banette_ch", "descripcion": "Permite la Mega Evolucion de Banette durante el combate."},
    "absolita": {"nombre": "Absolita", "efecto": "megapiedra", "pokemon": "Absol", "mega_forma": "mega_absol_ch", "descripcion": "Permite la Mega Evolucion de Absol durante el combate."},
    "glalita": {"nombre": "Glalita", "efecto": "megapiedra", "pokemon": "Glalie", "mega_forma": "mega_glalie_ch", "descripcion": "Permite la Mega Evolucion de Glalie durante el combate."},
    "salamencita": {"nombre": "Salamencita", "efecto": "megapiedra", "pokemon": "Salamence", "mega_forma": "mega_salamence_ch", "descripcion": "Permite la Mega Evolucion de Salamence durante el combate."},
    "metagrossita": {"nombre": "Metagrossita", "efecto": "megapiedra", "pokemon": "Metagross", "mega_forma": "mega_metagross_ch", "descripcion": "Permite la Mega Evolucion de Metagross durante el combate."},
    "latiosita": {"nombre": "Latiosita", "efecto": "megapiedra", "pokemon": "Latios", "mega_forma": "mega_latios_ch", "descripcion": "Permite la Mega Evolucion de Latios durante el combate."},
    "latiasita": {"nombre": "Latiasita", "efecto": "megapiedra", "pokemon": "Latias", "mega_forma": "mega_latias_ch", "descripcion": "Permite la Mega Evolucion de Latias durante el combate."},
    "lopunnyita": {"nombre": "Lopunnyita", "efecto": "megapiedra", "pokemon": "Lopunny", "mega_forma": "mega_lopunny_ch", "descripcion": "Permite la Mega Evolucion de Lopunny durante el combate."},
    "garchompita": {"nombre": "Garchompita", "efecto": "megapiedra", "pokemon": "Garchomp", "mega_forma": "mega_garchomp_ch", "descripcion": "Permite la Mega Evolucion de Garchomp durante el combate."},
    "lucarionita": {"nombre": "Lucarionita", "efecto": "megapiedra", "pokemon": "Lucario", "mega_forma": "mega_lucario_ch", "descripcion": "Permite la Mega Evolucion de Lucario durante el combate."},
    "abomasnowita": {"nombre": "Abomasnowita", "efecto": "megapiedra", "pokemon": "Abomasnow", "mega_forma": "mega_abomasnow_ch", "descripcion": "Permite la Mega Evolucion de Abomasnow durante el combate."},
    "galladita": {"nombre": "Galladita", "efecto": "megapiedra", "pokemon": "Gallade", "mega_forma": "mega_gallade_ch", "descripcion": "Permite la Mega Evolucion de Gallade durante el combate."},
    "audinita": {"nombre": "Audinita", "efecto": "megapiedra", "pokemon": "Audino", "mega_forma": "mega_audino_ch", "descripcion": "Permite la Mega Evolucion de Audino durante el combate."},
    "dragonitita": {"nombre": "Dragonitita", "efecto": "megapiedra", "pokemon": "Dragonite", "mega_forma": "mega_dragonite_ch", "descripcion": "Permite la Mega Evolucion de Dragonite durante el combate."},
    "meganiumita": {"nombre": "Meganiumita", "efecto": "megapiedra", "pokemon": "Meganium", "mega_forma": "mega_meganium_ch", "descripcion": "Permite la Mega Evolucion de Meganium durante el combate."},
    "feraligatrita": {"nombre": "Feraligatrita", "efecto": "megapiedra", "pokemon": "Feraligatr", "mega_forma": "mega_feraligatr_ch", "descripcion": "Permite la Mega Evolucion de Feraligatr durante el combate."},
    "emboarita": {"nombre": "Emboarita", "efecto": "megapiedra", "pokemon": "Emboar", "mega_forma": "mega_emboar_ch", "descripcion": "Permite la Mega Evolucion de Emboar durante el combate."},
    "excadrillita": {"nombre": "Excadrillita", "efecto": "megapiedra", "pokemon": "Excadrill", "mega_forma": "mega_excadrill_ch", "descripcion": "Permite la Mega Evolucion de Excadrill durante el combate."},
    "chandelurita": {"nombre": "Chandelurita", "efecto": "megapiedra", "pokemon": "Chandelure", "mega_forma": "mega_chandelure_ch", "descripcion": "Permite la Mega Evolucion de Chandelure durante el combate."},
    "golurkita": {"nombre": "Golurkita", "efecto": "megapiedra", "pokemon": "Golurk", "mega_forma": "mega_golurk_ch", "descripcion": "Permite la Mega Evolucion de Golurk durante el combate."},
    "chesnaughtita": {"nombre": "Chesnaughtita", "efecto": "megapiedra", "pokemon": "Chesnaught", "mega_forma": "mega_chesnaught_ch", "descripcion": "Permite la Mega Evolucion de Chesnaught durante el combate."},
    "delphoxita": {"nombre": "Delphoxita", "efecto": "megapiedra", "pokemon": "Delphox", "mega_forma": "mega_delphox_ch", "descripcion": "Permite la Mega Evolucion de Delphox durante el combate."},
    "greninjita": {"nombre": "Greninjita", "efecto": "megapiedra", "pokemon": "Greninja", "mega_forma": "mega_greninja_ch", "descripcion": "Permite la Mega Evolucion de Greninja durante el combate."},
    "floettita": {"nombre": "Floettita", "efecto": "megapiedra", "pokemon": "Floette Flor Eterna", "mega_forma": "mega_floette_ch", "descripcion": "Permite la Mega Evolucion de Floette Flor Eterna durante el combate."},
    "meowsticita": {"nombre": "Meowsticita", "efecto": "megapiedra", "pokemon": "Meowstic", "mega_forma": "mega_meowstic_ch", "descripcion": "Permite la Mega Evolucion de Meowstic durante el combate."},
    "hawluchita": {"nombre": "Hawluchita", "efecto": "megapiedra", "pokemon": "Hawlucha", "mega_forma": "mega_hawlucha_ch", "descripcion": "Permite la Mega Evolucion de Hawlucha durante el combate."},
    "crabominablita": {"nombre": "Crabominablita", "efecto": "megapiedra", "pokemon": "Crabominable", "mega_forma": "mega_crabominable_ch", "descripcion": "Permite la Mega Evolucion de Crabominable durante el combate."},
    "drampita": {"nombre": "Drampita", "efecto": "megapiedra", "pokemon": "Drampa", "mega_forma": "mega_drampa_ch", "descripcion": "Permite la Mega Evolucion de Drampa durante el combate."},
    "scovillainita": {"nombre": "Scovillainita", "efecto": "megapiedra", "pokemon": "Scovillain", "mega_forma": "mega_scovillain_ch", "descripcion": "Permite la Mega Evolucion de Scovillain durante el combate."},
    "glimmorita": {"nombre": "Glimmorita", "efecto": "megapiedra", "pokemon": "Glimmora", "mega_forma": "mega_glimmora_ch", "descripcion": "Permite la Mega Evolucion de Glimmora durante el combate."},
    "victreebelita": {"nombre": "Victreebelita", "efecto": "megapiedra", "pokemon": "Victreebel", "mega_forma": "mega_victreebel_ch", "descripcion": "Permite la Mega Evolucion de Victreebel durante el combate."},
    "starmita": {"nombre": "Starmita", "efecto": "megapiedra", "pokemon": "Starmie", "mega_forma": "mega_starmie_ch", "descripcion": "Permite la Mega Evolucion de Starmie durante el combate."},
    "clefablita": {"nombre": "Clefablita", "efecto": "megapiedra", "pokemon": "Clefable", "mega_forma": "mega_clefable_ch", "descripcion": "Permite la Mega Evolucion de Clefable durante el combate."},
    "chimechita": {"nombre": "Chimechita", "efecto": "megapiedra", "pokemon": "Chimecho", "mega_forma": "mega_chimecho_ch", "descripcion": "Permite la Mega Evolucion de Chimecho durante el combate."},
    "skarmorita": {"nombre": "Skarmorita", "efecto": "megapiedra", "pokemon": "Skarmory", "mega_forma": "mega_skarmory_ch", "descripcion": "Permite la Mega Evolucion de Skarmory durante el combate."},
    "froslassita": {"nombre": "Froslassita", "efecto": "megapiedra", "pokemon": "Froslass", "mega_forma": "mega_froslass_ch", "descripcion": "Permite la Mega Evolucion de Froslass durante el combate."},
}


def buscar_objeto_champions(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return OBJETOS_CHAMPIONS.get(key)


def listar_objetos_champions() -> list[str]:
    return [v["nombre"] for v in OBJETOS_CHAMPIONS.values()]


def listar_megapiedras_champions() -> list[dict]:
    """Lista todas las megapiedras con el Pokemon al que pertenecen."""
    return [
        {"megapiedra": v["nombre"], "pokemon": v.get("pokemon"), "mega_forma": v.get("mega_forma")}
        for v in OBJETOS_CHAMPIONS.values()
        if v.get("efecto") == "megapiedra"
    ]
