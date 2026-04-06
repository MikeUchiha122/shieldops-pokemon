"""
tests/unit/test_damage_engine.py
Tests del motor de daño — sin conexión a red, sin I/O.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.models import (
    BaseStats, EVSpread, IVSpread, Move, MoveCategory, Nature, Pokemon, Type, Game
)
from core.damage.engine import calculate_damage, DamageContext
from core.hack_check.validator import validate_pokemon, validate_team


def _make_lucario() -> Pokemon:
    return Pokemon(
        name="Mega-Lucario",
        dex_number=448,
        types=[Type.FIGHTING, Type.STEEL],
        base_stats=BaseStats(hp=70, attack=145, defense=88, sp_atk=140, sp_def=70, speed=112),
        nature=Nature.TIMID,
        ability="Adaptability",
        item="Lucarionite",
        level=50,
        ivs=IVSpread(),
        evs=EVSpread(sp_atk=252, speed=252, hp=4),
        moves=[
            Move(name="Aura Sphere", type=Type.FIGHTING, category=MoveCategory.SPECIAL, power=80, pp=20),
            Move(name="Flash Cannon", type=Type.STEEL,   category=MoveCategory.SPECIAL, power=80, accuracy=100, pp=10),
            Move(name="Nasty Plot",  type=Type.DARK,     category=MoveCategory.STATUS, power=0, pp=20),
            Move(name="Vacuum Wave", type=Type.FIGHTING, category=MoveCategory.SPECIAL, power=40, accuracy=100, pp=30, priority=1),
        ],
        can_mega=True,
    )


def _make_blissey() -> Pokemon:
    return Pokemon(
        name="Blissey",
        dex_number=242,
        types=[Type.NORMAL],
        base_stats=BaseStats(hp=255, attack=10, defense=10, sp_atk=75, sp_def=135, speed=55),
        nature=Nature.CALM,
        ability="Natural Cure",
        level=50,
        ivs=IVSpread(),
        evs=EVSpread(hp=252, sp_def=252, defense=4),
        moves=[
            Move(name="Soft-Boiled", type=Type.NORMAL, category=MoveCategory.STATUS, power=0, pp=10),
            Move(name="Seismic Toss", type=Type.FIGHTING, category=MoveCategory.PHYSICAL, power=1, accuracy=100, pp=20),
            Move(name="Thunder Wave", type=Type.ELECTRIC, category=MoveCategory.STATUS, power=0, pp=20),
            Move(name="Ice Beam", type=Type.ICE, category=MoveCategory.SPECIAL, power=90, accuracy=100, pp=10),
        ],
    )


class TestDamageEngine:
    def test_returns_16_rolls(self) -> None:
        lucario = _make_lucario()
        blissey = _make_blissey()
        move    = lucario.moves[0]   # Aura Sphere

        ctx    = DamageContext(attacker=lucario, defender=blissey, move=move, is_mega_active=True)
        result = calculate_damage(ctx)

        assert len(result.rolls) == 16

    def test_min_less_than_max(self) -> None:
        lucario = _make_lucario()
        blissey = _make_blissey()
        move    = lucario.moves[0]

        ctx    = DamageContext(attacker=lucario, defender=blissey, move=move, is_mega_active=True)
        result = calculate_damage(ctx)

        assert result.min_damage <= result.max_damage

    def test_adaptable_stab_applied(self) -> None:
        """Adaptable debería aumentar el daño vs STAB estándar."""
        lucario = _make_lucario()
        blissey = _make_blissey()
        aura    = lucario.moves[0]

        # Con Adaptable
        ctx_adapt = DamageContext(attacker=lucario, defender=blissey, move=aura, is_mega_active=True)
        res_adapt  = calculate_damage(ctx_adapt)

        # Sin Adaptable (cambiar habilidad temporalmente)
        lucario_no_adapt = lucario.model_copy(update={"ability": "Inner Focus"})
        ctx_normal = DamageContext(attacker=lucario_no_adapt, defender=blissey, move=aura)
        res_normal  = calculate_damage(ctx_normal)

        assert res_adapt.max_damage > res_normal.max_damage, \
            "Adaptable debe hacer más daño que STAB estándar"

    def test_status_move_zero_damage(self) -> None:
        lucario = _make_lucario()
        blissey = _make_blissey()
        nasty   = lucario.moves[2]   # Nasty Plot — STATUS

        ctx    = DamageContext(attacker=lucario, defender=blissey, move=nasty)
        result = calculate_damage(ctx)

        assert result.max_damage == 0

    def test_percent_calculated(self) -> None:
        lucario = _make_lucario()
        blissey = _make_blissey()
        move    = lucario.moves[0]

        ctx    = DamageContext(attacker=lucario, defender=blissey, move=move, is_mega_active=True)
        result = calculate_damage(ctx)

        assert 0 < result.min_percent <= result.max_percent


class TestHackCheck:
    def test_legal_pokemon_passes(self) -> None:
        lucario = _make_lucario()
        report  = validate_pokemon(lucario, Game.LEGENDS_ZA)
        assert report.is_legal, f"Infracciones inesperadas: {report.violations}"

    def test_over_510_evs_detected(self) -> None:
        from pydantic import ValidationError
        import pytest

        with pytest.raises(ValidationError):
            # 512 EVs — debe fallar en Pydantic antes de llegar al validator
            EVSpread(hp=252, attack=252, defense=8, sp_atk=0, sp_def=0, speed=0)

    def test_banned_move_detected(self) -> None:
        lucario  = _make_lucario()
        bad_move = Move(
            name="Spore", type=Type.GRASS, category=MoveCategory.STATUS, power=0, pp=15
        )
        lucario_bad = lucario.model_copy(update={"moves": [*lucario.moves[:3], bad_move]})
        report = validate_pokemon(lucario_bad, Game.SCARLET_VIOLET)
        assert not report.is_legal
        assert any("Spore" in v for v in report.violations)

    def test_duplicate_item_in_team(self) -> None:
        lucario = _make_lucario()
        blissey = _make_blissey()

        # Ambos con el mismo ítem
        blissey_same_item = blissey.model_copy(update={"item": "Lucarionite"})
        reports = validate_team([lucario, blissey_same_item], Game.LEGENDS_ZA)

        # Al menos uno debe reportar ítem duplicado
        all_violations = [v for r in reports for v in r.violations]
        assert any("duplicado" in v.lower() for v in all_violations)


class TestConfig:
    def test_settings_default_env(self) -> None:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from core.config import Settings, AppEnv
        s = Settings()
        assert s.app_env == AppEnv.DEVELOPMENT
        assert not s.is_production

    def test_settings_forbidden_dsn(self) -> None:
        import pytest
        from pydantic import ValidationError
        from core.config import Settings
        with pytest.raises(ValidationError):
            Settings(database_url="pickle://./bad.pkl")
