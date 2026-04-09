"""
cerebros/eyp/engine/damage.py
Motor de daño para Escarlata/Púrpura — Fórmula oficial Gen IX.

Fórmula:
  Daño = (((2×Nivel/5 + 2) × Potencia × (Atq/Def)) / 50 + 2)
         × Modificadores

Modificadores en orden oficial:
  1. Targets (dobles: 0.75 si ataca a 2)
  2. Pantallas (0.5 si activa, 0.5×0.5 si ambas)
  3. Clima
  4. Crítico (×1.5)
  5. Aleatorio (85–100 / 100, 16 rolls)
  6. STAB (×1.5, Adaptable ×2.0)
  7. Tipo (efectividad)
  8. Quemar (×0.5 si físico y quemado)
  9. Otros (items, etc.)
"""
from __future__ import annotations
import math
from core.types import TipoElemental, efectividad_base, TABLA_EFECTIVIDAD
from cerebros.eyp.models.schemas import (
    PokemonEyP, MovimientoEyP, CategoriaMovimiento,
    NaturalezaEyP, MODIFICADORES_NATURALEZA, PeticionCalculoDanoEyP,
    ResultadoDanoEyP,
)

# Multiplicadores de naturaleza
_MOD_NAT: dict[str, float] = {}  # calculado en _inicializar_mods_nat()

def _inicializar_mods_nat() -> None:
    global _MOD_NAT
    # No hace falta precalcular — se aplica inline en stat_final


def stat_final(
    base: int,
    ev: int,
    iv: int,
    nivel: int,
    es_hp: bool,
    naturaleza: NaturalezaEyP,
    stat_key: str,
) -> int:
    """
    Fórmula oficial de stats Gen IX.
    HP:    floor((2×Base + IV + floor(EV/4)) × Nivel / 100) + Nivel + 10
    Otro:  (floor((2×Base + IV + floor(EV/4)) × Nivel / 100) + 5) × Naturaleza
    """
    base_calc = math.floor((2 * base + iv + math.floor(ev / 4)) * nivel / 100)
    if es_hp:
        return base_calc + nivel + 10
    stat = base_calc + 5
    mod_nat, _ = MODIFICADORES_NATURALEZA.get(naturaleza, ("", None))
    _, menos_nat = MODIFICADORES_NATURALEZA.get(naturaleza, ("", None))
    nat_multi = 1.0
    if mod_nat == stat_key:
        nat_multi = 1.1
    elif menos_nat == stat_key:
        nat_multi = 0.9
    return math.floor(stat * nat_multi)


def aplicar_boost(stat: int, boost: int) -> int:
    """
    Tabla oficial de boosts: cada etapa es ×(2+n)/2 para positivos
    y ×2/(2+|n|) para negativos. Máximo ±6.
    """
    boost = max(-6, min(6, boost))
    if boost >= 0:
        return math.floor(stat * (2 + boost) / 2)
    return math.floor(stat * 2 / (2 + abs(boost)))


def efectividad_eyp(
    tipo_mov: TipoElemental,
    tipos_defensor: list[TipoElemental],
    habilidad_defensor: str,
    teraactivada: bool,
    teratipo: TipoElemental | None,
) -> float:
    """
    Calcula la efectividad en EyP aplicando:
    - Habilidades que otorgan inmunidades (Levitación, Maravilla, etc.)
    - Teracristalización del defensor
    """
    # Si el defensor teracristalizó, sus tipos cambian al Teratipo
    tipos_efectivos = ([teratipo] if teraactivada and teratipo else tipos_defensor)

    mult = 1.0
    for t in tipos_efectivos:
        mult *= efectividad_base(tipo_mov, t)

    # Habilidades que modifican efectividad
    hab = habilidad_defensor.lower()
    if hab == "levitacion" and tipo_mov == TipoElemental.TIERRA:
        mult = 0.0
    elif hab == "maravilla" and mult > 1.0:
        mult = 1.0
    elif hab == "filtro" and mult > 1.0:
        mult *= 0.75
    elif hab == "rompemoldes":
        pass  # atacante — se aplica ignorando habilidades del defensor
    # Flash Fuego (Volcán) — si recibe Fuego, absorbe
    elif hab in ("volcan", "absorbe agua", "absorbevoltios") and mult == 0.0:
        mult = 0.0  # sigue siendo inmune, pero carga la habilidad

    return mult


def stab_multiplier(
    tipo_mov: TipoElemental,
    tipos_pokemon: list[TipoElemental],
    habilidad: str,
    teraactivada: bool,
    teratipo: TipoElemental | None,
) -> float:
    """
    STAB normal: ×1.5
    Adaptable: ×2.0
    Tera-STAB: si el teratipo coincide con el tipo del movimiento → ×2.0
    """
    adaptable = habilidad.lower() == "adaptable"
    tipos_para_stab = tipos_pokemon[:]
    if teraactivada and teratipo:
        tipos_para_stab.append(teratipo)
    tiene_stab = tipo_mov in tipos_para_stab
    if not tiene_stab:
        return 1.0
    return 2.0 if adaptable else 1.5


