"""Tests unitarios — Cerebro A: EyP VGC."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from cerebros.eyp.models.schemas import (
    PokemonEyP, MovimientoEyP, EVsEyP, IVsEyP, EquipoEyP,
    CategoriaMovimiento, NaturalezaEyP, PeticionCalculoDanoEyP,
)
from cerebros.eyp.engine.damage import (
    stat_final, aplicar_boost, efectividad_eyp, stab_multiplier, calcular_dano,
)
from core.types import TipoElemental


def _miraidon() -> PokemonEyP:
    return PokemonEyP(
        nombre="Miraidon",
        tipos=[TipoElemental.ELECTRICO, TipoElemental.DRAGON],
        habilidad="Motor Hadrón",
        item="Choice Specs",
        naturaleza=NaturalezaEyP.TIMIDO,
        nivel=50,
        stats_base={"hp":100,"atq_fis":85,"def_fis":100,"atq_esp":135,"def_esp":115,"vel":135},
        evs=EVsEyP(atq_esp=252, vel=252, hp=6),
        movimientos=[_electro_drift()],
    )

def _rillaboom() -> PokemonEyP:
    return PokemonEyP(
        nombre="Rillaboom",
        tipos=[TipoElemental.PLANTA],
        habilidad="Batería Hierba",
        naturaleza=NaturalezaEyP.OSADO,
        nivel=50,
        stats_base={"hp":100,"atq_fis":125,"def_fis":90,"atq_esp":60,"def_esp":70,"vel":85},
        evs=EVsEyP(hp=252, atq_fis=252, def_fis=6),
        movimientos=[_grassy_glide()],
    )

def _electro_drift() -> MovimientoEyP:
    return MovimientoEyP(
        nombre="Electro Drift", tipo=TipoElemental.ELECTRICO,
        categoria=CategoriaMovimiento.ESPECIAL, potencia=100, precision=100, pp=5,
    )

def _grassy_glide() -> MovimientoEyP:
    return MovimientoEyP(
        nombre="Grassy Glide", tipo=TipoElemental.PLANTA,
        categoria=CategoriaMovimiento.FISICO, potencia=70, precision=100, pp=10,
    )


class TestStatFinal:
    def test_hp_nivel50_miraidon(self):
        # HP base 100, IV 31, EV 6, nivel 50
        # Formula: floor((2*100+31+floor(6/4))*50/100) + 50 + 10 = 176
        hp = stat_final(100, 6, 31, 50, True, NaturalezaEyP.TIMIDO, "hp")
        assert hp == 176

    def test_vel_timido_bonus(self):
        # Vel base 135, IV 31, EV 252, nivel 50, naturaleza Timido (+vel x1.1)
        vel = stat_final(135, 252, 31, 50, False, NaturalezaEyP.TIMIDO, "vel")
        assert vel == 205  # con bonus x1.1

    def test_naturaleza_neutra(self):
        # Atq base 100, IV 31, EV 0, nivel 50, naturaleza Serio (sin modificador)
        # Formula: floor((2*100+31+0)*50/100) + 5 = floor(115.5)+5 = 120
        s = stat_final(100, 0, 31, 50, False, NaturalezaEyP.SERIO, "atq_fis")
        assert s == 120


class TestBoosts:
    def test_boost_cero(self):
        assert aplicar_boost(100, 0) == 100

    def test_boost_positivo(self):
        assert aplicar_boost(100, 1) == 150
        assert aplicar_boost(100, 2) == 200
        assert aplicar_boost(100, 6) == 400

    def test_boost_negativo(self):
        assert aplicar_boost(100, -1) == 66
        assert aplicar_boost(100, -2) == 50
        assert aplicar_boost(100, -6) == 25


class TestEfectividad:
    def test_electrico_vs_agua(self):
        eff = efectividad_eyp(TipoElemental.ELECTRICO, [TipoElemental.AGUA],
                               "ninguna", False, None)
        assert eff == 2.0

    def test_electrico_inmune_tierra(self):
        eff = efectividad_eyp(TipoElemental.ELECTRICO, [TipoElemental.TIERRA],
                               "ninguna", False, None)
        assert eff == 0.0

    def test_levitacion_inmuniza_tierra(self):
        eff = efectividad_eyp(TipoElemental.TIERRA, [TipoElemental.ELECTRICO],
                               "Levitacion", False, None)
        assert eff == 0.0

    def test_tera_cambia_tipo_defensor(self):
        # Defensor tipo Agua/Volador: electrico vs agua=2.0, vs volador=2.0 → total 4.0
        eff_sin = efectividad_eyp(TipoElemental.ELECTRICO,
                                   [TipoElemental.AGUA, TipoElemental.VOLADOR],
                                   "ninguna", False, None)
        assert eff_sin == 4.0  # doble SE
        # Al teracristalizar a Tierra, electrico queda inmune (0.0)
        eff_tera = efectividad_eyp(TipoElemental.ELECTRICO,
                                    [TipoElemental.AGUA, TipoElemental.VOLADOR],
                                    "ninguna", True, TipoElemental.TIERRA)
        assert eff_tera == 0.0  # Tierra es inmune a electrico


class TestSTAB:
    def test_stab_electrico_miraidon(self):
        m = _miraidon()
        s = stab_multiplier(TipoElemental.ELECTRICO, m.tipos, m.habilidad,
                             m.teraactivada, m.teratipo)
        assert s == 1.5

    def test_no_stab(self):
        m = _miraidon()
        s = stab_multiplier(TipoElemental.FUEGO, m.tipos, m.habilidad,
                             m.teraactivada, m.teratipo)
        assert s == 1.0

    def test_adaptable_stab(self):
        s = stab_multiplier(TipoElemental.ELECTRICO,
                             [TipoElemental.ELECTRICO], "Adaptable",
                             False, None)
        assert s == 2.0


class TestCalculoDano:
    def test_dano_electro_drift_miraidon_vs_rillaboom(self):
        req = PeticionCalculoDanoEyP(
            atacante=_miraidon(),
            defensor=_rillaboom(),
            movimiento=_electro_drift(),
        )
        res = calcular_dano(req)
        # Planta resiste Electrico: efectividad 0.5 (poco eficaz)
        assert res.efectividad == 0.5
        assert res.stab_aplicado is True
        assert res.dano_minimo > 0
        assert res.dano_maximo >= res.dano_minimo
        assert len(res.rolls) == 16

    def test_movimiento_estado_dano_cero(self):
        protect = MovimientoEyP(
            nombre="Proteccion", tipo=TipoElemental.NORMAL,
            categoria=CategoriaMovimiento.ESTADO, potencia=None, precision=None, pp=10,
        )
        req = PeticionCalculoDanoEyP(
            atacante=_miraidon(), defensor=_rillaboom(), movimiento=protect,
        )
        res = calcular_dano(req)
        assert res.dano_minimo == 0
        assert res.dano_maximo == 0

    def test_tierra_vs_electrico_dragon_supereficaz(self):
        terremoto = MovimientoEyP(
            nombre="Terremoto", tipo=TipoElemental.TIERRA,
            categoria=CategoriaMovimiento.FISICO, potencia=100, precision=100, pp=10,
        )
        req = PeticionCalculoDanoEyP(
            atacante=_miraidon(),
            defensor=_miraidon(),  # Electrico/Dragon: Tierra es SE vs Electrico (x2), neutro vs Dragon (x1)
            movimiento=terremoto,
        )
        res = calcular_dano(req)
        # Tierra vs Electrico = 2.0, Tierra vs Dragon = 1.0 → total 2.0
        assert res.efectividad == 2.0
        assert res.dano_minimo > 0


class TestValidacionPydantic:
    def test_evs_total_max_510(self):
        with pytest.raises(Exception):
            EVsEyP(hp=252, atq_fis=252, def_fis=10)  # total = 514 > 510

    def test_nombre_con_inyeccion_sql(self):
        with pytest.raises(Exception):
            MovimientoEyP(
                nombre="'; DROP TABLE pokemon; --",
                tipo=TipoElemental.FUEGO,
                categoria=CategoriaMovimiento.ESPECIAL,
                potencia=90, precision=100, pp=10,
            )

    def test_equipo_valido_6_miembros(self):
        miembros = [_miraidon()] + [
            PokemonEyP(
                nombre=f"Pokemon{i}",
                tipos=[TipoElemental.NORMAL],
                habilidad="Ninguna",
                naturaleza=NaturalezaEyP.SERIO,
                nivel=50,
                stats_base={"hp":80,"atq_fis":80,"def_fis":80,"atq_esp":80,"def_esp":80,"vel":80},
                movimientos=[_grassy_glide()],
            ) for i in range(5)
        ]
        equipo = EquipoEyP(nombre="Equipo Test", miembros=miembros)
        assert len(equipo.miembros) == 6
