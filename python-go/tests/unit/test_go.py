"""
tests/unit/test_go.py — Suite de tests ShieldOps GO
11 tests cubriendo: modelos, daño, IVs, equipos y hack-check
"""
from __future__ import annotations
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.models import GoPokemon, GoIVSpread, GoMove, GoTeam, MoveCategory, League, PlayStyle, TeamRole
from core.damage.engine import calculate_damage, calculate_cp, effective_attack, get_cpm
from core.ivs.calculator import evaluate_ivs, find_max_level_under_cap
from core.teams.generator import generate_team, team_to_text
from core.hack_check.validator import validate_pokemon


# ── Fixtures ─────────────────────────────────────────────────────
@pytest.fixture
def galarian_stunfisk():
    fast = GoMove(name="Mud Shot", type="ground", category=MoveCategory.FAST, power=3, energy=4)
    charged = [
        GoMove(name="Rock Slide", type="rock", category=MoveCategory.CHARGED, power=75, energy=45),
        GoMove(name="Earthquake", type="ground", category=MoveCategory.CHARGED, power=120, energy=65),
    ]
    return GoPokemon(
        name="Galarian Stunfisk", types=["ground","steel"],
        base_attack=144, base_defense=179, base_hp=198,
        ivs=GoIVSpread(attack=0, defense=15, hp=15),
        level=29.0, fast_move=fast, charged_moves=charged, role=TeamRole.LEAD,
    )


@pytest.fixture
def giratina_a():
    fast = GoMove(name="Shadow Claw", type="ghost", category=MoveCategory.FAST, power=9, energy=8)
    charged = [
        GoMove(name="Shadow Ball", type="ghost", category=MoveCategory.CHARGED, power=100, energy=55),
        GoMove(name="Dragon Claw", type="dragon", category=MoveCategory.CHARGED, power=50, energy=35),
    ]
    return GoPokemon(
        name="Giratina-A", types=["ghost","dragon"],
        base_attack=187, base_defense=225, base_hp=284,
        ivs=GoIVSpread(attack=0, defense=15, hp=15),
        level=28.5, fast_move=fast, charged_moves=charged, role=TeamRole.CLOSER,
    )


# ── Modelos ──────────────────────────────────────────────────────
class TestModels:
    def test_iv_spread_hundo(self):
        ivs = GoIVSpread(attack=15, defense=15, hp=15)
        assert ivs.is_hundo is True
        assert ivs.is_nundo is False

    def test_iv_spread_nundo(self):
        ivs = GoIVSpread(attack=0, defense=0, hp=0)
        assert ivs.is_nundo is True
        assert ivs.is_hundo is False

    def test_iv_range_0_to_15(self):
        """IVs deben estar entre 0 y 15 — a diferencia de VGC (0–31)"""
        with pytest.raises(Exception):
            GoIVSpread(attack=16, defense=15, hp=15)
        with pytest.raises(Exception):
            GoIVSpread(attack=0, defense=-1, hp=15)

    def test_go_team_requires_3_members(self, galarian_stunfisk, giratina_a):
        with pytest.raises(Exception):
            GoTeam(name="Test", league=League.ULTRA, style=PlayStyle.BALANCED,
                   members=[galarian_stunfisk, giratina_a])  # solo 2 → debe fallar


