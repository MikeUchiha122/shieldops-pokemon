"""Tests unitarios — Cerebro D: Pokémon Champions Singles."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from cerebros.champions.data.pokemon import efectividad_champions
from cerebros.champions.models.schemas import (
    PokemonChampions, StatsBaseChampions, EVsChampions, IVsChampions,
    NaturalezaChampions, PeticionDanoChampions,
)
from cerebros.champions.engine.damage import stat_final, calcular_dano


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _flutter_mane() -> PokemonChampions:
    """Flutter Mane Modesto: Fantasma/Hada, SpA base 135, 252 SpA EVs."""
    return PokemonChampions(
        nombre="Flutter Mane",
        tipos=["fantasma", "hada"],
        stats_base=StatsBaseChampions(
            hp=55, ataque=55, defensa=55,
            ataque_especial=135, defensa_especial=135, velocidad=135,
        ),
        evs=EVsChampions(ataque_especial=252, velocidad=252, hp=4),
        ivs=IVsChampions(),
        naturaleza=NaturalezaChampions.modesto,
        nivel=50,
    )


def _garchomp_fragil() -> PokemonChampions:
    """Garchomp con SpD base 50 para verificar KO garantizado."""
    return PokemonChampions(
        nombre="Garchomp",
        tipos=["dragon", "tierra"],
        stats_base=StatsBaseChampions(
            hp=50, ataque=130, defensa=95,
            ataque_especial=80, defensa_especial=50, velocidad=102,
        ),
        evs=EVsChampions(),
        ivs=IVsChampions(),
        naturaleza=NaturalezaChampions.serio,
        nivel=50,
    )


def _heatran() -> PokemonChampions:
    return PokemonChampions(
        nombre="Heatran",
        tipos=["fuego", "acero"],
        stats_base=StatsBaseChampions(
            hp=91, ataque=90, defensa=106,
            ataque_especial=130, defensa_especial=106, velocidad=77,
        ),
        evs=EVsChampions(ataque_especial=252, velocidad=252),
        ivs=IVsChampions(),
        naturaleza=NaturalezaChampions.timido,
        nivel=50,
    )


def _req(atacante, defensor, movimiento="brillo_magico", **kwargs) -> PeticionDanoChampions:
    return PeticionDanoChampions(
        atacante=atacante, defensor=defensor, movimiento=movimiento, **kwargs
    )


# ── Tests stat_final ─────────────────────────────────────────────────────────

class TestStatFinalChampions:
    def test_hp_base100_lv50(self):
        # floor((2*100+31+0)*50/100) + 50 + 10 = floor(115.5) + 60 = 175
        assert stat_final(100, 31, 0, 50, 1.0, True) == 175

    def test_stat_neutro_base100_lv50(self):
        # floor((floor(231*0.5)+5)*1.0) = floor(120) = 120
        assert stat_final(100, 31, 0, 50, 1.0, False) == 120

    def test_stat_con_nature_boost(self):
        # SpA modesta base 100, 252 EV, lv 50:
        # inner = floor((200+31+63)*0.5) = 147
        # outer = floor(152*1.1) = 167
        assert stat_final(100, 31, 252, 50, 1.1, False) == 167

    def test_stat_con_nature_penalty(self):
        # Atk base 100, solitario -Def: vel tiene malus -0.1 pero aqui testeamos atk
        # stat_final(100, 31, 0, 50, 0.9) = floor(120*0.9) = 108
        assert stat_final(100, 31, 0, 50, 0.9, False) == 108

    def test_hp_crece_con_evs(self):
        hp_sin = stat_final(100, 31, 0, 50, 1.0, True)
        hp_con = stat_final(100, 31, 252, 50, 1.0, True)
        assert hp_con > hp_sin

    def test_hp_no_aplica_nature(self):
        # HP siempre ignora naturaleza — el mult no cambia nada
        hp_1 = stat_final(100, 31, 0, 50, 1.0, True)
        hp_2 = stat_final(100, 31, 0, 50, 1.1, True)
        # La formula HP no multiplica por nat_mult, resultado igual
        assert hp_1 == hp_2


# ── Tests efectividad ────────────────────────────────────────────────────────

class TestEfectividadChampions:
    def test_supereficaz(self):
        assert efectividad_champions("fuego", ["planta"]) == 2.0

    def test_poco_eficaz(self):
        # Agua vs Dragon = 0.5
        assert efectividad_champions("agua", ["dragon"]) == 0.5

    def test_inmune(self):
        # Tierra vs Volador = 0.0
        assert efectividad_champions("tierra", ["volador"]) == 0.0

    def test_no_es_multiplicador_go(self):
        # Champions usa x2.0, GO usa x1.6 — deben ser distintos
        eff = efectividad_champions("agua", ["fuego"])
        assert eff == 2.0
        assert eff != 1.6

    def test_doble_resistencia(self):
        # Planta vs Fuego/Acero = 0.5 * 0.5 = 0.25
        assert efectividad_champions("planta", ["fuego", "acero"]) == 0.25

    def test_doble_supereficaz(self):
        # Agua vs Fuego/Roca = 2.0 * 2.0 = 4.0
        assert efectividad_champions("agua", ["fuego", "roca"]) == 4.0

    def test_fantasma_vs_normal_inmune(self):
        # Normal es inmune a Fantasma
        assert efectividad_champions("fantasma", ["normal"]) == 0.0

    def test_neutro(self):
        assert efectividad_champions("normal", ["normal"]) == 1.0


# ── Tests calcular_dano ──────────────────────────────────────────────────────

class TestCalculoDanoChampions:
    def test_dano_positivo(self):
        res = calcular_dano(_req(_flutter_mane(), _garchomp_fragil()))
        assert res.dano_minimo > 0
        assert res.dano_maximo >= res.dano_minimo

    def test_stab_detectado(self):
        # Brillo Magico (hada) — Flutter Mane tiene tipo hada → STAB
        res = calcular_dano(_req(_flutter_mane(), _garchomp_fragil()))
        assert res.stab is True

    def test_efectividad_correcta(self):
        # Brillo Magico (hada) vs Garchomp (dragon/tierra): hada vs dragon=2.0, hada vs tierra=1.0 → 2.0
        res = calcular_dano(_req(_flutter_mane(), _garchomp_fragil()))
        assert res.efectividad == 2.0

    def test_rango_16_rolls(self):
        # El rango min-max debe corresponder al rango 85%-100%
        res = calcular_dano(_req(_flutter_mane(), _garchomp_fragil()))
        assert res.dano_maximo > res.dano_minimo
        ratio = res.dano_maximo / res.dano_minimo
        assert 1.0 <= ratio <= 1.25

    def test_ko_garantizado(self):
        # Flutter Mane modesto SpA 205 vs Garchomp SpD 70, HP 125, efectividad 2.0, STAB 1.5
        # Min damage >> HP → KO garantizado
        res = calcular_dano(_req(_flutter_mane(), _garchomp_fragil()))
        assert res.ko_garantizado is True

    def test_critico_aumenta_dano(self):
        res_normal = calcular_dano(_req(_flutter_mane(), _garchomp_fragil(), critico=False))
        res_crit   = calcular_dano(_req(_flutter_mane(), _garchomp_fragil(), critico=True))
        assert res_crit.dano_maximo > res_normal.dano_maximo

    def test_movimiento_estado_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_dano(_req(_flutter_mane(), _garchomp_fragil(), movimiento="danza_dragon"))

    def test_movimiento_inexistente_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_dano(_req(_flutter_mane(), _garchomp_fragil(), movimiento="move_xyz_falso"))

    def test_clima_sol_potencia_fuego(self):
        res_sin = calcular_dano(_req(_heatran(), _garchomp_fragil(), "llamarada"))
        res_sol = calcular_dano(_req(_heatran(), _garchomp_fragil(), "llamarada", clima="sol"))
        assert res_sol.dano_maximo > res_sin.dano_maximo

    def test_clima_lluvia_debilita_fuego(self):
        res_sin   = calcular_dano(_req(_heatran(), _garchomp_fragil(), "llamarada"))
        res_lluvia = calcular_dano(_req(_heatran(), _garchomp_fragil(), "llamarada", clima="lluvia"))
        assert res_lluvia.dano_maximo < res_sin.dano_maximo

    def test_detalle_no_vacio(self):
        res = calcular_dano(_req(_flutter_mane(), _garchomp_fragil()))
        assert len(res.detalle) > 20

    def test_porcentaje_consistente_con_dano(self):
        res = calcular_dano(_req(_flutter_mane(), _garchomp_fragil()))
        assert res.porcentaje_max >= res.porcentaje_min
        assert res.porcentaje_min > 0


# ── Tests validación Pydantic ────────────────────────────────────────────────

class TestValidacionPydanticChampions:
    def test_evs_max_252(self):
        with pytest.raises(Exception):
            EVsChampions(hp=253)

    def test_evs_min_0(self):
        with pytest.raises(Exception):
            EVsChampions(ataque=-1)

    def test_ivs_max_31(self):
        with pytest.raises(Exception):
            IVsChampions(ataque=32)

    def test_ivs_min_0(self):
        with pytest.raises(Exception):
            IVsChampions(velocidad=-1)

    def test_naturaleza_valida(self):
        p = _flutter_mane()
        assert p.naturaleza == NaturalezaChampions.modesto

    def test_nivel_rango(self):
        with pytest.raises(Exception):
            PokemonChampions(
                nombre="Test", tipos=["normal"],
                stats_base=StatsBaseChampions(hp=100, ataque=100, defensa=100,
                                               ataque_especial=100, defensa_especial=100,
                                               velocidad=100),
                naturaleza=NaturalezaChampions.serio,
                nivel=0,  # invalido — ge=1
            )
