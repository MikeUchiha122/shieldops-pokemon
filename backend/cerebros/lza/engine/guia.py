"""
cerebros/lza/engine/guia.py
Motor de guías para Leyendas Z-A — Action Time PvP.

Mecánicas clave del cerebro LZA:
- Sin EVs / IVs / Naturaleza (stats directos del catálogo)
- La velocidad importa como cooldown_ms y startup_frames
- Mega Evolución: cambia tipos → recalcular efectividad de tabla de tipos LZA
- Habilidades DESACTIVADAS: solo tipo determina inmunidades
- Equipos de 3 Pokémon, máx 3 switches
"""
from __future__ import annotations
import math

from cerebros.lza.data.pokemon import POKEMON_LZA, buscar_pokemon_lza, efectividad_lza
from cerebros.lza.data.movimientos import MOVIMIENTOS_LZA, buscar_movimiento_lza
from cerebros.lza.data.objetos import OBJETOS_LZA
from core.types import TipoElemental


# ── Amenazas meta LZA para simulación interna del cerebro ────────────────────
AMENAZAS_META_LZA: list[dict] = [
    {"clave": "garchomp",   "importancia": 1.0, "objeto": "orbe_de_vida",    "usar_mega": True},
    {"clave": "mewtwo",     "importancia": 1.0, "objeto": "piedra_megay",    "usar_mega": True},
    {"clave": "charizard",  "importancia": 0.9, "objeto": "piedra_megax",    "usar_mega": True},
    {"clave": "lucario",    "importancia": 0.9, "objeto": "orbe_de_vida",    "usar_mega": True},
    {"clave": "greninja",   "importancia": 0.85,"objeto": "turbocinta",      "usar_mega": False},
    {"clave": "salamence",  "importancia": 0.85,"objeto": "orbe_de_vida",    "usar_mega": True},
    {"clave": "gardevoir",  "importancia": 0.8, "objeto": "piedra_de_mega",  "usar_mega": True},
    {"clave": "gengar",     "importancia": 0.8, "objeto": "piedra_de_mega",  "usar_mega": True},
    {"clave": "tyranitar",  "importancia": 0.75,"objeto": "orbe_de_vida",    "usar_mega": True},
    {"clave": "talonflame", "importancia": 0.7, "objeto": "turbocinta",      "usar_mega": False},
]


def _dano_lza(
    potencia: int,
    ataque: int,
    defensa: int,
    efectividad: float,
    stab: bool,
    quemadura: bool = False,
    orbe_de_vida: bool = False,
) -> int:
    """
    Fórmula de daño LZA (Action Time — determinista, sin rolls).
    Daño = floor((Atk / Def) * Potencia / 50 + 2) * Efectividad * STAB * Modificadores
    """
    stab_mult = 1.5 if stab else 1.0
    orbe_mult = 1.3 if orbe_de_vida else 1.0
    quemadura_mult = 0.5 if quemadura else 1.0

    dano_base = math.floor((ataque / max(defensa, 1)) * potencia / 50 + 2)
    return max(1, math.floor(dano_base * efectividad * stab_mult * orbe_mult * quemadura_mult))


def _mejor_dano_lza(
    atacante_datos: dict,
    defensor_datos: dict,
    atacante_mega: bool = False,
    defensor_mega: bool = False,
    objeto_atacante: str | None = None,
) -> tuple[int, str, float]:
    """
    Retorna (daño_máximo, nombre_movimiento, porcentaje_hp_defensor).
    Considera tipos del defensor — con Mega si aplica.
    """
    tipos_def = (
        defensor_datos.get("tipos_mega") or
        defensor_datos.get("tipos_mega_x") or
        defensor_datos["tipos"]
    ) if defensor_mega else defensor_datos["tipos"]

    tipos_atk = (
        atacante_datos.get("tipos_mega") or
        atacante_datos.get("tipos_mega_x") or
        atacante_datos["tipos"]
    ) if atacante_mega else atacante_datos["tipos"]

    stats_atk = (
        atacante_datos.get("stats_mega") or
        atacante_datos.get("stats_mega_x") or
        atacante_datos["stats"]
    ) if atacante_mega else atacante_datos["stats"]

    stats_def = (
        defensor_datos.get("stats_mega") or
        defensor_datos.get("stats_mega_x") or
        defensor_datos["stats"]
    ) if defensor_mega else defensor_datos["stats"]

    hp_defensor = stats_def["hp"]
    tiene_orbe = objeto_atacante == "orbe_de_vida"

    mejor_dano = 0
    mejor_mov = ""
    for mk in atacante_datos.get("movimientos", []):
        mov = buscar_movimiento_lza(mk)
        if not mov or mov.get("potencia") is None:
            continue
        eff = efectividad_lza(mov["tipo"], tipos_def)
        if eff == 0:
            continue
        stab = mov["tipo"] in tipos_atk
        d = _dano_lza(
            mov["potencia"], stats_atk["ataque"], stats_def["defensa"],
            eff, stab, orbe_de_vida=tiene_orbe,
        )
        if d > mejor_dano:
            mejor_dano = d
            mejor_mov = mov["nombre"]

    pct = round(mejor_dano / max(hp_defensor, 1) * 100, 1)
    return mejor_dano, mejor_mov, pct


