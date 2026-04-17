"""
cerebros/eyp/engine/guia.py
Motor de generación de guías competitivas para EyP (VGC 2026).

FLUJO:
  1. cerebro.recibir_peticion(pokemon_nombre) → valida en catálogo EyP
  2. cerebro.generar_candidatos() → crea builds con EVs/naturaleza/objeto/movimientos del juego
  3. cerebro.simular_batallas(candidatos, amenazas_meta_eyp) → motor de daño Gen IX
  4. cerebro.seleccionar_mejores(resultados) → top 3 builds con puntuación
  5. retornar GuiaEyP con datos SOLO de EyP (sin mezclar otros juegos)
"""
from __future__ import annotations
import math
from itertools import product as itertools_product

from core.types import TipoElemental
from cerebros.eyp.data.pokemon import POKEMON_EYP, buscar_pokemon_eyp, efectividad_eyp
from cerebros.eyp.data.movimientos import MOVIMIENTOS_EYP, buscar_movimiento_eyp
from cerebros.eyp.data.objetos import OBJETOS_EYP
from cerebros.eyp.models.schemas import (
    PokemonEyP, MovimientoEyP, CategoriaMovimiento,
    NaturalezaEyP, EVsEyP, IVsEyP, PeticionCalculoDanoEyP,
)
from cerebros.eyp.engine.damage import calcular_dano, stat_final


# ── Amenazas meta EyP VGC 2026 que el cerebro usa para simular ───────────────
AMENAZAS_META_EYP: list[dict] = [
    {
        "clave": "flutter_mane", "importancia": 1.0,
        "naturaleza": "timido", "evs": {"hp": 4, "atq_esp": 252, "vel": 252},
        "objeto": "energia_propulsora",
        "movimientos": ["confusion_lunar", "brillo_magico", "sombra_ball", "proteccion"],
    },
    {
        "clave": "incineroar", "importancia": 1.0,
        "naturaleza": "cuidadoso", "evs": {"hp": 252, "def_fis": 4, "def_esp": 252},
        "objeto": "orbe_de_vida",
        "movimientos": ["golpe_karate", "envite_feroz", "cambia_ya", "proteccion"],
    },
    {
        "clave": "rillaboom", "importancia": 0.9,
        "naturaleza": "osado", "evs": {"hp": 252, "atq_fis": 252, "def_fis": 4},
        "objeto": "orbe_de_vida",
        "movimientos": ["tamborileo", "golpe_hierba", "terremoto", "proteccion"],
    },
    {
        "clave": "chi_yu", "importancia": 0.9,
        "naturaleza": "timido", "evs": {"hp": 4, "atq_esp": 252, "vel": 252},
        "objeto": "panuelo_elegante",
        "movimientos": ["llamarada_oscura", "lanzallamas", "sombra_ball", "proteccion"],
    },
    {
        "clave": "urshifu_single", "importancia": 0.85,
        "naturaleza": "osado", "evs": {"hp": 4, "atq_fis": 252, "vel": 252},
        "objeto": "faja_de_enfoque",
        "movimientos": ["golpe_maestro", "a_bocajarro", "acua_tail", "proteccion"],
    },
    {
        "clave": "gholdengo", "importancia": 0.85,
        "naturaleza": "timido", "evs": {"hp": 4, "atq_esp": 252, "vel": 252},
        "objeto": "orbe_de_vida",
        "movimientos": ["esfuerzo_supremo", "sombra_ball", "flash_cannon", "proteccion"],
    },
    {
        "clave": "landorus_therian", "importancia": 0.8,
        "naturaleza": "timido", "evs": {"hp": 4, "atq_fis": 252, "vel": 252},
        "objeto": "orbe_de_vida",
        "movimientos": ["terremoto", "roca_afilada", "bofeton_lodo", "proteccion"],
    },
    {
        "clave": "calyrex_shadow", "importancia": 0.75,
        "naturaleza": "timido", "evs": {"hp": 4, "atq_esp": 252, "vel": 252},
        "objeto": "panuelo_elegante",
        "movimientos": ["galopar_espectral", "psicocarga", "sombra_ball", "proteccion"],
    },
    {
        "clave": "miraidon", "importancia": 0.75,
        "naturaleza": "timido", "evs": {"hp": 4, "atq_esp": 252, "vel": 252},
        "objeto": "energia_propulsora",
        "movimientos": ["voltio_cruel", "trueno", "pulso_dragon", "proteccion"],
    },
    {
        "clave": "koraidon", "importancia": 0.75,
        "naturaleza": "osado", "evs": {"hp": 4, "atq_fis": 252, "vel": 252},
        "objeto": "energia_propulsora",
        "movimientos": ["ciclotorrente", "garra_dragon", "terremoto", "proteccion"],
    },
]

