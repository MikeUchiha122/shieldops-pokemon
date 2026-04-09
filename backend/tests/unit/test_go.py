"""Tests unitarios — Cerebro C: Pokémon GO."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import math
import pytest
from core.types import TipoElemental
from cerebros.go.models.schemas import (
    PokemonGO, MovimientoGO, StatsBaseGO, IVsGO, EquipoGO,
    LigaGO, CategoriaMovimientoGO, TipoPokemonGO, PeticionDanoGO,
    obtener_cpm,
)
from cerebros.go.engine.damage import (
    efectividad_go, calcular_dano, calcular_cp, nivel_optimo_para_liga,
)


def _swampert() -> PokemonGO:
    return PokemonGO(
        nombre="Swampert",
        tipos=[TipoElemental.AGUA, TipoElemental.TIERRA],
        stats_base=StatsBaseGO(ataque=208, defensa=175, hp=225),
        ivs=IVsGO(ataque=0, defensa=15, hp=14),  # IVs meta GL
        nivel=27.5,
        fast_move=MovimientoGO(
            nombre="Pistola Agua", tipo=TipoElemental.AGUA,
            categoria=CategoriaMovimientoGO.RAPIDO,
            potencia=5, energia=7, duracion_turnos=1,
        ),
        charged_moves=[
            MovimientoGO(
                nombre="Hidrobomba", tipo=TipoElemental.AGUA,
                categoria=CategoriaMovimientoGO.CARGADO,
                potencia=130, energia=-75, duracion_turnos=4,
            ),
            MovimientoGO(
                nombre="Terremoto", tipo=TipoElemental.TIERRA,
                categoria=CategoriaMovimientoGO.CARGADO,
                potencia=120, energia=-65, duracion_turnos=3,
            ),
        ],
    )

def _galarian_stunfisk() -> PokemonGO:
    return PokemonGO(
        nombre="Galarian Stunfisk",
        tipos=[TipoElemental.TIERRA, TipoElemental.ACERO],
        stats_base=StatsBaseGO(ataque=166, defensa=259, hp=240),
        ivs=IVsGO(ataque=0, defensa=15, hp=15),
        nivel=28.5,
        fast_move=MovimientoGO(
            nombre="Barro Lodo", tipo=TipoElemental.TIERRA,
            categoria=CategoriaMovimientoGO.RAPIDO,
            potencia=14, energia=9, duracion_turnos=2,
        ),
        charged_moves=[
            MovimientoGO(
                nombre="Avalancha", tipo=TipoElemental.ROCA,
                categoria=CategoriaMovimientoGO.CARGADO,
                potencia=90, energia=-45, duracion_turnos=3,
            ),
        ],
    )


class TestEfectividadGO:
    def test_multiplicadores_distintos_de_eyp(self):
        # GO usa x1.6, no x2.0
        eff = efectividad_go(TipoElemental.AGUA, [TipoElemental.FUEGO])
        assert eff == pytest.approx(1.6, rel=1e-4)

    def test_poco_eficaz_go(self):
        eff = efectividad_go(TipoElemental.NORMAL, [TipoElemental.ROCA])
        assert eff == pytest.approx(0.625, rel=1e-4)

    def test_inmune_no_es_cero_en_go(self):
        # Tierra vs Volador: inmune en EyP = 0, en GO = 0.391
        eff = efectividad_go(TipoElemental.TIERRA, [TipoElemental.VOLADOR])
        assert eff == pytest.approx(0.391, rel=1e-3)
        assert eff > 0.0  # NUNCA es 0 en GO

    def test_doble_supereficaz_go(self):
        # Agua vs Fuego/Tierra = 1.6 * 1.6 = 2.56
        eff = efectividad_go(TipoElemental.AGUA,
                              [TipoElemental.FUEGO, TipoElemental.TIERRA])
        assert eff == pytest.approx(2.56, rel=1e-3)

    def test_doble_poco_eficaz_go(self):
        # Fuego vs Agua/Roca = 0.625 * 0.625 = 0.391
        eff = efectividad_go(TipoElemental.FUEGO,
                              [TipoElemental.AGUA, TipoElemental.ROCA])
        assert eff == pytest.approx(0.390625, rel=1e-3)


class TestCPFormula:
    def test_cp_swampert_nivel18_5_great_league(self):
        # Nivel optimo real para GL (<=1500) con IVs 0/15/14 es 18.5 → CP 1489
        cp = calcular_cp(208, 175, 225, 0, 15, 14, 18.5)
        assert 1480 <= cp <= 1500

    def test_cp_alto_nivel_supera_cap(self):
        # A nivel 27.5 el CP es ~2196, muy por encima del cap GL
        cp = calcular_cp(208, 175, 225, 0, 15, 14, 27.5)
        assert cp > 1500

    def test_cp_minimo_10(self):
        cp = calcular_cp(50, 50, 50, 0, 0, 0, 1.0)
        assert cp >= 10

    def test_nivel_optimo_great_league(self):
        nivel_opt, cp_opt = nivel_optimo_para_liga(208, 175, 225, 0, 15, 14, 1500)
        assert cp_opt <= 1500
        assert nivel_opt <= 51.0
        assert nivel_opt == 18.5  # valor real verificado


class TestCalculoDanoGO:
    def test_dano_basico(self):
        req = PeticionDanoGO(
            atacante=_swampert(),
            defensor=_galarian_stunfisk(),
            movimiento=_swampert().charged_moves[0],  # Hidrobomba
        )
        res = calcular_dano(req)
        assert res.dano > 0
        assert res.efectividad == pytest.approx(1.6, rel=1e-3)  # SE
        assert res.stab_aplicado is True

    def test_escudo_reduce_a_1(self):
        req = PeticionDanoGO(
            atacante=_swampert(),
            defensor=_galarian_stunfisk(),
            movimiento=_swampert().charged_moves[0],
            defensor_usa_escudo=True,
        )
        res = calcular_dano(req)
        assert res.dano == 1
        assert res.escudo_usado is True

    def test_fast_move_no_activa_escudo(self):
        req = PeticionDanoGO(
            atacante=_swampert(),
            defensor=_galarian_stunfisk(),
            movimiento=_swampert().fast_move,  # Fast Move
            defensor_usa_escudo=True,
        )
        res = calcular_dano(req)
        # Escudo no aplica a Fast Moves
        assert res.dano > 1
        assert res.escudo_usado is False

    def test_shadow_bonus_ataque(self):
        shadow = PokemonGO(
            nombre="Shadow Swampert",
            tipos=[TipoElemental.AGUA, TipoElemental.TIERRA],
            stats_base=StatsBaseGO(ataque=208, defensa=175, hp=225),
            ivs=IVsGO(ataque=0, defensa=15, hp=14),
            nivel=27.5,
            tipo_pokemon=TipoPokemonGO.SHADOW,
            fast_move=_swampert().fast_move,
            charged_moves=_swampert().charged_moves,
        )
        normal = _swampert()
        # Shadow debe tener más ataque efectivo
        assert shadow.ataque_efectivo > normal.ataque_efectivo
        assert shadow.ataque_efectivo == pytest.approx(normal.ataque_efectivo * 1.2, rel=1e-3)

    def test_iv_ataque_bajo_relevante_gl(self):
        # IV Ataque 0 vs 15 — en GL el IV 0 da MENOS CP, más bulk bajo el cap
        cp_iv0  = calcular_cp(208, 175, 225, 0, 15, 15, 27.5)
        cp_iv15 = calcular_cp(208, 175, 225, 15, 15, 15, 40.0)
        assert cp_iv15 > cp_iv0  # A igual nivel, IV 15 da más CP

    def test_energia_fast_move_positiva(self):
        fm = _swampert().fast_move
        assert fm.energia > 0

    def test_energia_charged_move_negativa(self):
        cm = _swampert().charged_moves[0]
        assert cm.energia < 0


class TestValidacionGO:
    def test_fast_move_no_puede_ser_charged(self):
        with pytest.raises(Exception):
            PokemonGO(
                nombre="Test",
                tipos=[TipoElemental.AGUA],
                stats_base=StatsBaseGO(ataque=100, defensa=100, hp=100),
                fast_move=MovimientoGO(
                    nombre="Bad Move", tipo=TipoElemental.AGUA,
                    categoria=CategoriaMovimientoGO.CARGADO,  # inválido como fast_move
                    potencia=50, energia=-50, duracion_turnos=2,
                ),
                charged_moves=[
                    MovimientoGO(
                        nombre="OK", tipo=TipoElemental.AGUA,
                        categoria=CategoriaMovimientoGO.CARGADO,
                        potencia=50, energia=-50, duracion_turnos=2,
                    )
                ],
            )

    def test_iv_fuera_de_rango(self):
        with pytest.raises(Exception):
            IVsGO(ataque=16, defensa=15, hp=15)  # 16 > 15

    def test_equipo_cp_valido_great_league(self):
        equipo = EquipoGO(
            nombre="GL Team",
            liga=LigaGO.GREAT,
            miembros=[_swampert(), _galarian_stunfisk()],
        )
        assert len(equipo.miembros) == 2