def modificador_clima(
    tipo_mov: TipoElemental,
    clima: str | None,
) -> float:
    if not clima:
        return 1.0
    c = clima.lower()
    if c == "sol":
        if tipo_mov == TipoElemental.FUEGO:  return 1.5
        if tipo_mov == TipoElemental.AGUA:   return 0.5
    elif c == "lluvia":
        if tipo_mov == TipoElemental.AGUA:   return 1.5
        if tipo_mov == TipoElemental.FUEGO:  return 0.5
    return 1.0


def calcular_dano(req: PeticionCalculoDanoEyP) -> ResultadoDanoEyP:
    """
    Calcula el daño con los 16 rolls (85–100%) de Gen IX.
    """
    atk = req.atacante
    defn = req.defensor
    mov = req.movimiento

    if mov.categoria == CategoriaMovimiento.ESTADO or mov.potencia is None:
        return ResultadoDanoEyP(
            atacante=atk.nombre, defensor=defn.nombre,
            movimiento=mov.nombre, dano_minimo=0, dano_maximo=0,
            porcentaje_min=0.0, porcentaje_max=0.0,
            hp_defensor=_hp(defn), es_ohko=False, es_2hko=False,
            stab_aplicado=False, tera_aplicado=False,
            efectividad=0.0, rolls=[0]*16,
        )

    # Stats finales del atacante
    es_fisico = mov.categoria == CategoriaMovimiento.FISICO
    atk_stat_key = "atq_fis" if es_fisico else "atq_esp"
    def_stat_key = "def_fis" if es_fisico else "def_esp"

    atq_val = stat_final(
        atk.stats_base[atk_stat_key],
        getattr(atk.evs, atk_stat_key),
        getattr(atk.ivs, atk_stat_key),
        atk.nivel, False, atk.naturaleza, atk_stat_key,
    )
    def_val = stat_final(
        defn.stats_base[def_stat_key],
        getattr(defn.evs, def_stat_key),
        getattr(defn.ivs, def_stat_key),
        defn.nivel, False, defn.naturaleza, def_stat_key,
    )
    hp_def = _hp(defn)

    # Boosts
    atq_val = aplicar_boost(atq_val, req.boost_atq)
    def_val = aplicar_boost(def_val, req.boost_def)

    # Efectividad
    eff = efectividad_eyp(
        mov.tipo, defn.tipos, defn.habilidad,
        defn.teraactivada, defn.teratipo,
    )
    if eff == 0.0:
        return ResultadoDanoEyP(
            atacante=atk.nombre, defensor=defn.nombre,
            movimiento=mov.nombre, dano_minimo=0, dano_maximo=0,
            porcentaje_min=0.0, porcentaje_max=0.0,
            hp_defensor=hp_def, es_ohko=False, es_2hko=False,
            stab_aplicado=False, tera_aplicado=atk.teraactivada,
            efectividad=0.0, rolls=[0]*16,
        )

    stab = stab_multiplier(mov.tipo, atk.tipos, atk.habilidad,
                           atk.teraactivada, atk.teratipo)
    clima = modificador_clima(mov.tipo, req.clima_activo)
    critico_mult = 1.5 if req.critico else 1.0
    pantalla_mult = 0.5 if req.pantallas and not req.critico else 1.0
    quemar_mult  = 0.5 if es_fisico else 1.0  # solo si está quemado (simplificado)

    # Daño base (sin roll)
    dano_base = math.floor(
        (math.floor((2 * atk.nivel / 5 + 2) * mov.potencia * atq_val / def_val) / 50 + 2)
        * critico_mult * clima * pantalla_mult
    )

    # 16 rolls: 85/100 a 100/100
    rolls_values = [
        math.floor(dano_base * r / 100 * stab * eff * quemar_mult)
        for r in range(85, 101)
    ]
    rolls_values = rolls_values[:req.n_rolls]

    dano_min = rolls_values[0]
    dano_max = rolls_values[-1]

    return ResultadoDanoEyP(
        atacante=atk.nombre,
        defensor=defn.nombre,
        movimiento=mov.nombre,
        dano_minimo=dano_min,
        dano_maximo=dano_max,
        porcentaje_min=round(dano_min / hp_def * 100, 1),
        porcentaje_max=round(dano_max / hp_def * 100, 1),
        hp_defensor=hp_def,
        es_ohko=dano_min >= hp_def,
        es_2hko=dano_min * 2 >= hp_def,
        stab_aplicado=stab > 1.0,
        tera_aplicado=atk.teraactivada,
        efectividad=eff,
        rolls=rolls_values,
    )


def _hp(p: PokemonEyP) -> int:
    return stat_final(
        p.stats_base["hp"], p.evs.hp, p.ivs.hp,
        p.nivel, True, p.naturaleza, "hp",
    )