# ── Motor de daño ────────────────────────────────────────────────
class TestDamageEngine:
    def test_damage_minimum_1(self, galarian_stunfisk, giratina_a):
        """Daño mínimo es siempre 1 en GO"""
        move = GoMove(name="Struggle", type="normal", category=MoveCategory.FAST, power=1, energy=0)
        result = calculate_damage(galarian_stunfisk, giratina_a, move)
        assert result.damage >= 1

    def test_stab_applied(self, galarian_stunfisk):
        """STAB de ×1.2 se aplica cuando tipo del movimiento coincide con tipo del atacante"""
        defender = GoPokemon(name="Test", types=["normal"], base_attack=100, base_defense=100,
                             base_hp=200, ivs=GoIVSpread(attack=15, defense=15, hp=15), level=40.0)
        move_stab    = GoMove(name="Earthquake", type="ground", category=MoveCategory.CHARGED, power=120, energy=65)
        move_no_stab = GoMove(name="Shadow Ball", type="ghost",  category=MoveCategory.CHARGED, power=100, energy=55)
        r_stab    = calculate_damage(galarian_stunfisk, defender, move_stab)
        r_no_stab = calculate_damage(galarian_stunfisk, defender, move_no_stab)
        assert r_stab.stab_applied is True
        assert r_no_stab.stab_applied is False

    def test_type_effectiveness_supereffective(self, giratina_a, galarian_stunfisk):
        """Ghost vs Psychic = ×1.6 en GO (no ×2 como en VGC)"""
        psych = GoPokemon(name="Cresselia", types=["psychic"], base_attack=152,
                          base_defense=258, base_hp=260, ivs=GoIVSpread(attack=0, defense=15, hp=15), level=29.0)
        move = GoMove(name="Shadow Ball", type="ghost", category=MoveCategory.CHARGED, power=100, energy=55)
        result = calculate_damage(giratina_a, psych, move)
        assert result.type_eff == pytest.approx(1.6, rel=0.01)

    def test_cp_calculation(self, galarian_stunfisk):
        """CP calculado debe estar cerca del CP real conocido (1500)"""
        cp = calculate_cp(galarian_stunfisk)
        assert 1450 <= cp <= 1520

    def test_cpm_level_40(self):
        """CPM nivel 40 = 0.7903 (dato oficial)"""
        assert get_cpm(40.0) == pytest.approx(0.7903, rel=0.001)


# ── Calculadora IVs ──────────────────────────────────────────────
class TestIVCalculator:
    def test_low_attack_iv_optimal_great_league(self, galarian_stunfisk):
        """IVs 0/15/15 son óptimos para Great League"""
        report = evaluate_ivs(galarian_stunfisk, League.GREAT)
        assert report.is_legal_cp is True
        assert report.is_optimal is True

    def test_high_attack_iv_suboptimal_great_league(self, galarian_stunfisk):
        """IV Ataque alto en Great League debe generar sugerencia"""
        galarian_stunfisk.ivs = GoIVSpread(attack=15, defense=15, hp=15)
        report = evaluate_ivs(galarian_stunfisk, League.GREAT)
        assert any("Ataque" in s for s in report.suggestions)

    def test_master_league_wants_hundo(self):
        """Master League: 15/15/15 es el objetivo"""
        zacian = GoPokemon(name="Zacian-C", types=["fairy","steel"],
                           base_attack=332, base_defense=250, base_hp=192,
                           ivs=GoIVSpread(attack=15, defense=15, hp=15), level=50.0)
        report = evaluate_ivs(zacian, League.MASTER)
        assert report.is_optimal is True


# ── Generador de equipos ─────────────────────────────────────────
class TestTeamGenerator:
    def test_generates_3_members(self):
        team = generate_team(League.GREAT, PlayStyle.BALANCED)
        assert len(team.members) == 3

    def test_team_has_roles(self):
        team = generate_team(League.ULTRA, PlayStyle.AGGRO)
        roles = [m.role for m in team.members]
        assert TeamRole.LEAD in roles
        assert TeamRole.SAFE_SWITCH in roles
        assert TeamRole.CLOSER in roles


# ── Hack Check ───────────────────────────────────────────────────
class TestHackCheck:
    def test_legal_pokemon_passes(self, galarian_stunfisk):
        result = validate_pokemon(galarian_stunfisk, League.GREAT)
        assert result.passed is True
        assert len(result.errors) == 0

    def test_cp_over_limit_fails(self, giratina_a):
        """Giratina-A a nivel 50 supera el límite de Great League"""
        giratina_a.level = 50.0
        result = validate_pokemon(giratina_a, League.GREAT)
        assert any("excede" in e for e in result.errors)

    def test_invalid_iv_range_fails(self, galarian_stunfisk):
        """IV = 16 debe fallar la validación"""
        with pytest.raises(Exception):
            galarian_stunfisk.ivs = GoIVSpread(attack=16, defense=15, hp=15)
