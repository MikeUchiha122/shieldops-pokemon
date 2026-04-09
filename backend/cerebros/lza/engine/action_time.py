"""
cerebros/lza/engine/action_time.py
Motor Action Time para Leyendas Z-A.

Diferencias críticas vs EyP:
- Sin turnos. Sin habilidades. Startup frames + cooldowns.
- Inmunidades SOLO por tipo elemental base (no habilidades).
- Quemadura: daño físico ×0.5.
- Parálisis: cooldown_ms ×1.5 (movilidad reducida).
- Mega Evolution cambia tipos del Pokémon para efectividad.
"""
from __future__ import annotations
import math

from core.types import TipoElemental, efectividad_base
from cerebros.lza.models.schemas import (
    PokemonLZA, MovimientoLZA, CategoriaMovLZA, EstadoAlteradoLZA,
    PeticionDanoLZA, ResultadoDanoLZA,
    PeticionSimularFrameLZA, ResultadoFrameLZA,
    EstadoCombateLZA,
)


def efectividad_lza(
    tipo_mov: TipoElemental,
    tipos_defensor: list[TipoElemental],
) -> float:
    """
    LZA: efectividad calculada SOLO por tipos base.
    Habilidades como Levitación NO se aplican aquí.
    """
    mult = 1.0
    for t in tipos_defensor:
        mult *= efectividad_base(tipo_mov, t)
    return mult


def stat_final_lza(base: int, iv: int, nivel: int, es_hp: bool) -> int:
    """
    Fórmula de stats LZA (misma Gen IX pero sin EVs).
    HP:    floor((2×Base + IV) × Nivel / 100) + Nivel + 10
    Otro:  floor((2×Base + IV) × Nivel / 100) + 5
    Sin naturaleza en LZA (se usa la neutra por defecto).
    """
    base_calc = math.floor((2 * base + iv) * nivel / 100)
    if es_hp:
        return base_calc + nivel + 10
    return base_calc + 5


def cooldown_efectivo(mov: MovimientoLZA, estado: EstadoAlteradoLZA) -> int:
    """
    Aplica el modificador de Parálisis al cooldown.
    Parálisis → cooldown ×1.5 (redondeado hacia arriba).
    """
    cd = mov.cooldown_ms
    if estado == EstadoAlteradoLZA.PARALISIS:
        cd = math.ceil(cd * 1.5)
    return cd


