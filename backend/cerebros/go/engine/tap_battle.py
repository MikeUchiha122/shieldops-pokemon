"""
cerebros/go/engine/tap_battle.py
Motor Tap Battle para Pokémon GO.

Multiplicadores GO (distintos al juego principal):
- STAB:          ×1.2
- Super eficaz:  ×1.6
- Poco eficaz:   ×0.625
- Inmune*:       ×0.391  (* no hay inmunidades reales en GO)
- Doble SE:      ×2.56
- Doble NVE:     ×0.391
- Shadow Atk:    ×1.2
- Shadow Def:    ×0.833
- Purificado:    sin bonus en PvP

Fórmula de daño GO PvP:
  Daño = floor(0.5 × Potencia × (Atk_atacante / Def_defensor) × STAB × TypeEff) + 1

Stats en GO:
  Ataque_efectivo  = (stat_base_atk  + iv_atk)  × CPM
  Defensa_efectiva = (stat_base_def  + iv_def)   × CPM
  HP_efectivo      = floor((stat_base_hp + iv_hp) × CPM)
"""
from __future__ import annotations
import math

from core.types import TipoElemental, efectividad_base
from cerebros.go.models.schemas import (
    PokemonGO, FastMoveGO, ChargedMoveGO, LigaGO, CP_MAXIMOS,
    PeticionCalculoGO, PeticionDPSGO,
    ResultadoDanoGO, ResultadoDPSGO,
    cpm_para_nivel,
)

# ── Multiplicadores GO (no modificar sin actualizar Niantic official) ─
STAB_GO:          float = 1.2
SE_GO:            float = 1.6    # super eficaz ×1
NVE_GO:           float = 0.625  # poco eficaz ×1
INMUNE_GO:        float = 0.391  # "inmune" en GO (×0 en juego principal)
SHADOW_ATK_MULT:  float = 1.2
SHADOW_DEF_MULT:  float = 0.833


def efectividad_go(
    tipo_mov: TipoElemental,
    tipos_defensor: list[TipoElemental],
) -> float:
    """
    Efectividad en GO con multiplicadores propios.
    Combina los multiplicadores de cada tipo defensor.
    
    ×0 en la tabla base → ×0.391 en GO (no hay 0 reales).
    """
    mult = 1.0
    for t in tipos_defensor:
        base = efectividad_base(tipo_mov, t)
        # Convertir multiplicadores de juego principal a GO
        if base == 2.0:
            mult *= SE_GO
        elif base == 0.5:
            mult *= NVE_GO
        elif base == 0.0:
            mult *= INMUNE_GO
        # base == 1.0 → mult *= 1.0 (sin cambio)
    return round(mult, 4)


def stats_efectivos_go(pokemon: PokemonGO) -> tuple[float, float, int]:
    """
    Calcula Ataque, Defensa y HP efectivos para un Pokémon GO dado su nivel e IVs.
    Aplica bonus de Shadow si corresponde.
    Retorna (atk_efectivo, def_efectivo, hp_efectivo).
    """
    cpm = cpm_para_nivel(pokemon.nivel)
    base_atk = pokemon.stats_base["ataque"]
    base_def = pokemon.stats_base["defensa"]
    base_hp  = pokemon.stats_base["hp"]

    atk = (base_atk + pokemon.ivs.ataque) * cpm
    def_ = (base_def + pokemon.ivs.defensa) * cpm
    hp   = max(10, math.floor((base_hp + pokemon.ivs.hp) * cpm))

    if pokemon.es_shadow:
        atk  *= SHADOW_ATK_MULT
        def_ *= SHADOW_DEF_MULT

    return atk, def_, hp


def calcular_cp(pokemon: PokemonGO) -> int:
    """
    Fórmula oficial de CP Niantic:
    CP = floor((Atk_efectivo × Def_efectivo^0.5 × HP_efectivo^0.5 × CPM^2) / 10)
    Mínimo CP = 10.
    """
    cpm = cpm_para_nivel(pokemon.nivel)
    base_atk = pokemon.stats_base["ataque"] + pokemon.ivs.ataque
    base_def = pokemon.stats_base["defensa"] + pokemon.ivs.defensa
    base_hp  = pokemon.stats_base["hp"]     + pokemon.ivs.hp

    cp = math.floor(
        (base_atk * math.sqrt(base_def) * math.sqrt(base_hp) * cpm ** 2) / 10
    )
    return max(10, cp)


