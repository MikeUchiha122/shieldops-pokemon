"""
cerebros/champions/engine/guia.py
Motor de guía para Pokémon Champions — Singles multi-generacional.
El cerebro simula internamente batallas contra amenazas meta para
determinar el mejor set de movimientos, objeto y naturaleza.
"""
from __future__ import annotations
import math
from cerebros.champions.data.pokemon import (
    POKEMON_CHAMPIONS, buscar_pokemon_champions, efectividad_champions,
)
from cerebros.champions.data.movimientos import MOVIMIENTOS_CHAMPIONS
from cerebros.champions.data.objetos import OBJETOS_CHAMPIONS
from cerebros.champions.models.schemas import NATURALEZA_MODIFICADORES

# ── Amenazas meta Singles ─────────────────────────────────────────────────────
AMENAZAS_META_CHAMPIONS: list[dict] = [
    {
        "nombre": "Flutter Mane",
        "tipos": ["fantasma", "hada"],
        "stats": {"hp": 55, "ataque": 55, "defensa": 55, "ataque_especial": 135,
                  "defensa_especial": 135, "velocidad": 135},
        "movimiento": "brillo_magico", "tipo_mov": "hada", "cat": "especial",
        "potencia": 80, "peso_meta": 1.4,
    },
    {
        "nombre": "Iron Bundle",
        "tipos": ["agua", "hielo"],
        "stats": {"hp": 56, "ataque": 80, "defensa": 114, "ataque_especial": 124,
                  "defensa_especial": 60, "velocidad": 136},
        "movimiento": "hidrobomba", "tipo_mov": "agua", "cat": "especial",
        "potencia": 110, "peso_meta": 1.3,
    },
    {
        "nombre": "Landorus-T",
        "tipos": ["tierra", "volador"],
        "stats": {"hp": 89, "ataque": 145, "defensa": 90, "ataque_especial": 105,
                  "defensa_especial": 80, "velocidad": 91},
        "movimiento": "terremoto", "tipo_mov": "tierra", "cat": "fisico",
        "potencia": 100, "peso_meta": 1.3,
    },
    {
        "nombre": "Heatran",
        "tipos": ["fuego", "acero"],
        "stats": {"hp": 91, "ataque": 90, "defensa": 106, "ataque_especial": 130,
                  "defensa_especial": 106, "velocidad": 77},
        "movimiento": "llamarada", "tipo_mov": "fuego", "cat": "especial",
        "potencia": 110, "peso_meta": 1.2,
    },
    {
        "nombre": "Toxapex",
        "tipos": ["veneno", "agua"],
        "stats": {"hp": 50, "ataque": 63, "defensa": 152, "ataque_especial": 53,
                  "defensa_especial": 142, "velocidad": 35},
        "movimiento": "surf", "tipo_mov": "agua", "cat": "especial",
        "potencia": 90, "peso_meta": 1.1,
    },
    {
        "nombre": "Dragapult",
        "tipos": ["dragon", "fantasma"],
        "stats": {"hp": 88, "ataque": 120, "defensa": 75, "ataque_especial": 100,
                  "defensa_especial": 75, "velocidad": 142},
        "movimiento": "draco_meteoro", "tipo_mov": "dragon", "cat": "especial",
        "potencia": 130, "peso_meta": 1.2,
    },
    {
        "nombre": "Tyranitar",
        "tipos": ["roca", "siniestro"],
        "stats": {"hp": 100, "ataque": 134, "defensa": 110, "ataque_especial": 95,
                  "defensa_especial": 100, "velocidad": 61},
        "movimiento": "roca_afilada", "tipo_mov": "roca", "cat": "fisico",
        "potencia": 100, "peso_meta": 1.1,
    },
    {
        "nombre": "Clefable",
        "tipos": ["normal"],
        "stats": {"hp": 95, "ataque": 70, "defensa": 73, "ataque_especial": 95,
                  "defensa_especial": 90, "velocidad": 60},
        "movimiento": "voz_cautivadora", "tipo_mov": "hada", "cat": "especial",
        "potencia": 90, "peso_meta": 1.0,
    },
    {
        "nombre": "Garchomp",
        "tipos": ["dragon", "tierra"],
        "stats": {"hp": 108, "ataque": 130, "defensa": 95, "ataque_especial": 80,
                  "defensa_especial": 85, "velocidad": 102},
        "movimiento": "terremoto", "tipo_mov": "tierra", "cat": "fisico",
        "potencia": 100, "peso_meta": 1.2,
    },
    {
        "nombre": "Kyurem-Black",
        "tipos": ["dragon", "hielo"],
        "stats": {"hp": 125, "ataque": 170, "defensa": 100, "ataque_especial": 120,
                  "defensa_especial": 90, "velocidad": 95},
        "movimiento": "draco_meteoro", "tipo_mov": "dragon", "cat": "especial",
        "potencia": 130, "peso_meta": 1.2,
    },
]