# Naturalezas viables por perfil del Pokémon
_NATURALEZAS_OFENSIVAS_ESP = ["timido", "modesto"]
_NATURALEZAS_OFENSIVAS_FIS = ["osado", "audaz"]
_NATURALEZAS_BULKY       = ["relajado", "manso", "gentil", "calmado", "flojo"]

# Spreads de EVs más comunes en VGC competitivo
_EV_SPREADS = [
    {"atq_esp": 252, "vel": 252, "hp": 4},                         # Max SpA/Spe ofensivo
    {"atq_fis": 252, "vel": 252, "hp": 4},                         # Max Atk/Spe ofensivo
    {"hp": 252, "def_esp": 252, "atq_esp": 4},                     # Max HP/SpD bulky esp
    {"hp": 252, "def_fis": 252, "atq_fis": 4},                     # Max HP/Def bulky fis
    {"hp": 252, "atq_esp": 252, "def_esp": 4},                     # Atk + Bulk
    {"hp": 172, "def_fis": 84, "vel": 252},                        # Bulky rápido
    {"hp": 252, "vel": 252, "atq_esp": 4},                         # HP + Velocidad
    {"atq_fis": 252, "atq_esp": 4, "vel": 252},                    # Mixed rápido
]


def _construir_pokemon_eyp(
    clave: str,
    datos: dict,
    naturaleza_str: str,
    ev_spread: dict,
    objeto_clave: str | None,
    movimientos_clave: list[str],
) -> PokemonEyP | None:
    """Construye un PokemonEyP desde el catálogo EyP con los parámetros dados."""
    movs = []
    for mk in movimientos_clave[:4]:
        mov_datos = buscar_movimiento_eyp(mk)
        if not mov_datos:
            continue
        try:
            movs.append(MovimientoEyP(
                nombre=mov_datos["nombre"],
                tipo=TipoElemental(mov_datos["tipo"]),
                categoria=CategoriaMovimiento(mov_datos["categoria"]),
                potencia=mov_datos.get("potencia"),
                precision=mov_datos.get("precision"),
                pp=mov_datos["pp"],
                prioridad=mov_datos.get("prioridad", 0),
            ))
        except Exception:
            continue

    if not movs:
        return None

    ev_fields = {
        "hp": ev_spread.get("hp", 0),
        "atq_fis": ev_spread.get("atq_fis", 0),
        "def_fis": ev_spread.get("def_fis", 0),
        "atq_esp": ev_spread.get("atq_esp", 0),
        "def_esp": ev_spread.get("def_esp", 0),
        "vel": ev_spread.get("vel", 0),
    }
    total_ev = sum(ev_fields.values())
    if total_ev > 510:
        return None

    try:
        nat_enum = NaturalezaEyP(naturaleza_str)
    except ValueError:
        nat_enum = NaturalezaEyP.SERIO

    return PokemonEyP(
        nombre=datos["nombre"],
        tipos=[TipoElemental(t) for t in datos["tipos"]],
        habilidad=datos["habilidades"][0],
        item=objeto_clave,
        naturaleza=nat_enum,
        nivel=50,
        stats_base=datos["stats"],
        evs=EVsEyP(**ev_fields),
        ivs=IVsEyP(),
        movimientos=movs,
    )