def calcular_dano_lza(req: PeticionDanoLZA) -> ResultadoDanoLZA:
    """
    Cálculo de daño en LZA.
    Sin boosts de combate (no hay etapas de stat en Action Time).
    Sin pantallas. Sin clima (LZA no implementa clima en combate).
    Con STAB, efectividad por tipo, quemadura.
    """
    atk = req.atacante
    defn = req.defensor
    mov = req.movimiento

    if mov.categoria == CategoriaMovLZA.ESTADO or mov.potencia is None:
        return ResultadoDanoLZA(
            atacante=atk.nombre, defensor=defn.nombre,
            movimiento=mov.nombre, dano=0, porcentaje_hp=0.0,
            hp_defensor=_hp_lza(defn), es_ko=False,
            efectividad=0.0, stab_aplicado=False, mega_aplicado=atk.mega_activada,
            estado_bonus="movimiento de estado", cooldown_real_ms=cooldown_efectivo(mov, atk.estado),
        )

    es_fisico = mov.categoria in (CategoriaMovLZA.RAPIDO, CategoriaMovLZA.AOE)
    atk_key   = "atq_fis" if es_fisico else "atq_esp"
    def_key   = "def_fis" if es_fisico else "def_esp"

    atq_val = stat_final_lza(
        atk.stats_base[atk_key],
        getattr(atk.ivs, atk_key),
        atk.nivel, False,
    )
    def_val = stat_final_lza(
        defn.stats_base[def_key],
        getattr(defn.ivs, def_key),
        defn.nivel, False,
    )
    hp_def = _hp_lza(defn)

    # Efectividad — SOLO tipos base (habilidades desactivadas en LZA)
    tipos_defensor = defn.tipos_efectivos  # respeta Mega del defensor
    eff = efectividad_lza(mov.tipo, tipos_defensor)

    if eff == 0.0:
        return ResultadoDanoLZA(
            atacante=atk.nombre, defensor=defn.nombre,
            movimiento=mov.nombre, dano=0, porcentaje_hp=0.0,
            hp_defensor=hp_def, es_ko=False,
            efectividad=0.0, stab_aplicado=False, mega_aplicado=atk.mega_activada,
            estado_bonus="sin efecto (inmunidad de tipo)",
            cooldown_real_ms=cooldown_efectivo(mov, atk.estado),
        )

    # STAB
    tipos_atacante = atk.tipos_efectivos
    stab = 1.5 if mov.tipo in tipos_atacante else 1.0

    # Quemadura: daño físico ×0.5
    quemadura_mult = 0.5 if (es_fisico and atk.estado == EstadoAlteradoLZA.QUEMADURA) else 1.0
    estado_desc = (
        "quemadura (-50% daño físico)" if quemadura_mult == 0.5
        else "ninguno"
    )

    # Crítico ×1.5
    critico_mult = 1.5 if req.critico else 1.0

    # Daño base LZA (misma estructura Gen IX, sin roll aleatorio)
    dano_base = math.floor(
        (math.floor((2 * atk.nivel / 5 + 2) * mov.potencia * atq_val / def_val) / 50 + 2)
        * critico_mult
    )
    dano_final = math.floor(dano_base * stab * eff * quemadura_mult)
    dano_final = max(1, dano_final)  # mínimo 1 de daño si no es inmune

    return ResultadoDanoLZA(
        atacante=atk.nombre,
        defensor=defn.nombre,
        movimiento=mov.nombre,
        dano=dano_final,
        porcentaje_hp=round(dano_final / hp_def * 100, 1),
        hp_defensor=hp_def,
        es_ko=dano_final >= hp_def,
        efectividad=eff,
        stab_aplicado=stab > 1.0,
        mega_aplicado=atk.mega_activada,
        estado_bonus=estado_desc,
        cooldown_real_ms=cooldown_efectivo(mov, atk.estado),
    )


def simular_frame_priority(req: PeticionSimularFrameLZA) -> ResultadoFrameLZA:
    """
    Determina quién ataca primero en LZA.
    El tiempo efectivo de un ataque = cooldown_restante + startup_frames.
    Menor tiempo = ataca primero.
    Parálisis suma al cooldown restante.
    """
    sa_efectivo = (
        req.cooldown_restante_a
        + cooldown_efectivo(req.movimiento_a, req.pokemon_a.estado)
        + req.movimiento_a.startup_frames
    )
    sb_efectivo = (
        req.cooldown_restante_b
        + cooldown_efectivo(req.movimiento_b, req.pokemon_b.estado)
        + req.movimiento_b.startup_frames
    )

    if sa_efectivo <= sb_efectivo:
        primero = req.pokemon_a.nombre
        ventaja = sb_efectivo - sa_efectivo
        nota = f"{req.pokemon_a.nombre} ataca {ventaja}ms antes."
    else:
        primero = req.pokemon_b.nombre
        ventaja = sa_efectivo - sb_efectivo
        nota = f"{req.pokemon_b.nombre} ataca {ventaja}ms antes."

    return ResultadoFrameLZA(
        quien_ataca_primero=primero,
        ventaja_ms=ventaja,
        startup_a_efectivo=sa_efectivo,
        startup_b_efectivo=sb_efectivo,
        nota=nota,
    )


def validar_switch_lza(estado: EstadoCombateLZA, nombre_entrante: str) -> tuple[bool, str]:
    """
    Valida si se puede realizar un switch en LZA.
    Retorna (permitido, mensaje).
    """
    if estado.switches_usados >= 3:
        return False, f"Límite de 3 switches por combate alcanzado ({estado.switches_usados}/3)."
    return True, f"Switch a {nombre_entrante} permitido ({estado.switches_usados + 1}/3)."


def _hp_lza(p: PokemonLZA) -> int:
    return stat_final_lza(p.stats_base["hp"], p.ivs.hp, p.nivel, True)