def _velocidad_efectiva_lza(datos: dict, mega: bool, objeto: str | None) -> dict:
    """Calcula cooldown efectivo considerando objeto (turbocinta reduce 15%)."""
    turbocinta = objeto == "turbocinta"
    amuleto   = objeto == "amuleto_de_startup"

    mejor_cd = min(
        (buscar_movimiento_lza(mk) or {}).get("cooldown_ms", 9999)
        for mk in datos.get("movimientos", [])
        if buscar_movimiento_lza(mk) and buscar_movimiento_lza(mk).get("potencia")
    ) if datos.get("movimientos") else 9999

    if turbocinta:
        mejor_cd = int(mejor_cd * 0.85)

    mejor_sf = min(
        (buscar_movimiento_lza(mk) or {}).get("startup_frames", 99)
        for mk in datos.get("movimientos", [])
        if buscar_movimiento_lza(mk) and buscar_movimiento_lza(mk).get("potencia")
    ) if datos.get("movimientos") else 99

    if amuleto:
        mejor_sf = max(1, mejor_sf - 3)

    return {"cooldown_ms": mejor_cd, "startup_frames": mejor_sf, "puede_esquivar": mejor_sf > 12}


def generar_guia_pokemon_lza(nombre: str) -> dict:
    """
    Cerebro LZA genera guía Action Time PvP para un Pokémon.

    Pasos del cerebro:
      1. Verifica que el Pokémon esté en el catálogo LZA (Kalos + confirmados)
      2. Evalúa configuraciones: con/sin Mega, objeto, moveset
      3. Simula confrontaciones vs amenazas meta LZA
      4. Considera startup_frames (esquivabilidad) y cooldown (velocidad)
      5. Retorna los 2 mejores builds (normal + Mega si aplica)
    """
    datos = buscar_pokemon_lza(nombre)
    if not datos:
        return {
            "ok": False,
            "error": f"'{nombre}' no está disponible en Leyendas Z-A. "
                     f"Solo Pokémon de la región Kalos y confirmados en LZA.",
        }

    puede_mega = datos.get("puede_mega", False)
    objetos_candidatos = ["orbe_de_vida", "faja_de_enfoque", "turbocinta", "restos"]
    if puede_mega:
        objetos_candidatos = ["piedra_de_mega", "piedra_megax", "piedra_megay",
                               "orbe_de_vida", "turbocinta"]

    builds_puntuados: list[dict] = []

    for objeto_clave in objetos_candidatos[:3]:
        for usar_mega in ([True, False] if puede_mega else [False]):
            objeto_datos = OBJETOS_LZA.get(objeto_clave)

            # Verificar coherencia: piedra solo si puede mega
            if usar_mega and not puede_mega:
                continue
            if objeto_clave in ("piedra_de_mega", "piedra_megax", "piedra_megay") and not puede_mega:
                continue

            score = 0.0
            victorias = 0
            derrotas = 0
            detalles = []

            vel = _velocidad_efectiva_lza(datos, usar_mega, objeto_clave)

            for amenaza_cfg in AMENAZAS_META_LZA:
                amenaza = buscar_pokemon_lza(amenaza_cfg["clave"])
                if not amenaza:
                    continue

                importancia = amenaza_cfg["importancia"]
                amenaza_mega = amenaza_cfg.get("usar_mega", False) and amenaza.get("puede_mega", False)

                dano_inf, mov_usado, pct_inf = _mejor_dano_lza(
                    datos, amenaza, usar_mega, amenaza_mega, objeto_clave,
                )
                dano_rec, _, pct_rec = _mejor_dano_lza(
                    amenaza, datos, amenaza_mega, usar_mega, amenaza_cfg.get("objeto"),
                )

                resultado_str = "desfavorable"
                if pct_inf >= 100:
                    resultado_str = "OHKO"
                    score += importancia * 3
                    victorias += 1
                elif pct_inf >= 50:
                    resultado_str = "2HKO"
                    score += importancia * 2
                    victorias += 1
                elif pct_rec < 100:
                    resultado_str = "tanquea"
                    score += importancia * 0.5
                else:
                    derrotas += 1

                detalles.append({
                    "vs": amenaza["nombre"] + (" Mega" if amenaza_mega else ""),
                    "movimiento_usado": mov_usado,
                    "dano_infligido_pct": pct_inf,
                    "dano_recibido_pct": pct_rec,
                    "resultado": resultado_str,
                    "puede_esquivar_su_ataque": vel["puede_esquivar"],
                })

            # Bonus por velocidad (cooldown bajo = más turnos de acción)
            if vel["cooldown_ms"] < 1200:
                score += 1.5
            elif vel["cooldown_ms"] < 1500:
                score += 0.5

            tipos_activos = (
                datos.get("tipos_mega") or datos.get("tipos_mega_x") or datos["tipos"]
            ) if usar_mega else datos["tipos"]

            builds_puntuados.append({
                "configuracion": "Con Mega" if usar_mega else "Sin Mega",
                "objeto": objeto_datos["nombre"] if objeto_datos else objeto_clave,
                "tipos_activos": tipos_activos,
                "stats_activos": (
                    datos.get("stats_mega") or datos.get("stats_mega_x") or datos["stats"]
                ) if usar_mega else datos["stats"],
                "movimientos": datos.get("movimientos", [])[:4],
                "cooldown_mejor_ms": vel["cooldown_ms"],
                "startup_frames_mejor": vel["startup_frames"],
                "movimientos_esquivables_propios": vel["puede_esquivar"],
                "score": round(score, 2),
                "victorias": victorias,
                "derrotas": derrotas,
                "detalles": detalles,
            })

    if not builds_puntuados:
        return {"ok": False, "error": "No se pudieron generar builds para este Pokémon LZA."}

    mejores = sorted(builds_puntuados, key=lambda x: x["score"], reverse=True)[:2]

    return {
        "ok": True,
        "juego": "Leyendas Z-A — Action Time PvP",
        "pokemon": datos["nombre"],
        "tipos_base": datos["tipos"],
        "puede_mega": puede_mega,
        "tabla_tipos": _tabla_tipos_lza(datos["tipos"]),
        "tabla_tipos_mega": _tabla_tipos_lza(
            datos.get("tipos_mega") or datos.get("tipos_mega_x") or datos["tipos"]
        ) if puede_mega else None,
        "builds_recomendados": mejores,
        "nota_cerebro": (
            "El cerebro LZA simuló Action Time PvP con startup_frames y cooldowns reales. "
            "Sin habilidades activas — efectividad de tipo determina inmunidades. "
            "Mega Evolución: 1 por combate — cambia tipos del Pokémon → tabla de tipos recalculada. "
            "Solo Pokémon del catálogo Kalos/LZA."
        ),
    }