_ROLL_MED = 0.925  # roll medio para estimaciones rápidas

_BOOSTS_CANDIDATOS = [
    ("timido",   "velocidad",       {"velocidad": 252, "ataque_especial": 252, "hp": 4}),
    ("modesto",  "ataque_especial", {"ataque_especial": 252, "hp": 252, "velocidad": 4}),
    ("audaz",    "ataque",          {"ataque": 252, "velocidad": 252, "hp": 4}),
    ("imprudente","defensa",        {"hp": 252, "defensa": 252, "velocidad": 4}),
    ("calmo",    "defensa_especial",{"hp": 252, "defensa_especial": 252, "velocidad": 4}),
    ("timido",   "velocidad_tank",  {"hp": 248, "velocidad": 252, "defensa_especial": 8}),
]

_OBJETOS_CANDIDATOS = ["orbe_de_vida", "gafas_eleccion", "garra_eleccion",
                        "faja_asalto", "fajin_focus", "resto_sobras", "bayas_sitrus"]


def _stat(base: int, iv: int, ev: int, nivel: int,
          nat_mult: float = 1.0, es_hp: bool = False) -> int:
    if es_hp:
        return math.floor((2 * base + iv + math.floor(ev / 4)) * nivel / 100) + nivel + 10
    return math.floor(
        (math.floor((2 * base + iv + math.floor(ev / 4)) * nivel / 100) + 5) * nat_mult
    )


def _nat_m(nat: str, stat: str) -> float:
    return NATURALEZA_MODIFICADORES.get(nat, {}).get(stat, 1.0)


def _dano(potencia: int, atk: int, df: int, nivel: int,
          efect: float, stab: bool, objeto: str | None) -> int:
    base = math.floor(
        math.floor(math.floor(2 * nivel / 5 + 2) * potencia * atk / df / 50) + 2
    )
    d = math.floor(base * _ROLL_MED)
    if stab:
        d = math.floor(d * 1.5)
    d = math.floor(d * efect)
    if objeto == "orbe_de_vida":
        d = math.floor(d * 1.3)
    return max(1, d)


def _mejor_movset(poke_data: dict, tipos_poke: list[str],
                  atk_stat: int, atkesp_stat: int, nivel: int,
                  objeto: str | None) -> list[str]:
    """Selecciona los 4 movimientos con mayor DPS esperado contra la meta."""
    candidatos: list[tuple[float, str]] = []
    movs_disponibles = poke_data.get("movimientos", list(MOVIMIENTOS_CHAMPIONS.keys())[:20])

    for mov_key in movs_disponibles:
        mov = MOVIMIENTOS_CHAMPIONS.get(mov_key)
        if not mov or mov["categoria"] == "estado" or not mov.get("potencia"):
            continue
        tipo_m = mov["tipo"]
        cat = mov["categoria"]
        potencia = mov["potencia"]
        stab = tipo_m in tipos_poke

        score_total = 0.0
        for amenaza in AMENAZAS_META_CHAMPIONS:
            efect = efectividad_champions(tipo_m, amenaza["tipos"])
            if efect == 0.0:
                continue
            stat_atk = atk_stat if cat == "fisico" else atkesp_stat
            df_amenaza = math.floor(
                (_stat(amenaza["stats"]["defensa"] if cat == "fisico"
                       else amenaza["stats"]["defensa_especial"],
                       31, 4, 50) )
            )
            d = _dano(potencia, stat_atk, max(df_amenaza, 1), nivel, efect, stab, objeto)
            score_total += d * amenaza["peso_meta"]

        candidatos.append((score_total, mov_key))

    candidatos.sort(reverse=True)
    # Siempre incluir un movimiento de estado/setup si disponible
    mov_estado = next(
        (k for k in movs_disponibles
         if MOVIMIENTOS_CHAMPIONS.get(k, {}).get("categoria") == "estado"),
        None,
    )
    top4 = [k for _, k in candidatos[:4]]
    if mov_estado and mov_estado not in top4 and len(top4) == 4:
        top4[3] = mov_estado  # reemplaza el peor ofensivo por el setup
    return top4 if top4 else list(movs_disponibles)[:4]


