"""
cerebros/go/engine/guia.py
Motor de guías para Pokémon GO — GO Battle League.

Mecánicas exclusivas GO:
- Stats GO (escala Niantic, diferente a serie principal)
- STAB ×1.2 | SE ×1.6 | NVE ×0.625 | "Inmune" ×0.391
- IVs 0-15 | Sin naturaleza | Sin EVs | Sin objetos
- Optimización de IVs por liga: encontrar el mejor IVs que maximiza stats en el CP cap
- DPS (Damage Per Second) y TDO (Total Damage Output) como métricas
- Shadow: Ataque ×1.2, Defensa ×0.833
- Escudos: 2 por batalla — bloquean Charged Moves (reducen a 1 HP)
"""
from __future__ import annotations
import math

from cerebros.go.data.pokemon import POKEMON_GO, buscar_pokemon_go, efectividad_go, pokemon_go_por_liga
from cerebros.go.data.movimientos import FAST_MOVES_GO, CHARGED_MOVES_GO
from cerebros.go.models.schemas import obtener_cpm, CPM_TABLE, LigaGO, CP_CAPS
from core.types import TipoElemental


# ── Amenazas meta GO por liga ─────────────────────────────────────────────────
AMENAZAS_META_GO: dict[str, list[str]] = {
    "great": [
        "galarian_stunfisk", "medicham", "registeel", "azumarill",
        "walrein", "talonflame", "bastiodon", "lanturn",
    ],
    "ultra": [
        "cresselia", "obstagoon", "alolan_muk", "trevenant",
        "jellicent", "giratina_altered", "registeel", "walrein",
    ],
    "master": [
        "zacian", "kyogre", "groudon", "dialga",
        "palkia", "mewtwo", "giratina_origin", "togekiss",
        "garchomp", "dragonite",
    ],
}


def _calcular_cp_go(
    atk_base: int, def_base: int, hp_base: int,
    iv_atk: int, iv_def: int, iv_hp: int,
    nivel: float,
) -> int:
    """Fórmula oficial CP Niantic."""
    cpm = obtener_cpm(nivel)
    atk = (atk_base + iv_atk) * cpm
    def_ = (def_base + iv_def) * cpm
    hp  = (hp_base + iv_hp) * cpm
    return max(10, math.floor(atk * math.sqrt(def_) * math.sqrt(hp) / 10))


def _nivel_optimo_go(
    atk_base: int, def_base: int, hp_base: int,
    iv_atk: int, iv_def: int, iv_hp: int,
    cp_cap: int | None,
) -> tuple[float, int]:
    """Encuentra el nivel máximo que no supera el CP cap."""
    if cp_cap is None:
        return 51.0, _calcular_cp_go(atk_base, def_base, hp_base, iv_atk, iv_def, iv_hp, 51.0)
    niveles = sorted(CPM_TABLE.keys(), reverse=True)
    for nivel in niveles:
        cp = _calcular_cp_go(atk_base, def_base, hp_base, iv_atk, iv_def, iv_hp, nivel)
        if cp <= cp_cap:
            return nivel, cp
    return 1.0, _calcular_cp_go(atk_base, def_base, hp_base, iv_atk, iv_def, iv_hp, 1.0)


def _stats_efectivos_go(datos: dict, iv_atk: int, iv_def: int, iv_hp: int, nivel: float) -> dict:
    """Calcula stats efectivos GO con CPM, IVs y Shadow bonus."""
    cpm = obtener_cpm(nivel)
    shadow_atk = 1.2 if datos.get("shadow") else 1.0
    shadow_def = 0.833 if datos.get("shadow") else 1.0
    sb = datos["stats_go"]
    return {
        "atk": round((sb["ataque"] + iv_atk) * cpm * shadow_atk, 2),
        "def": round((sb["defensa"] + iv_def) * cpm * shadow_def, 2),
        "hp":  max(10, math.floor((sb["resistencia"] + iv_hp) * cpm)),
    }


def _dano_go(atk_efectivo: float, def_efectivo: float, potencia: int, mult: float) -> int:
    """Fórmula daño GO: floor(0.5 × Potencia × Atk/Def × Mult) + 1"""
    return math.floor(0.5 * potencia * (atk_efectivo / max(def_efectivo, 1)) * mult) + 1


def _dps_go(datos: dict, fast_key: str, charged_key: str, stats: dict) -> float:
    """DPS simplificado: (daño_fast/turno + daño_charged/ciclo) / ciclo."""
    fast = FAST_MOVES_GO.get(fast_key)
    charged = CHARGED_MOVES_GO.get(charged_key)
    if not fast or not charged:
        return 0.0

    tipo_stab_bonusx = lambda t: 1.2 if t in datos["tipos"] else 1.0
    eff_fast = efectividad_go(fast["tipo"], ["normal"])  # vs neutro
    eff_charged = efectividad_go(charged["tipo"], ["normal"])

    dmg_fast = _dano_go(stats["atk"], stats["def"], fast["potencia"],
                        eff_fast * tipo_stab_bonusx(fast["tipo"]))
    dmg_charged = _dano_go(stats["atk"], stats["def"], abs(charged["potencia"]),
                           eff_charged * tipo_stab_bonusx(charged["tipo"]))

    energia_por_fast = fast["energia"]
    energia_para_charged = abs(charged["energia"])
    turnos_para_charged = math.ceil(energia_para_charged / energia_por_fast)
    ciclo_turnos = turnos_para_charged + charged["duracion_turnos"]

    dano_ciclo = dmg_fast * turnos_para_charged + dmg_charged
    return round(dano_ciclo / ciclo_turnos, 2)