def _puntuar_build_vs_amenazas(
    pokemon: PokemonEyP,
    objeto_datos: dict | None,
) -> dict:
    """
    Simula el build contra las amenazas meta EyP.
    Retorna: {score, victorias, empates, derrotas, detalles}
    """
    victorias = 0
    empates = 0
    derrotas = 0
    score = 0.0
    detalles: list[dict] = []

    for amenaza_cfg in AMENAZAS_META_EYP:
        amenaza_data = buscar_pokemon_eyp(amenaza_cfg["clave"])
        if not amenaza_data:
            continue

        amenaza_ev = {
            "hp": 0, "atq_fis": 0, "def_fis": 0,
            "atq_esp": 0, "def_esp": 0, "vel": 0,
        }
        amenaza_ev.update(amenaza_cfg.get("evs", {}))

        amenaza_pokemon = _construir_pokemon_eyp(
            amenaza_cfg["clave"], amenaza_data,
            amenaza_cfg["naturaleza"], amenaza_ev,
            None, amenaza_cfg["movimientos"],
        )
        if not amenaza_pokemon:
            continue

        importancia = amenaza_cfg["importancia"]

        # Mejor movimiento del candidato vs la amenaza
        mejor_dano_pct = _mejor_movimiento_dano(pokemon, amenaza_pokemon)
        # Mejor movimiento de la amenaza vs el candidato
        dano_recibido_pct = _mejor_movimiento_dano(amenaza_pokemon, pokemon)

        resultado = {
            "vs": amenaza_data["nombre"],
            "dano_infligido_pct": round(mejor_dano_pct * 100, 1),
            "dano_recibido_pct": round(dano_recibido_pct * 100, 1),
        }

        # Victoria si puede OHKO o 2HKO sin recibir OHKO
        if mejor_dano_pct >= 1.0:
            resultado["resultado"] = "OHKO"
            score += importancia * 3
            victorias += 1
        elif mejor_dano_pct >= 0.5:
            if dano_recibido_pct < 1.0:
                resultado["resultado"] = "2HKO"
                score += importancia * 2
                victorias += 1
            else:
                resultado["resultado"] = "intercambio"
                score += importancia * 1
                empates += 1
        elif dano_recibido_pct < 1.0:
            resultado["resultado"] = "tanquea"
            score += importancia * 0.5
            empates += 1
        else:
            resultado["resultado"] = "desfavorable"
            derrotas += 1

        detalles.append(resultado)

    return {
        "score": round(score, 2),
        "victorias": victorias,
        "empates": empates,
        "derrotas": derrotas,
        "detalles": detalles,
    }


def _mejor_movimiento_dano(atacante: PokemonEyP, defensor: PokemonEyP) -> float:
    """Retorna el porcentaje de HP máximo que hace el mejor movimiento de daño."""
    mejor = 0.0
    for mov in atacante.movimientos:
        if mov.potencia is None:
            continue
        try:
            req = PeticionCalculoDanoEyP(
                atacante=atacante, defensor=defensor, movimiento=mov,
            )
            res = calcular_dano(req)
            pct = res.dano_maximo / res.hp_defensor if res.hp_defensor > 0 else 0.0
            if pct > mejor:
                mejor = pct
        except Exception:
            continue
    return mejor


