"""
cerebros/go/engine/damage.py
Motor de daño para Pokémon GO — Tap Battle System.

Fórmula oficial GO:
  Dano = floor(0.5 * Potencia * (Ataque_eff / Defensa_eff) * STAB * TypeEff) + 1

Multiplicadores GO (distintos de EyP y LZA):
  STAB:         x1.2  (no x1.5)
  Super eficaz: x1.6  (no x2.0)
  Poco eficaz:  x0.625
  Inmune*:      x0.391 (NO es 0 — en GO no existen inmunidades reales)
  Doble SE:     x2.56  (1.6 * 1.6)
  Doble PE:     x0.391 (0.625 * 0.625)
  Shadow Atk:   x1.2
  Shadow Def:   x0.833
  Escudo:       reduce dano a 1 HP
"""
from __future__ import annotations
import math
from core.types import TipoElemental, efectividad_base, TABLA_EFECTIVIDAD
from cerebros.go.models.schemas import (
    PokemonGO, MovimientoGO, CategoriaMovimientoGO,
    PeticionDanoGO, ResultadoDanoGO,
)

# Multiplicadores únicos de Pokémon GO
_STAB_GO         = 1.2
_SUPER_EFICAZ_GO = 1.6
_POCO_EFICAZ_GO  = 0.625
_INMUNE_GO       = 0.391   # En GO "inmune" es 0.391, NO cero


def efectividad_go(
    tipo_mov: TipoElemental,
    tipos_defensor: list[TipoElemental],
) -> float:
    """
    Calcula efectividad con multiplicadores de GO.
    Los valores base (2, 0.5, 0) se mapean a los valores GO reales.
    """
    mult = 1.0
    for t in tipos_defensor:
        base = efectividad_base(tipo_mov, t)
        if base == 2.0:
            mult *= _SUPER_EFICAZ_GO
        elif base == 0.5:
            mult *= _POCO_EFICAZ_GO
        elif base == 0.0:
            mult *= _INMUNE_GO
        # base == 1.0 -> mult *= 1.0 (sin cambio)
    return round(mult, 6)


def calcular_dano(req: PeticionDanoGO) -> ResultadoDanoGO:
    """
    Fórmula oficial:
    Dano = floor(0.5 * Potencia * (Atq_eff / Def_eff) * STAB * TypeEff) + 1
    """
    atk  = req.atacante
    defn = req.defensor
    mov  = req.movimiento

    hp_max_defensor = defn.hp_maximo
    hp_actual = defn.hp_actual if defn.hp_actual is not None else hp_max_defensor

    # Movimientos de estado sin potencia
    if mov.potencia == 0:
        return ResultadoDanoGO(
            atacante=atk.nombre, defensor=defn.nombre, movimiento=mov.nombre,
            dano=0, porcentaje_hp=0.0, efectividad=0.0,
            stab_aplicado=False, escudo_usado=False,
            energia_generada=mov.energia if mov.categoria == CategoriaMovimientoGO.RAPIDO else 0,
            es_ohko=False, hp_defensor_restante=hp_actual,
        )

    atq_eff = atk.ataque_efectivo
    def_eff = defn.defensa_efectiva

    stab = _STAB_GO if mov.tipo in atk.tipos else 1.0
    eff  = efectividad_go(mov.tipo, defn.tipos)

    dano = math.floor(0.5 * mov.potencia * (atq_eff / def_eff) * stab * eff) + 1

    # Escudo: reduce el daño a exactamente 1 HP
    escudo_activado = False
    if req.defensor_usa_escudo and mov.categoria == CategoriaMovimientoGO.CARGADO:
        dano = 1
        escudo_activado = True

    hp_restante = max(0, hp_actual - dano)

    # Energía que genera el atacante con este movimiento
    energia_gen = 0
    if mov.categoria == CategoriaMovimientoGO.RAPIDO:
        energia_gen = mov.energia  # positivo

    return ResultadoDanoGO(
        atacante=atk.nombre,
        defensor=defn.nombre,
        movimiento=mov.nombre,
        dano=dano,
        porcentaje_hp=round(dano / hp_max_defensor * 100, 1),
        efectividad=eff,
        stab_aplicado=stab > 1.0,
        escudo_usado=escudo_activado,
        energia_generada=energia_gen,
        es_ohko=dano >= hp_actual,
        hp_defensor_restante=hp_restante,
    )


def calcular_cp(
    stats_base_atq: int,
    stats_base_def: int,
    stats_base_hp: int,
    iv_atq: int,
    iv_def: int,
    iv_hp: int,
    nivel: float,
) -> int:
    """
    Fórmula oficial CP de Pokémon GO:
    CP = floor(Atq_eff * sqrt(Def_eff) * sqrt(HP_eff) * CPM^2 / 10)
    Mínimo 10 CP.
    """
    from cerebros.go.models.schemas import obtener_cpm
    cpm = obtener_cpm(nivel)
    atq_eff = (stats_base_atq + iv_atq) * cpm
    def_eff = (stats_base_def + iv_def) * cpm
    hp_eff  = (stats_base_hp  + iv_hp)  * cpm
    cp = math.floor(atq_eff * math.sqrt(def_eff) * math.sqrt(hp_eff) / 10)
    return max(10, cp)


def nivel_optimo_para_liga(
    stats_base_atq: int,
    stats_base_def: int,
    stats_base_hp: int,
    iv_atq: int,
    iv_def: int,
    iv_hp: int,
    cp_cap: int,
) -> tuple[float, int]:
    """
    Encuentra el nivel más alto (en pasos de 0.5) cuyo CP no excede cp_cap.
    Retorna (nivel_optimo, cp_en_ese_nivel).
    """
    mejor_nivel = 1.0
    mejor_cp    = 10
    nivel = 1.0
    while nivel <= 51.0:
        cp = calcular_cp(stats_base_atq, stats_base_def, stats_base_hp,
                         iv_atq, iv_def, iv_hp, nivel)
        if cp <= cp_cap:
            mejor_nivel = nivel
            mejor_cp    = cp
        else:
            break  # CP solo sube con el nivel, podemos parar
        nivel = round(nivel + 0.5, 1)
    return mejor_nivel, mejor_cp
