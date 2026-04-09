"""
cerebros/lza/engine/damage.py
Motor de daño para Leyendas Z-A — Action Time PvP.

Diferencias clave vs EyP:
- Habilidades DESACTIVADAS: efectividad solo por tipo elemental base.
- Sin IVs/EVs/naturaleza: stats fijas del Pokémon.
- Parálisis multiplica cooldown x1.5.
- Quemadura reduce daño físico x0.5.
- startup_frames determina si el defensor puede esquivar.
- La Mega Evolución cambia tipos y stats activos.

Fórmula simplificada LZA (basada en mecánica de acción):
  Daño = floor(Potencia * (Ataque / Defensa) * STAB * Efectividad * ModEstado)
"""
from __future__ import annotations
import math
from core.types import TipoElemental, efectividad_base
from cerebros.lza.models.schemas import (
    PokemonLZA, MovimientoLZA, CategoriaMovimientoLZA,
    EstadoAlteradoLZA, PeticionCalculoDanoLZA, ResultadoDanoLZA,
)

# Umbral de frames: si startup_frames > este valor, el defensor PUEDE esquivar
_UMBRAL_ESQUIVE_FRAMES = 12

# STAB en LZA: x1.5 (sin Adaptable, sin Tera)
_STAB_LZA = 1.5

# Parálisis: cooldown x1.5
_MULT_PARALISIS_COOLDOWN = 1.5

# Quemadura: daño físico x0.5
_MULT_QUEMADURA_FISICO = 0.5


def efectividad_lza(
    tipo_mov: TipoElemental,
    tipos_defensor: list[TipoElemental],
) -> float:
    """
    Efectividad en LZA: SOLO por tipo elemental base.
    Habilidades como Levitación NO tienen efecto aquí.
    """
    mult = 1.0
    for t in tipos_defensor:
        mult *= efectividad_base(tipo_mov, t)
    return mult


def cooldown_efectivo(mov: MovimientoLZA, estado: EstadoAlteradoLZA) -> int:
    """Cooldown real en ms, aplicando penalización de parálisis."""
    cd = mov.cooldown_ms
    if estado == EstadoAlteradoLZA.PARALIZADO:
        cd = math.ceil(cd * _MULT_PARALISIS_COOLDOWN)
    return cd


def calcular_dano(req: PeticionCalculoDanoLZA) -> ResultadoDanoLZA:
    atk = req.atacante
    defn = req.defensor
    mov = req.movimiento

    hp_max_defensor = defn.stats_activos.hp

    # Movimientos de estado no hacen daño
    if mov.categoria == CategoriaMovimientoLZA.ESTADO or mov.potencia is None:
        return ResultadoDanoLZA(
            atacante=atk.nombre, defensor=defn.nombre, movimiento=mov.nombre,
            dano=0, dano_con_estado=0, porcentaje_hp=0.0,
            efectividad=0.0, stab_aplicado=False, es_ohko=False,
            cooldown_efectivo_ms=cooldown_efectivo(mov, atk.estado),
            puede_esquivar=mov.startup_frames > _UMBRAL_ESQUIVE_FRAMES,
        )

    es_fisico = mov.categoria in (
        CategoriaMovimientoLZA.RAPIDO,
        CategoriaMovimientoLZA.CARGADO,
        CategoriaMovimientoLZA.AOE,
    )

    atq_stat = atk.stats_activos.ataque
    def_stat = defn.stats_activos.defensa

    # Si el defensor está dormido/congelado no puede esquivar
    puede_esquivar = (
        mov.startup_frames > _UMBRAL_ESQUIVE_FRAMES
        and defn.estado not in (EstadoAlteradoLZA.DORMIDO, EstadoAlteradoLZA.CONGELADO)
    )
    if req.defensor_esquivando and puede_esquivar:
        return ResultadoDanoLZA(
            atacante=atk.nombre, defensor=defn.nombre, movimiento=mov.nombre,
            dano=0, dano_con_estado=0, porcentaje_hp=0.0,
            efectividad=0.0, stab_aplicado=False, es_ohko=False,
            cooldown_efectivo_ms=cooldown_efectivo(mov, atk.estado),
            puede_esquivar=True,
        )

    eff = efectividad_lza(mov.tipo, defn.tipos_activos)
    stab = _STAB_LZA if mov.tipo in atk.tipos_activos else 1.0

    dano_base = math.floor(mov.potencia * (atq_stat / def_stat) * stab * eff)

    # Estado del atacante: quemadura reduce daño físico
    mod_estado = 1.0
    if req.quemadura_activa or atk.estado == EstadoAlteradoLZA.QUEMADO:
        if es_fisico:
            mod_estado = _MULT_QUEMADURA_FISICO

    dano_final = math.floor(dano_base * mod_estado)
    hp_actual = defn.hp_actual if defn.hp_actual is not None else hp_max_defensor

    return ResultadoDanoLZA(
        atacante=atk.nombre,
        defensor=defn.nombre,
        movimiento=mov.nombre,
        dano=dano_base,
        dano_con_estado=dano_final,
        porcentaje_hp=round(dano_final / hp_max_defensor * 100, 1),
        efectividad=eff,
        stab_aplicado=stab > 1.0,
        es_ohko=dano_final >= hp_actual,
        cooldown_efectivo_ms=cooldown_efectivo(mov, atk.estado),
        puede_esquivar=puede_esquivar,
    )