def _evaluar_build(poke_data: dict, nombre: str, naturaleza: str,
                   evs_config: dict, objeto: str, nivel: int = 100) -> dict:
    tipos = poke_data["tipos"]
    stats_b = poke_data["stats"]
    ivs = {s: 31 for s in ("hp", "ataque", "defensa", "ataque_especial",
                            "defensa_especial", "velocidad")}
    evs = {s: evs_config.get(s, 0) for s in ivs}

    hp_stat  = _stat(stats_b["hp"],  ivs["hp"],  evs["hp"],  nivel, es_hp=True)
    atk_stat = _stat(stats_b["ataque"], ivs["ataque"], evs["ataque"], nivel,
                     _nat_m(naturaleza, "ataque"))
    def_stat = _stat(stats_b["defensa"], ivs["defensa"], evs["defensa"], nivel,
                     _nat_m(naturaleza, "defensa"))
    atkesp   = _stat(stats_b["ataque_especial"], ivs["ataque_especial"],
                     evs["ataque_especial"], nivel,
                     _nat_m(naturaleza, "ataque_especial"))
    defesp   = _stat(stats_b["defensa_especial"], ivs["defensa_especial"],
                     evs["defensa_especial"], nivel,
                     _nat_m(naturaleza, "defensa_especial"))
    vel_stat = _stat(stats_b["velocidad"], ivs["velocidad"], evs["velocidad"], nivel,
                     _nat_m(naturaleza, "velocidad"))

    # Selección de movimientos
    movset = _mejor_movset(poke_data, tipos, atk_stat, atkesp, nivel, objeto)

    # Simular contra amenazas
    victorias = 0
    detalles_amenazas: list[dict] = []
    score_total = 0.0

    for amenaza in AMENAZAS_META_CHAMPIONS:
        # Daño infligido (mejor movimiento disponible)
        mejor_dano = 0
        mejor_mov_usado = ""
        for mov_key in movset:
            mov = MOVIMIENTOS_CHAMPIONS.get(mov_key)
            if not mov or mov["categoria"] == "estado" or not mov.get("potencia"):
                continue
            tipo_m = mov["tipo"]
            cat = mov["categoria"]
            efect = efectividad_champions(tipo_m, amenaza["tipos"])
            if efect == 0.0:
                continue
            stat_atk_uso = atk_stat if cat == "fisico" else atkesp
            df_am = max(1, _stat(
                amenaza["stats"]["defensa"] if cat == "fisico"
                else amenaza["stats"]["defensa_especial"], 31, 4, 50
            ))
            d = _dano(mov["potencia"], stat_atk_uso, df_am, nivel, efect,
                      tipo_m in tipos, objeto)
            if d > mejor_dano:
                mejor_dano = d
                mejor_mov_usado = mov_key

        hp_amenaza = _stat(amenaza["stats"]["hp"], 31, 4, 50, es_hp=True)

        # Daño recibido
        efect_recib = efectividad_champions(amenaza["tipo_mov"], tipos)
        df_recib = def_stat if amenaza["cat"] == "fisico" else defesp
        dano_recib = max(1, _dano(
            amenaza["potencia"], amenaza["stats"]["ataque_especial"]
            if amenaza["cat"] == "especial" else amenaza["stats"]["ataque"],
            max(df_recib, 1), 50, efect_recib, False, None,
        ))

        ko_a = mejor_dano >= hp_amenaza
        ko_recibido = dano_recib >= hp_stat
        gana = ko_a and not ko_recibido
        if gana:
            victorias += 1
        score_total += amenaza["peso_meta"] * (1.5 if ko_a else 0.5) * (
            1.2 if not ko_recibido else 0.8
        )

        detalles_amenazas.append({
            "amenaza": amenaza["nombre"],
            "dano_infligido": mejor_dano,
            "ko_enemigo": ko_a,
            "dano_recibido": dano_recib,
            "ko_recibido": ko_recibido,
            "resultado": "victoria" if gana else "derrota",
            "movimiento_usado": mejor_mov_usado,
        })

    return {
        "naturaleza": naturaleza,
        "evs": evs,
        "objeto": objeto,
        "movimientos": movset,
        "stats_finales": {
            "hp": hp_stat, "ataque": atk_stat, "defensa": def_stat,
            "ataque_especial": atkesp, "defensa_especial": defesp,
            "velocidad": vel_stat,
        },
        "victorias_meta": victorias,
        "total_amenazas": len(AMENAZAS_META_CHAMPIONS),
        "score": round(score_total, 3),
        "detalles_amenazas": detalles_amenazas,
    }