def generar_guia_pokemon_eyp(nombre: str) -> dict:
    """
    Cerebro EyP genera una guía competitiva completa para un Pokémon.

    Pasos internos del cerebro:
      1. Verifica que el Pokémon esté en el catálogo EyP
      2. Genera candidatos (naturaleza × EVs × objeto × movimientos)
      3. Simula batallas vs amenazas meta EyP
      4. Retorna los 3 mejores builds ordenados por puntuación
    """
    datos = buscar_pokemon_eyp(nombre)
    if not datos:
        return {
            "ok": False,
            "error": f"'{nombre}' no está disponible en Escarlata/Púrpura. "
                     f"Verifica que sea un Pokémon de la Pokédex de Paldea o DLC.",
        }

    # Determinar perfiles viables según el Pokémon
    stats = datos["stats"]
    es_especial = stats["atq_esp"] > stats["atq_fis"]
    es_fisico = stats["atq_fis"] >= stats["atq_esp"]
    es_rapido = stats["vel"] >= 100

    naturalezas_candidatas = []
    if es_especial:
        naturalezas_candidatas = _NATURALEZAS_OFENSIVAS_ESP + ["calmado", "manso"]
    elif es_fisico:
        naturalezas_candidatas = _NATURALEZAS_OFENSIVAS_FIS + ["relajado", "gentil"]
    else:
        naturalezas_candidatas = ["serio", "timido", "osado"]

    # Seleccionar movimientos de daño del Pokémon
    movs_disponibles = [
        mk for mk in datos["movimientos"]
        if mk in MOVIMIENTOS_EYP and MOVIMIENTOS_EYP[mk]["potencia"] is not None
    ]
    movs_estado = [
        mk for mk in datos["movimientos"]
        if mk in MOVIMIENTOS_EYP and MOVIMIENTOS_EYP[mk]["potencia"] is None
    ]

    # Siempre incluir Protección si disponible
    movset_base = movs_disponibles[:3]
    if "proteccion" in datos["movimientos"] and "proteccion" not in movset_base:
        movset_base = movs_disponibles[:2] + ["proteccion"]
    elif movs_estado:
        movset_base = movs_disponibles[:2] + movs_estado[:1] + ["proteccion"]

    # Objetos candidatos según perfil
    objetos_candidatos = ["orbe_de_vida", "faja_de_enfoque", "panuelo_elegante"]
    if es_especial:
        objetos_candidatos = ["orbe_de_vida", "panuelo_elegante", "lentes_de_decision", "energia_propulsora"]
    elif es_fisico:
        objetos_candidatos = ["orbe_de_vida", "panuelo_elegante", "cinta_de_decision", "faja_de_enfoque"]

    # ── Fase de simulación interna del cerebro ────────────────────────────────
    candidatos_puntuados: list[dict] = []

    for naturaleza, ev_spread, objeto_clave in itertools_product(
        naturalezas_candidatas[:3], _EV_SPREADS[:5], objetos_candidatos[:3]
    ):
        # Verificar objeto existe en catálogo EyP
        objeto_datos = OBJETOS_EYP.get(objeto_clave)

        pokemon = _construir_pokemon_eyp(
            nombre.lower().replace(" ", "_"),
            datos,
            naturaleza,
            ev_spread,
            objeto_datos["nombre"] if objeto_datos else None,
            movset_base,
        )
        if not pokemon:
            continue

        puntuacion = _puntuar_build_vs_amenazas(pokemon, objeto_datos)
        candidatos_puntuados.append({
            "naturaleza": naturaleza,
            "ev_spread": ev_spread,
            "objeto": objeto_datos["nombre"] if objeto_datos else None,
            "movimientos": [m.nombre for m in pokemon.movimientos],
            "stats_nivel_50": _calcular_stats_finales(datos["stats"], ev_spread, naturaleza),
            **puntuacion,
        })

    if not candidatos_puntuados:
        return {"ok": False, "error": "No se pudieron generar candidatos para este Pokémon."}

    # Ordenar por score y retornar top 3
    mejores = sorted(candidatos_puntuados, key=lambda x: x["score"], reverse=True)[:3]

    return {
        "ok": True,
        "juego": "Escarlata/Púrpura — VGC 2026",
        "pokemon": datos["nombre"],
        "tipos": datos["tipos"],
        "habilidades_disponibles": datos["habilidades"],
        "restringido_vgc": datos.get("restringido", False),
        "tabla_tipos": _tabla_tipos_pokemon(datos["tipos"]),
        "builds_recomendados": mejores,
        "nota_cerebro": (
            "El cerebro EyP simuló cada build contra las 10 amenazas meta más usadas en VGC 2026. "
            "Score = victorias × importancia_meta. Solo se usaron Pokémon, movimientos y "
            "objetos disponibles en la Pokédex de Paldea + DLC."
        ),
    }


def generar_mejor_equipo_eyp(pokemon_ancla: str, formato: str = "vgc2026") -> dict:
    """
    Genera el mejor equipo de 6 (dobles VGC) alrededor de un Pokémon ancla.
    Solo usa Pokémon disponibles en EyP.
    """
    ancla_datos = buscar_pokemon_eyp(pokemon_ancla)
    if not ancla_datos:
        return {
            "ok": False,
            "error": f"'{pokemon_ancla}' no disponible en EyP.",
        }

    # Compañeros sinérgicos según tipos del ancla
    tipos_ancla = ancla_datos["tipos"]
    compañeros_viables = _seleccionar_companeros(pokemon_ancla, tipos_ancla, formato)

    equipo: list[dict] = [{"pokemon": ancla_datos["nombre"], "rol": "ancla"}]
    for comp in compañeros_viables[:5]:
        comp_datos = buscar_pokemon_eyp(comp["clave"])
        if comp_datos:
            equipo.append({"pokemon": comp_datos["nombre"], "rol": comp["rol"]})

    return {
        "ok": True,
        "juego": "Escarlata/Púrpura — VGC 2026",
        "formato": formato,
        "equipo": equipo,
        "nota_cerebro": (
            "Equipo generado usando solo Pokémon de la Pokédex de Paldea + DLC. "
            "Máx 1 legendario restringido. Balance ofensivo/defensivo y coberturas de tipo."
        ),
    }


