"""Tests unitarios — Cerebro B: LZA Action Time PvP."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from core.types import TipoElemental
from cerebros.lza.models.schemas import (
    PokemonLZA, MovimientoLZA, StatsBaseLZA, EquipoLZA,
    EstadoAlteradoLZA, CategoriaMovimientoLZA, PeticionCalculoDanoLZA,
)
from cerebros.lza.engine.damage import (
    efectividad_lza, cooldown_efectivo, calcular_dano,
)


def _stats_generico() -> StatsBaseLZA:
    return StatsBaseLZA(hp=150, ataque=100, defensa=80, vel=90)

def _garchomp() -> PokemonLZA:
    return PokemonLZA(
        nombre="Garchomp",
        tipos=[TipoElemental.DRAGON, TipoElemental.TIERRA],
        stats=StatsBaseLZA(hp=170, ataque=130, defensa=95, vel=102),
        movimientos=[_garra_dragon(), _terremoto_lza()],
    )

def _togekiss() -> PokemonLZA:
    return PokemonLZA(
        nombre="Togekiss",
        tipos=[TipoElemental.HADA, TipoElemental.VOLADOR],
        stats=StatsBaseLZA(hp=160, ataque=75, defensa=115, vel=80),
        movimientos=[_brillo_magico()],
    )

def _garra_dragon() -> MovimientoLZA:
    return MovimientoLZA(
        nombre="Garra Dragon", tipo=TipoElemental.DRAGON,
        categoria=CategoriaMovimientoLZA.RAPIDO,
        potencia=80, startup_frames=8, cooldown_ms=600,
    )

def _terremoto_lza() -> MovimientoLZA:
    return MovimientoLZA(
        nombre="Terremoto", tipo=TipoElemental.TIERRA,
        categoria=CategoriaMovimientoLZA.CARGADO,
        potencia=100, startup_frames=20, cooldown_ms=1200,
    )

def _brillo_magico() -> MovimientoLZA:
    return MovimientoLZA(
        nombre="Brillo Magico", tipo=TipoElemental.HADA,
        categoria=CategoriaMovimientoLZA.CARGADO,
        potencia=80, startup_frames=18, cooldown_ms=1000,
    )


class TestEfectividadLZA:
    def test_hada_vs_dragon_supereficaz(self):
        eff = efectividad_lza(TipoElemental.HADA, [TipoElemental.DRAGON])
        assert eff == 2.0

    def test_tierra_vs_volador_inmune(self):
        # En LZA las inmunidades SÍ aplican (solo por tipo, sin habilidades)
        eff = efectividad_lza(TipoElemental.TIERRA, [TipoElemental.VOLADOR])
        assert eff == 0.0

    def test_dragon_vs_hada_poco_eficaz(self):
        eff = efectividad_lza(TipoElemental.DRAGON, [TipoElemental.HADA])
        assert eff == 0.0  # Hada es inmune a Dragón

    def test_no_habilidades_levitacion(self):
        # En LZA levitación NO existe — tierra vs eléctrico SÍ hace daño
        eff = efectividad_lza(TipoElemental.TIERRA, [TipoElemental.ELECTRICO])
        assert eff == 2.0  # SE en EyP también, pero en LZA no hay habilidad que lo anule

    def test_efectividad_doble_tipo(self):
        # Hada vs Dragón/Oscuro: 2.0 x 2.0 = 4.0 (pero Oscuro resiste hada? No)
        # Hada vs Dragon/Lucha: 2.0 x 2.0 = 4.0
        eff = efectividad_lza(TipoElemental.HADA,
                               [TipoElemental.DRAGON, TipoElemental.SINIESTRO])
        assert eff == 4.0


class TestCooldownLZA:
    def test_cooldown_normal(self):
        mov = _garra_dragon()
        cd = cooldown_efectivo(mov, EstadoAlteradoLZA.NINGUNO)
        assert cd == 600

    def test_cooldown_paralisis(self):
        mov = _garra_dragon()
        cd = cooldown_efectivo(mov, EstadoAlteradoLZA.PARALIZADO)
        assert cd == 900  # 600 * 1.5

    def test_cooldown_quemadura_no_afecta(self):
        # Quemadura no afecta cooldown
        mov = _terremoto_lza()
        cd = cooldown_efectivo(mov, EstadoAlteradoLZA.QUEMADO)
        assert cd == 1200


class TestCalculoDanoLZA:
    def test_hada_vs_dragon_se(self):
        req = PeticionCalculoDanoLZA(
            atacante=_togekiss(), defensor=_garchomp(),
            movimiento=_brillo_magico(),
        )
        res = calcular_dano(req)
        assert res.efectividad == 2.0
        assert res.dano > 0
        assert res.stab_aplicado is True

    def test_quemadura_reduce_dano_fisico(self):
        req_normal = PeticionCalculoDanoLZA(
            atacante=_garchomp(), defensor=_togekiss(),
            movimiento=_garra_dragon(), quemadura_activa=False,
        )
        req_quemado = PeticionCalculoDanoLZA(
            atacante=_garchomp(), defensor=_togekiss(),
            movimiento=_garra_dragon(), quemadura_activa=True,
        )
        res_normal  = calcular_dano(req_normal)
        res_quemado = calcular_dano(req_quemado)
        assert res_quemado.dano_con_estado == res_normal.dano_con_estado // 2

    def test_esquive_con_startup_alto(self):
        req = PeticionCalculoDanoLZA(
            atacante=_garchomp(), defensor=_togekiss(),
            movimiento=_terremoto_lza(),  # startup_frames=20 > 12
            defensor_esquivando=True,
        )
        res = calcular_dano(req)
        assert res.dano == 0
        assert res.puede_esquivar is True

    def test_no_esquive_startup_bajo_con_movimiento_efectivo(self):
        # Usar Terremoto (Tierra) vs Togekiss (Hada/Volador)
        # startup_frames=20 > 12, pero usamos un movimiento con startup bajo
        mov_rapido_tierra = MovimientoLZA(
            nombre="Patada Baja", tipo=TipoElemental.LUCHA,
            categoria=CategoriaMovimientoLZA.RAPIDO,
            potencia=50, startup_frames=6, cooldown_ms=500,
        )
        req = PeticionCalculoDanoLZA(
            atacante=_garchomp(), defensor=_togekiss(),
            movimiento=mov_rapido_tierra,  # Lucha vs Hada/Volador: Lucha SE vs Hada x2, PE vs Volador x0.5 → total 1.0
            defensor_esquivando=True,      # startup=6 <= 12, no puede esquivar
        )
        res = calcular_dano(req)
        assert res.puede_esquivar is False
        assert res.dano > 0  # Lucha vs Hada/Volador = 2.0 * 0.5 = 1.0 → daño normal

    def test_tierra_inmune_vs_volador_lza(self):
        req = PeticionCalculoDanoLZA(
            atacante=_garchomp(), defensor=_togekiss(),
            movimiento=_terremoto_lza(),  # Tierra vs Hada/Volador
            defensor_esquivando=False,
        )
        res = calcular_dano(req)
        # Tierra vs Volador = 0 (inmune). Tierra vs Hada = 1.0 -> total 0
        assert res.efectividad == 0.0
        assert res.dano == 0


class TestValidacionLZA:
    def test_max_3_switches(self):
        with pytest.raises(Exception):
            from cerebros.lza.models.schemas import EstadoCombateLZA
            EstadoCombateLZA(
                equipo_a=EquipoLZA(nombre="A", miembros=[_garchomp()]),
                equipo_b=EquipoLZA(nombre="B", miembros=[_togekiss()]),
                switches_a=4,  # inválido
            )

    def test_mega_activa_sin_puede_mega_falla(self):
        with pytest.raises(Exception):
            PokemonLZA(
                nombre="Garchomp",
                tipos=[TipoElemental.DRAGON, TipoElemental.TIERRA],
                stats=StatsBaseLZA(hp=170, ataque=130, defensa=95, vel=102),
                movimientos=[_garra_dragon()],
                puede_mega=False,
                mega_activa=True,  # inválido
            )

    def test_max_una_mega_por_equipo(self):
        p1 = PokemonLZA(
            nombre="Mega-Garchomp",
            tipos=[TipoElemental.DRAGON, TipoElemental.TIERRA],
            stats=StatsBaseLZA(hp=170, ataque=130, defensa=95, vel=102),
            movimientos=[_garra_dragon()],
            puede_mega=True,
            stats_mega=StatsBaseLZA(hp=170, ataque=170, defensa=115, vel=92),
            tipos_mega=[TipoElemental.DRAGON, TipoElemental.TIERRA],
            mega_activa=True,
        )
        p2 = PokemonLZA(
            nombre="Mega-Lucario",
            tipos=[TipoElemental.LUCHA, TipoElemental.ACERO],
            stats=StatsBaseLZA(hp=140, ataque=110, defensa=70, vel=90),
            movimientos=[_brillo_magico()],
            puede_mega=True,
            stats_mega=StatsBaseLZA(hp=140, ataque=145, defensa=88, vel=112),
            tipos_mega=[TipoElemental.LUCHA, TipoElemental.ACERO],
            mega_activa=True,
        )
        with pytest.raises(Exception):
            EquipoLZA(nombre="Equipo Doble Mega", miembros=[p1, p2])