def _matchup_score_go(
    atacante: dict, defensor: dict,
    iv_atk: int, iv_def: int, iv_hp: int, nivel: float,
    fast_key: str, charged_keys: list[str],
) -> dict:
    """Calcula score en matchup vs amenaza meta GO."""
    stats_atk = _stats_efectivos_go(atacante, iv_atk, iv_def, iv_hp, nivel)

    # Stats del defensor (asumimos 15/15/15 a su nivel óptimo)
    liga_defensor = atacante.get("ligas", ["master"])[0]
    cp_cap = CP_CAPS.get(LigaGO(liga_defensor))
    nivel_def, _ = _nivel_optimo_go(
        defensor["stats_go"]["ataque"], defensor["stats_go"]["defensa"],
        defensor["stats_go"]["resistencia"], 15, 15, 15, cp_cap,
    )
    stats_def = _stats_efectivos_go(defensor, 15, 15, 15, nivel_def)

    best_dps = 0.0
    best_charged = charged_keys[0] if charged_keys else ""
    for ck in charged_keys:
        dps = _dps_go(atacante, fast_key, ck, stats_atk)
        if dps > best_dps:
            best_dps = dps
            best_charged = ck

    # Daño del fast move vs defensor
    fast = FAST_MOVES_GO.get(fast_key, {})
    eff_fast_vs_def = efectividad_go(fast.get("tipo", "normal"), defensor["tipos"])
    stab_fast = 1.2 if fast.get("tipo") in atacante["tipos"] else 1.0
    dmg_por_turno = _dano_go(stats_atk["atk"], stats_def["def"],
                             fast.get("potencia", 1),
                             eff_fast_vs_def * stab_fast)

    turnos_para_ko = math.ceil(stats_def["hp"] / max(dmg_por_turno, 1))

    return {
        "vs": defensor["nombre"],
        "dps": best_dps,
        "mejor_charged": best_charged,
        "turnos_para_ko": turnos_para_ko,
        "efectividad_fast": round(eff_fast_vs_def, 3),
    }


