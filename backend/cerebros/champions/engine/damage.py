"""
cerebros/champions/engine/damage.py
Motor de daño para Pokémon Champions — Singles Gen IX (sin Tera/Mega/Dynamax).
Fórmula: piso((piso(piso(2*nivel/5+2)*potencia*A/D/50)+2)*modificadores)
Sistema de 16 rolls: 85–100 % (85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100).
"""
from __future__ import annotations
import math
from cerebros.champions.models.schemas import (
    PeticionDanoChampions, ResultadoDanoChampions,
    NATURALEZA_MODIFICADORES,
)
from cerebros.champions.data.pokemon import efectividad_champions
from cerebros.champions.data.movimientos import MOVIMIENTOS_CHAMPIONS

_ROLLS = [r / 100.0 for r in range(85, 101)]

_CLIMA_BOOST = {
    ("sol",    "fuego"):   1.5,
    ("lluvia", "agua"):    1.5,
    ("sol",    "agua"):    0.5,
    ("lluvia", "fuego"):   0.5,
    ("arena",  "roca"):    1.5,
}

_BOOST_TABLE = {
    -6: 2/8, -5: 2/7, -4: 2/6, -3: 2/5, -2: 2/4, -1: 2/3,
     0: 1.0,
     1: 3/2,  2: 4/2,  3: 5/2,  4: 6/2,  5: 7/2,  6: 8/2,
}


def stat_final(base: int, iv: int, ev: int, nivel: int,
               naturaleza_mult: float = 1.0, es_hp: bool = False) -> int:
    if es_hp:
        return math.floor((2 * base + iv + math.floor(ev / 4)) * nivel / 100) + nivel + 10
    return math.floor(
        (math.floor((2 * base + iv + math.floor(ev / 4)) * nivel / 100) + 5) * naturaleza_mult
    )


def _nat_mult(naturaleza: str, stat: str) -> float:
    mods = NATURALEZA_MODIFICADORES.get(naturaleza, {})
    return mods.get(stat, 1.0)


def calcular_dano(req: PeticionDanoChampions) -> ResultadoDanoChampions:
    mov_data = MOVIMIENTOS_CHAMPIONS.get(
        req.movimiento.lower().replace(" ", "_").replace("-", "_")
    )
    if mov_data is None:
        raise ValueError(f"Movimiento '{req.movimiento}' no encontrado en Champions.")

    potencia = mov_data.get("potencia")
    if not potencia:
        raise ValueError(f"'{req.movimiento}' es un movimiento de estado sin daño.")

    categoria = mov_data["categoria"]
    tipo_mov = mov_data["tipo"]
    nivel = req.atacante.nivel
    nat_atk = req.atacante.naturaleza.value
    nat_def = req.defensor.naturaleza.value

    # Stats atacante
    if categoria == "fisico":
        atk_base = req.atacante.stats_base.ataque
        atk_iv   = req.atacante.ivs.ataque
        atk_ev   = req.atacante.evs.ataque
        atk_stat = stat_final(atk_base, atk_iv, atk_ev, nivel,
                              _nat_mult(nat_atk, "ataque"))
    else:
        atk_base = req.atacante.stats_base.ataque_especial
        atk_iv   = req.atacante.ivs.ataque_especial
        atk_ev   = req.atacante.evs.ataque_especial
        atk_stat = stat_final(atk_base, atk_iv, atk_ev, nivel,
                              _nat_mult(nat_atk, "ataque_especial"))

    # Stats defensor
    if categoria == "fisico":
        def_base = req.defensor.stats_base.defensa
        def_iv   = req.defensor.ivs.defensa
        def_ev   = req.defensor.evs.defensa
        def_stat = stat_final(def_base, def_iv, def_ev, req.defensor.nivel,
                              _nat_mult(nat_def, "defensa"))
    else:
        def_base = req.defensor.stats_base.defensa_especial
        def_iv   = req.defensor.ivs.defensa_especial
        def_ev   = req.defensor.evs.defensa_especial
        def_stat = stat_final(def_base, def_iv, def_ev, req.defensor.nivel,
                              _nat_mult(nat_def, "defensa_especial"))

    hp_defensor = stat_final(
        req.defensor.stats_base.hp, req.defensor.ivs.hp,
        req.defensor.evs.hp, req.defensor.nivel, es_hp=True,
    )

    # Boosts
    atk_stat = math.floor(atk_stat * _BOOST_TABLE.get(req.boost_atacante, 1.0))
    def_stat = math.floor(def_stat * _BOOST_TABLE.get(req.boost_defensor, 1.0))
    def_stat = max(def_stat, 1)

    # Base damage (sin roll)
    base = math.floor(
        math.floor(math.floor(2 * nivel / 5 + 2) * potencia * atk_stat / def_stat / 50) + 2
    )

    # STAB
    stab = tipo_mov in req.atacante.tipos
    stab_mult = 1.5 if stab else 1.0

    # Efectividad
    efect = efectividad_champions(tipo_mov, req.defensor.tipos)

    # Clima
    clima_mult = _CLIMA_BOOST.get((req.clima, tipo_mov), 1.0) if req.clima else 1.0

    # Objeto — Orbe de Vida
    objeto_mult = 1.3 if req.atacante.objeto == "orbe_de_vida" else 1.0

    # Crítico
    crit_mult = 1.5 if req.critico else 1.0

    # Burn
    quemadura_mult = 0.5 if (categoria == "fisico" and
                              getattr(req.atacante, "estado", None) == "quemadura") else 1.0

    # 16 rolls
    danos = []
    for roll in _ROLLS:
        d = math.floor(base * roll)
        d = math.floor(d * stab_mult)
        d = math.floor(d * efect)
        d = math.floor(d * clima_mult)
        d = math.floor(d * objeto_mult)
        d = math.floor(d * crit_mult)
        d = math.floor(d * quemadura_mult)
        danos.append(max(1, d))

    dano_min = danos[0]
    dano_max = danos[-1]
    dano_prom = sum(danos) / len(danos)

    pct_min  = round(dano_min  / hp_defensor * 100, 2)
    pct_max  = round(dano_max  / hp_defensor * 100, 2)
    pct_prom = round(dano_prom / hp_defensor * 100, 2)

    ko_guar = dano_min >= hp_defensor
    pos_2hko = dano_min * 2 >= hp_defensor

    detalle = (
        f"{req.atacante.nombre} usa {mov_data['nombre']} contra {req.defensor.nombre} | "
        f"Daño: {dano_min}–{dano_max} ({pct_min}–{pct_max} %) | "
        f"Efect: ×{efect} | STAB: {stab} | "
        f"{'¡KO garantizado!' if ko_guar else '2HKO posible' if pos_2hko else 'No KO'}"
    )

    return ResultadoDanoChampions(
        dano_minimo=dano_min,
        dano_maximo=dano_max,
        dano_promedio=round(dano_prom, 2),
        porcentaje_min=pct_min,
        porcentaje_max=pct_max,
        porcentaje_promedio=pct_prom,
        efectividad=efect,
        stab=stab,
        critico=req.critico,
        ko_garantizado=ko_guar,
        posible_2hko=pos_2hko,
        detalle=detalle,
    )
