"""
cerebros/champions/data/entrenamiento.py
Reglas de entrenamiento especificas de Pokemon Champions.

Fuente: Vandal — Guia Pokemon Champions (abril 2026).
https://vandal.elespanol.com/guias/guia-pokemon-champions-trucos-consejos-y-secretos/entrenar-y-mejorar-pokemon

Champions se aparta del sistema main series en varios aspectos clave:
- No hay IVs (todos los Pokemon parten con IVs maximos por defecto).
- EVs limitados a 32 por estadistica y 66 totales (vs. 252/508 main series).
- Todos los Pokemon estan fijos a nivel 50.
- Todas las mejoras se compran con Puntos de Victoria (PV) obtenidos en combate.
"""
from __future__ import annotations

REGLAS_ENTRENAMIENTO_CHAMPIONS: dict = {
    "nivel": {
        "fijo": 50,
        "nota": "Todos los Pokemon en Champions estan fijos al nivel 50; no hay sistema de experiencia.",
    },
    "ivs": {
        "activos": False,
        "valor_por_defecto": 31,
        "nota": "Los IVs clasicos NO existen en Champions; se considera que todos parten al maximo (31).",
    },
    "evs": {
        "max_por_stat": 32,
        "max_total": 66,
        "nota_hp": "El HP no se puede subir via naturaleza (solo via EVs).",
        "conversion": "1 EV invertido = 1 punto de stat directo.",
    },
    "naturalezas": {
        "cambio_disponible": True,
        "coste_pv": 500,
        "efecto": "+10 % / -10 % en stats (excepto HP que queda intacto).",
        "total_disponibles": 25,
    },
    "habilidades": {
        "cambio_disponible": True,
        "coste_pv": 500,
        "nota": "Solo se pueden seleccionar habilidades disponibles en Champions para ese Pokemon.",
    },
    "movimientos": {
        "cambio_disponible": True,
        "coste_pv_por_movimiento": 250,
        "nota": "Solo se pueden aprender movimientos disponibles en Champions para ese Pokemon.",
    },
    "coste_total_maximo_ev": {
        "pv_por_ev": 5,
        "pv_totales_66_evs": 330,
        "descripcion": "Para invertir los 66 puntos de EV al maximo: 66 x 5 = 330 PV.",
    },
    "moneda_entrenamiento": "Puntos de Victoria (PV)",
    "formato_competitivo": "Singles nivel 50 con EVs 66/66, IVs 31 fijos, 1 objeto, 1 habilidad, 4 movimientos.",
}