# ── Helpers internos ──────────────────────────────────────────────────────────

def _calcular_stats_finales(stats_base: dict, ev_spread: dict, naturaleza: str) -> dict:
    """Calcula los stats finales a nivel 50 con los EVs y naturaleza dados."""
    try:
        nat = NaturalezaEyP(naturaleza)
    except ValueError:
        nat = NaturalezaEyP.SERIO

    resultado = {}
    for clave_base, clave_stat in [
        ("hp", "hp"), ("atq_fis", "atq_fis"), ("def_fis", "def_fis"),
        ("atq_esp", "atq_esp"), ("def_esp", "def_esp"), ("vel", "vel"),
    ]:
        resultado[clave_stat] = stat_final(
            base=stats_base[clave_base],
            ev=ev_spread.get(clave_stat, 0),
            iv=31,
            nivel=50,
            es_hp=(clave_stat == "hp"),
            naturaleza=nat,
            stat_key=clave_stat,
        )
    return resultado


def _tabla_tipos_pokemon(tipos: list[str]) -> dict:
    """Genera la tabla de fortalezas/debilidades del Pokémon en EyP."""
    todos_tipos = [t.value for t in TipoElemental]
    tabla: dict = {"supereficaz": [], "poco_eficaz": [], "sin_efecto": [], "normal": []}
    for tipo_ataque in todos_tipos:
        mult = efectividad_eyp(tipo_ataque, tipos)
        if mult >= 4.0:
            tabla["supereficaz"].append(f"×4 {tipo_ataque}")
        elif mult >= 2.0:
            tabla["supereficaz"].append(f"×2 {tipo_ataque}")
        elif mult == 0.0:
            tabla["sin_efecto"].append(tipo_ataque)
        elif mult <= 0.25:
            tabla["poco_eficaz"].append(f"×0.25 {tipo_ataque}")
        elif mult <= 0.5:
            tabla["poco_eficaz"].append(f"×0.5 {tipo_ataque}")
    return tabla


def _seleccionar_companeros(
    ancla_clave: str,
    tipos_ancla: list[str],
    formato: str,
) -> list[dict]:
    """Selecciona compañeros sinérgicos para el equipo VGC."""
    roles_necesarios = ["lluvia_sol", "apoyo_velocidad", "tanque", "rematador", "cobertura"]

    # Compañeros predefinidos por sinergia meta VGC 2026
    sinergias: dict[str, list[dict]] = {
        "electrico": [
            {"clave": "pelipper", "rol": "setter_lluvia"},
            {"clave": "incineroar", "rol": "intimidacion_apoyo"},
            {"clave": "flutter_mane", "rol": "especial_ofensivo"},
        ],
        "agua": [
            {"clave": "rillaboom", "rol": "zona_hierba_apoyo"},
            {"clave": "incineroar", "rol": "intimidacion_apoyo"},
            {"clave": "gholdengo", "rol": "acero_ofensivo"},
        ],
        "fuego": [
            {"clave": "torkoal", "rol": "setter_sol"},
            {"clave": "rillaboom", "rol": "zona_hierba_cobertura"},
            {"clave": "landorus_therian", "rol": "pivot_intimidacion"},
        ],
        "default": [
            {"clave": "incineroar", "rol": "intimidacion_apoyo"},
            {"clave": "flutter_mane", "rol": "especial_ofensivo"},
            {"clave": "rillaboom", "rol": "zona_hierba"},
            {"clave": "landorus_therian", "rol": "pivot"},
            {"clave": "gholdengo", "rol": "bloqueador"},
        ],
    }

    for tipo in tipos_ancla:
        if tipo in sinergias:
            base = sinergias[tipo]
            base_filtrada = [c for c in base if c["clave"] != ancla_clave]
            # Completar con default
            default_filtrado = [c for c in sinergias["default"]
                                 if c["clave"] != ancla_clave
                                 and c["clave"] not in {b["clave"] for b in base_filtrada}]
            return (base_filtrada + default_filtrado)[:5]

    return [c for c in sinergias["default"] if c["clave"] != ancla_clave][:5]