def generar_mejor_equipo_lza(pokemon_ancla: str) -> dict:
    """Genera equipo de 3 para LZA alrededor de un Pokémon ancla."""
    ancla = buscar_pokemon_lza(pokemon_ancla)
    if not ancla:
        return {"ok": False, "error": f"'{pokemon_ancla}' no disponible en LZA."}

    tipos_ancla = ancla["tipos"]
    compañeros = _sinergias_lza(pokemon_ancla, tipos_ancla)

    return {
        "ok": True,
        "juego": "Leyendas Z-A — Action Time PvP",
        "equipo": [
            {"pokemon": ancla["nombre"], "rol": "ancla", "puede_mega": ancla.get("puede_mega", False)},
            *compañeros[:2],
        ],
        "nota_cerebro": (
            "Equipo de 3 para LZA. 1 Mega permitida. Máx 3 switches. "
            "Solo Pokémon del catálogo Kalos/LZA."
        ),
    }


def _tabla_tipos_lza(tipos: list[str]) -> dict:
    todos = [t.value for t in TipoElemental]
    tabla: dict = {"supereficaz": [], "poco_eficaz": [], "sin_efecto": []}
    for ta in todos:
        mult = efectividad_lza(ta, tipos)
        if mult >= 4.0:
            tabla["supereficaz"].append(f"×4 {ta}")
        elif mult >= 2.0:
            tabla["supereficaz"].append(f"×2 {ta}")
        elif mult == 0.0:
            tabla["sin_efecto"].append(ta)
        elif mult <= 0.25:
            tabla["poco_eficaz"].append(f"×0.25 {ta}")
        elif mult <= 0.5:
            tabla["poco_eficaz"].append(f"×0.5 {ta}")
    return tabla


def _sinergias_lza(ancla_clave: str, tipos: list[str]) -> list[dict]:
    sinergias_map = {
        "dragon": [
            {"pokemon": "Togekiss",  "rol": "hada_contra_dragon", "puede_mega": False},
            {"pokemon": "Greninja",  "rol": "rapido_cobertura",   "puede_mega": False},
        ],
        "fuego": [
            {"pokemon": "Gyarados",  "rol": "agua_cobertura",     "puede_mega": True},
            {"pokemon": "Gardevoir", "rol": "hada_apoyo",         "puede_mega": True},
        ],
        "psiquico": [
            {"pokemon": "Gengar",    "rol": "fantasma_ofensivo",  "puede_mega": True},
            {"pokemon": "Tyranitar", "rol": "roca_siniestro",     "puede_mega": True},
        ],
        "default": [
            {"pokemon": "Lucario",   "rol": "lucha_acero",        "puede_mega": True},
            {"pokemon": "Salamence", "rol": "dragon_volador",     "puede_mega": True},
        ],
    }
    for tipo in tipos:
        if tipo in sinergias_map:
            return [c for c in sinergias_map[tipo]
                    if c["pokemon"].lower() != ancla_clave.lower()][:2]
    return sinergias_map["default"]
