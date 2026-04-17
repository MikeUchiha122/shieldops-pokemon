"""
cerebros/lza/data/objetos.py
Objetos de Leyendas Z-A — adaptan mecánicas al sistema Action Time.
Sin Choice items ni semillas de terreno (mecánicas EyP). Sin Tera.
"""
from __future__ import annotations

OBJETOS_LZA: dict[str, dict] = {
    "orbe_de_vida": {
        "nombre": "Orbe de Vida",
        "descripcion": "Aumenta el daño ×1.3 a costa de 10% HP por acción.",
        "multiplicador_dano": 1.3, "costo_hp_pct": 0.1, "categoria": "ofensivo",
    },
    "faja_de_enfoque": {
        "nombre": "Faja de Enfoque",
        "descripcion": "Sobrevive con 1 HP si estaba a máximo.",
        "sobrevive_ohko": True, "categoria": "defensivo",
    },
    "restos": {
        "nombre": "Restos",
        "descripcion": "Recupera HP gradualmente cada 3 segundos de combate.",
        "recupera_hp_pct_cada_3s": 0.05, "categoria": "defensivo",
    },
    "baya_sitrus": {
        "nombre": "Baya Sitrus",
        "descripcion": "Recupera 25% HP cuando cae por debajo del 50%.",
        "umbral_hp": 0.5, "recupera_hp_pct": 0.25, "categoria": "defensivo",
    },
    "piedra_de_mega": {
        "nombre": "Piedra de Mega",
        "descripcion": "Activa la Mega Evolución en combate (1 vez por batalla).",
        "activa_mega": True, "categoria": "mega",
    },
    "piedra_megax": {
        "nombre": "Piedra Mega X",
        "descripcion": "Activa la Mega Evolución Forme X (Charizard, Mewtwo, etc.).",
        "activa_mega": True, "variante": "x", "categoria": "mega",
    },
    "piedra_megay": {
        "nombre": "Piedra Mega Y",
        "descripcion": "Activa la Mega Evolución Forme Y (Charizard, Mewtwo, etc.).",
        "activa_mega": True, "variante": "y", "categoria": "mega",
    },
    "turbocinta": {
        "nombre": "Turbocinta",
        "descripcion": "Reduce los cooldowns de todos los movimientos en 15%.",
        "reduccion_cooldown_pct": 0.15, "categoria": "velocidad",
    },
    "escudo_de_cristal": {
        "nombre": "Escudo de Cristal",
        "descripcion": "Bloquea el primer golpe crítico recibido.",
        "bloquea_critico": True, "un_uso": True, "categoria": "defensivo",
    },
    "amuleto_de_startup": {
        "nombre": "Amuleto de Startup",
        "descripcion": "Reduce startup_frames de todos los movimientos en 3.",
        "reduccion_startup_frames": 3, "categoria": "velocidad",
    },
    "hierba_magica": {
        "nombre": "Hierba Mágica",
        "descripcion": "Cura estados alterados automáticamente (parálisis, quemadura, etc.).",
        "cura_estados": True, "categoria": "apoyo",
    },
    "baya_chople": {
        "nombre": "Baya Chople",
        "descripcion": "Reduce daño supereficaz de tipo Lucha ×0.5.",
        "tipo_reducido": "lucha", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_haban": {
        "nombre": "Baya Haban",
        "descripcion": "Reduce daño supereficaz de tipo Dragón ×0.5.",
        "tipo_reducido": "dragon", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_yache": {
        "nombre": "Baya Yache",
        "descripcion": "Reduce daño supereficaz de tipo Hielo ×0.5.",
        "tipo_reducido": "hielo", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_wacan": {
        "nombre": "Baya Wacan",
        "descripcion": "Reduce daño supereficaz de tipo Eléctrico ×0.5.",
        "tipo_reducido": "electrico", "reduccion": 0.5, "categoria": "baya_tipo",
    },
    "baya_roseli": {
        "nombre": "Baya Roseli",
        "descripcion": "Reduce daño supereficaz de tipo Hada ×0.5.",
        "tipo_reducido": "hada", "reduccion": 0.5, "categoria": "baya_tipo",
    },
}


def buscar_objeto_lza(nombre: str) -> dict | None:
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    return OBJETOS_LZA.get(key)