def generar_guia_pokemon_go(nombre: str, liga: str = "great") -> dict:
    """
    Cerebro GO genera guía GO Battle League para un Pokémon.

    Pasos internos del cerebro:
      1. Verifica Pokémon en catálogo GO (stats Niantic, no serie principal)
      2. Busca los mejores IVs para el cap de CP de la liga
      3. Calcula DPS/TDO para cada combinación de movimientos GO
      4. Simula matchups vs amenazas meta de esa liga
      5. Retorna build óptimo con IV spread y moveset GO
    """
    datos = buscar_pokemon_go(nombre)
    if not datos:
        return {
            "ok": False,
            "error": f"'{nombre}' no está disponible en Pokémon GO. "
                     f"Solo Pokémon del catálogo GO con stats Niantic.",
        }

    if liga not in datos.get("ligas", ["master"]) and liga != "master":
        return {
            "ok": False,
            "error": f"'{nombre}' no es meta en liga '{liga}'. Prueba en: {datos.get('ligas')}.",
        }

    try:
        liga_enum = LigaGO(liga)
    except ValueError:
        liga_enum = LigaGO.GREAT

    cp_cap = CP_CAPS[liga_enum]
    sb = datos["stats_go"]

    # ── Buscar IVs óptimos para el CP cap ────────────────────────────────────
    mejor_stat_product = 0
    mejor_ivs = (15, 15, 15)
    mejor_nivel = 40.0
    mejor_cp = 0

    candidatos_ivs = [
        (a, d, h) for a in range(15, -1, -1)
        for d in range(15, -1, -1)
        for h in range(15, -1, -1)
    ] if cp_cap is not None else [(15, 15, 15)]

    for ia, id_, ih in (candidatos_ivs[:500] if cp_cap else [(15, 15, 15)]):
        nivel, cp = _nivel_optimo_go(
            sb["ataque"], sb["defensa"], sb["resistencia"], ia, id_, ih, cp_cap,
        )
        stats = _stats_efectivos_go(datos, ia, id_, ih, nivel)
        product = stats["atk"] * stats["def"] * stats["hp"]
        if product > mejor_stat_product:
            mejor_stat_product = product
            mejor_ivs = (ia, id_, ih)
            mejor_nivel = nivel
            mejor_cp = cp

    stats_optimos = _stats_efectivos_go(datos, *mejor_ivs, mejor_nivel)

    # ── Evaluar combos de movimientos GO ─────────────────────────────────────
    fast_keys = datos.get("fast_moves", [])
    charged_keys = datos.get("charged_moves", [])

    combos_puntuados = []
    for fk in fast_keys:
        fast = FAST_MOVES_GO.get(fk)
        if not fast:
            continue
        for ck1 in charged_keys:
            for ck2 in [None] + [c for c in charged_keys if c != ck1]:
                charged_set = [ck1] + ([ck2] if ck2 else [])
                dps_total = _dps_go(datos, fk, charged_set[0], stats_optimos)

                amenazas_liga = AMENAZAS_META_GO.get(liga, AMENAZAS_META_GO["master"])
                score = 0.0
                matchups = []
                for ak in amenazas_liga[:5]:
                    amenaza = buscar_pokemon_go(ak)
                    if not amenaza or amenaza["nombre"] == datos["nombre"]:
                        continue
                    mu = _matchup_score_go(
                        datos, amenaza, *mejor_ivs, mejor_nivel, fk, charged_set,
                    )
                    score += mu["dps"] * mu["efectividad_fast"]
                    matchups.append(mu)

                combos_puntuados.append({
                    "fast_move": fast["nombre"],
                    "charged_moves": [
                        (CHARGED_MOVES_GO.get(c) or {}).get("nombre", c)
                        for c in charged_set
                    ],
                    "dps_estimado": dps_total,
                    "score": round(score, 2),
                    "matchups": matchups[:3],
                })

    if not combos_puntuados:
        return {"ok": False, "error": "No se pudieron evaluar movimientos para este Pokémon GO."}

    mejores_combos = sorted(combos_puntuados, key=lambda x: x["score"], reverse=True)[:3]

    return {
        "ok": True,
        "juego": "Pokémon GO — GO Battle League",
        "pokemon": datos["nombre"],
        "liga": liga,
        "tipos": datos["tipos"],
        "shadow": datos.get("shadow", False),
        "tabla_tipos_go": _tabla_tipos_go(datos["tipos"]),
        "ivs_optimos": {
            "ataque": mejor_ivs[0],
            "defensa": mejor_ivs[1],
            "hp": mejor_ivs[2],
        },
        "nivel_optimo": mejor_nivel,
        "cp_resultante": mejor_cp,
        "stats_efectivos": stats_optimos,
        "builds_recomendados": mejores_combos,
        "nota_cerebro": (
            "El cerebro GO usó stats Niantic (escala diferente a serie principal). "
            f"STAB ×1.2 | SE ×1.6 | NVE ×0.625 | 'Inmune' ×0.391. "
            "Sin objetos ni habilidades — mecánica GO pura. "
            f"IVs óptimos para liga {liga.upper()} (CP ≤ {cp_cap or '∞'})."
        ),
    }


def generar_mejor_equipo_go(liga: str = "great") -> dict:
    """Genera el equipo meta de 3 Pokémon para una liga GO."""
    meta = AMENAZAS_META_GO.get(liga, AMENAZAS_META_GO["master"])
    cp_cap = CP_CAPS.get(LigaGO(liga) if liga in [l.value for l in LigaGO] else LigaGO.MASTER)

    equipo = []
    for pk_key in meta[:3]:
        datos = buscar_pokemon_go(pk_key)
        if datos:
            equipo.append({
                "pokemon": datos["nombre"],
                "tipos": datos["tipos"],
                "fast_move": datos["fast_moves"][0] if datos["fast_moves"] else "",
                "charged_moves": datos["charged_moves"][:2],
                "shadow": datos.get("shadow", False),
            })

    return {
        "ok": True,
        "juego": "Pokémon GO — GO Battle League",
        "liga": liga,
        "cp_cap": cp_cap,
        "equipo_meta": equipo,
        "nota_cerebro": (
            "Equipo basado en el meta actual de GO Battle League. "
            "Mecánicas GO exclusivas: IVs 0-15, sin naturaleza ni objetos."
        ),
    }


def _tabla_tipos_go(tipos: list[str]) -> dict:
    """Genera tabla de tipo con multiplicadores GO (no ×2 sino ×1.6)."""
    todos = [t.value for t in TipoElemental]
    tabla: dict = {"supereficaz_16x": [], "supereficaz_256x": [],
                   "poco_eficaz_0625x": [], "resistido_0391x": []}
    for ta in todos:
        mult = efectividad_go(ta, tipos)
        if mult >= 2.56:
            tabla["supereficaz_256x"].append(f"×2.56 {ta}")
        elif mult >= 1.6:
            tabla["supereficaz_16x"].append(f"×1.6 {ta}")
        elif mult <= 0.391:
            tabla["resistido_0391x"].append(f"×0.391 {ta}")
        elif mult <= 0.625:
            tabla["poco_eficaz_0625x"].append(f"×0.625 {ta}")
    return tabla