def calcular_dano_go(req: PeticionCalculoGO) -> ResultadoDanoGO:
    """
    Daño de un Charged Move en GO Battle League.
    
    Si el defensor usa escudo → daño = 1 (siempre, independiente de stats).
    """
    atk = req.atacante
    defn = req.defensor
    mov = req.move

    atk_val, _, _ = stats_efectivos_go(atk)
    _, def_val, hp_def_calc = stats_efectivos_go(defn)

    # HP efectivo del defensor
    hp_def = hp_def_calc

    # STAB
    stab = STAB_GO if mov.tipo in atk.tipos else 1.0

    # Efectividad GO
    eff = efectividad_go(mov.tipo, defn.tipos)

    # Fórmula daño GO PvP
    dano_base = math.floor(
        0.5 * mov.dano * (atk_val / def_val) * stab * eff
    ) + 1
    dano_base = max(1, dano_base)

    # Escudo: reduce a 1 de daño
    dano_final = 1 if req.usar_escudo else dano_base

    return ResultadoDanoGO(
        atacante=atk.nombre,
        defensor=defn.nombre,
        movimiento=mov.nombre,
        dano_base=dano_base,
        dano_final=dano_final,
        porcentaje_hp=round(dano_final / hp_def * 100, 2),
        hp_defensor=hp_def,
        efectividad=eff,
        stab_aplicado=stab > 1.0,
        shadow_bonus=atk.es_shadow,
        escudo_usado=req.usar_escudo,
        dano_con_escudo=1,
        liga=req.liga.value,
    )


def calcular_dps_tdo(req: PeticionDPSGO) -> ResultadoDPSGO:
    """
    Calcula DPS y TDO de un Pokémon en una liga específica.
    
    DPS = Daño en ciclo completo / Tiempo en ciclo
    TDO = DPS × HP_efectivo

    Ciclo = n fast_moves hasta llenar energía + 1 charged_move
    """
    pokemon = req.pokemon
    defensor = req.defensor

    fast  = pokemon.fast_move
    # Usar el primer charged move para el cálculo
    charged = pokemon.charged_moves[0]

    atk_val, def_val, hp_atk = stats_efectivos_go(pokemon)
    _, def_defensor, _ = stats_efectivos_go(defensor)

    # Cuántos fast moves para cargar el charged move
    fast_moves_por_ciclo = math.ceil(charged.costo_energia / fast.energia_gen)
    tiempo_ciclo_ms = (fast_moves_por_ciclo * fast.duracion_ms)

    # Daño fast moves en ciclo
    eff_fast = efectividad_go(fast.tipo, defensor.tipos)
    stab_fast = STAB_GO if fast.tipo in pokemon.tipos else 1.0
    dano_fast_por_uso = math.floor(
        0.5 * fast.dano * (atk_val / def_defensor) * stab_fast * eff_fast
    ) + 1
    dano_fast_total = dano_fast_por_uso * fast_moves_por_ciclo

    # Daño charged move
    eff_charged = efectividad_go(charged.tipo, defensor.tipos)
    stab_charged = STAB_GO if charged.tipo in pokemon.tipos else 1.0
    dano_charged = math.floor(
        0.5 * charged.dano * (atk_val / def_defensor) * stab_charged * eff_charged
    ) + 1

    dano_ciclo = dano_fast_total + dano_charged
    tiempo_ciclo_s = tiempo_ciclo_ms / 1000.0
    dps = round(dano_ciclo / tiempo_ciclo_s, 3) if tiempo_ciclo_s > 0 else 0.0
    tdo = round(dps * hp_atk, 1)

    return ResultadoDPSGO(
        pokemon=pokemon.nombre,
        fast_move=fast.nombre,
        charged_move=charged.nombre,
        dps=dps,
        tdo=tdo,
        ciclo_dano=dano_ciclo,
        ciclo_ms=tiempo_ciclo_ms,
        liga=req.liga.value,
    )


def nivel_optimo_para_liga(
    pokemon: PokemonGO,
    liga: LigaGO,
) -> tuple[float, int]:
    """
    Encuentra el nivel máximo para que el CP no supere el límite de la liga.
    Retorna (nivel_optimo, cp_maximo_alcanzado).
    """
    cp_max = CP_MAXIMOS[liga]
    if liga == LigaGO.MASTER:
        return 51.0, calcular_cp(pokemon)

    mejor_nivel = 1.0
    mejor_cp = 10

    for nivel in sorted(cpm_para_nivel.__globals__["CPM_TABLE"].keys()):
        import copy
        p = pokemon.model_copy(update={"nivel": nivel})
        try:
            cp = calcular_cp(p)
        except ValueError:
            continue
        if cp <= cp_max:
            mejor_nivel = nivel
            mejor_cp = cp
        else:
            break  # ya superó el cap

    return mejor_nivel, mejor_cp