def generar_guia_pokemon_champions(nombre: str) -> dict:
    poke_data = buscar_pokemon_champions(nombre)
    if not poke_data:
        return {"ok": False, "error": f"'{nombre}' no está en el catálogo de Champions."}

    nombre_limpio = nombre.lower().replace(" ", "_")

    mejores: list[dict] = []
    for nat, _, evs_cfg in _BOOSTS_CANDIDATOS:
        for obj in _OBJETOS_CANDIDATOS:
            build = _evaluar_build(poke_data, nombre_limpio, nat, evs_cfg, obj)
            mejores.append(build)

    mejores.sort(key=lambda b: (b["victorias_meta"], b["score"]), reverse=True)
    top3 = mejores[:3]

    return {
        "ok": True,
        "pokemon": poke_data.get("nombre", nombre),
        "tipos": poke_data["tipos"],
        "tier": poke_data.get("tier", "?"),
        "formato": "Singles",
        "generaciones": "I–IX",
        "top_builds": top3,
        "amenazas_evaluadas": len(AMENAZAS_META_CHAMPIONS),
    }


def generar_mejor_equipo_champions(pokemon_ancla: str) -> dict:
    ancla = buscar_pokemon_champions(pokemon_ancla)
    if not ancla:
        return {"ok": False, "error": f"'{pokemon_ancla}' no está en el catálogo de Champions."}

    tipos_ancla = ancla["tipos"]

    # Detectar debilidades del ancla
    debilidades_ancla: list[str] = []
    for t_ataque in ["fuego", "agua", "electrico", "planta", "hielo", "lucha",
                     "veneno", "tierra", "volador", "psiquico", "bicho", "roca",
                     "fantasma", "dragon", "siniestro", "acero", "hada", "normal"]:
        efect = efectividad_champions(t_ataque, tipos_ancla)
        if efect >= 2.0:
            debilidades_ancla.append(t_ataque)

    # Seleccionar compañeros que cubran debilidades
    equipo: list[dict] = [{"nombre": ancla.get("nombre", pokemon_ancla),
                            "tipos": tipos_ancla, "tier": ancla.get("tier", "?")}]
    candidatos_restantes = {
        k: v for k, v in POKEMON_CHAMPIONS.items()
        if k not in (pokemon_ancla.lower(), pokemon_ancla.lower() + "_ch")
    }

    for _ in range(5):
        mejor_candidato = None
        mejor_score = -1.0
        for clave, poke in candidatos_restantes.items():
            if any(m["nombre"] == poke.get("nombre") for m in equipo):
                continue
            score = 0.0
            for deb in debilidades_ancla:
                resil = efectividad_champions(deb, poke["tipos"])
                if resil <= 0.5:
                    score += (1.5 if resil == 0.0 else 1.0)
            tier_bonus = {"S": 0.5, "A": 0.3, "B": 0.1}.get(poke.get("tier", "B"), 0.0)
            score += tier_bonus
            if score > mejor_score:
                mejor_score = score
                mejor_candidato = (clave, poke)

        if mejor_candidato:
            clave, poke = mejor_candidato
            equipo.append({"nombre": poke.get("nombre", clave),
                           "tipos": poke["tipos"], "tier": poke.get("tier", "?")})
            del candidatos_restantes[clave]
            # Actualizar debilidades con las del nuevo miembro
            for t_a in list(debilidades_ancla):
                if efectividad_champions(t_a, poke["tipos"]) <= 0.5:
                    debilidades_ancla.remove(t_a)

    return {
        "ok": True,
        "formato": "Singles Champions",
        "ancla": ancla.get("nombre", pokemon_ancla),
        "equipo": equipo,
        "cobertura": f"{len(equipo)} Pokémon",
    }
