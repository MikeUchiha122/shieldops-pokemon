"""
cerebros/champions/data/habilidades.py
Catalogo de Habilidades disponibles en Pokemon Champions.

Fuente: op.gg/es/pokemon-champions/abilities (abril 2026).
Total aproximado en el juego: ~307 habilidades. Este catalogo incluye las
mas relevantes competitivamente + las referenciadas en pokemon.py.

Formato: clave → {nombre, descripcion}
"""
from __future__ import annotations

HABILIDADES_CHAMPIONS: dict[str, dict] = {
    # ── A ────────────────────────────────────────────────────────────────────
    "abalorio_debacle":    {"nombre": "Abalorio Debacle",    "descripcion": "Baja la Def. Especial de todos los demas Pokemon."},
    "absorbe_agua":        {"nombre": "Absorbe Agua",        "descripcion": "Recupera PS al recibir ataques de tipo Agua."},
    "absorbe_elec":        {"nombre": "Absorbe Elec",        "descripcion": "Recupera PS al recibir ataques de tipo Electrico."},
    "absorbe_fuego":       {"nombre": "Absorbe Fuego",       "descripcion": "Potencia movimientos de Fuego si ha sufrido alguno antes."},
    "acero_templado":      {"nombre": "Acero Templado",      "descripcion": "Potencia los movimientos de tipo Acero."},
    "acerrimo":            {"nombre": "Acerrimo",            "descripcion": "Impide que el rival atraiga ataques hacia si mismo."},
    "aclimatacion":        {"nombre": "Aclimatacion",        "descripcion": "Anula los efectos del tiempo atmosferico."},
    "adaptable":           {"nombre": "Adaptable",           "descripcion": "Potencia los movimientos del mismo tipo del Pokemon (STAB x2)."},
    "afortunado":          {"nombre": "Afortunado",          "descripcion": "Aumenta la probabilidad de dar golpes criticos."},
    "agallas":             {"nombre": "Agallas",             "descripcion": "Sube el Ataque si sufre un problema de estado."},
    "agrupamiento":        {"nombre": "Agrupamiento",        "descripcion": "Adopta su Forma Completa cuando PS se reducen a la mitad."},
    "alas_vendaval":       {"nombre": "Alas Vendaval",       "descripcion": "Da prioridad a los movimientos de tipo Volador."},
    "alerta":              {"nombre": "Alerta",              "descripcion": "Determina el movimiento mas potente del rival."},
    "allanamiento":        {"nombre": "Allanamiento",        "descripcion": "Ataca rodeando la barrera del rival."},
    "alma_acerada":        {"nombre": "Alma Acerada",        "descripcion": "Potencia los movimientos de tipo Acero de los aliados."},
    "alma_cura":           {"nombre": "Alma Cura",           "descripcion": "A veces cura los cambios de estado de un aliado."},
    "alma_errante":        {"nombre": "Alma Errante",        "descripcion": "Intercambia su habilidad con la del agresor al recibir contacto."},
    "amor_filial":         {"nombre": "Amor Filial",         "descripcion": "Ataca en familia (segundo golpe reducido)."},
    "antibalas":           {"nombre": "Antibalas",           "descripcion": "No le afectan las bombas ni algunos proyectiles."},
    "antibarrera":         {"nombre": "Antibarrera",         "descripcion": "Anula Pantalla de Luz, Reflejo y Velo Aurora."},
    "anticipacion":        {"nombre": "Anticipacion",        "descripcion": "Preve los movimientos peligrosos del rival."},
    "antidoto":            {"nombre": "Antidoto",            "descripcion": "Recupera PS si el Pokemon ha sido envenenado."},
    "armadura_batalla":    {"nombre": "Armadura Batalla",    "descripcion": "Bloquea golpes criticos."},
    "armadura_fragil":     {"nombre": "Armadura Fragil",     "descripcion": "Un ataque fisico baja la Defensa y sube la Velocidad."},
    "armadura_prisma":     {"nombre": "Armadura Prisma",     "descripcion": "Mitiga el dano de movimientos supereficaces."},
    "audaz":               {"nombre": "Audaz",               "descripcion": "Potencia los movimientos que danan al usuario."},
    "aura_feerica":        {"nombre": "Aura Feerica",        "descripcion": "Aumenta la potencia de todos los movimientos de tipo Hada."},
    "aura_oscura":         {"nombre": "Aura Oscura",         "descripcion": "Aumenta la potencia de todos los movimientos de tipo Siniestro."},
    "ausente":             {"nombre": "Ausente",             "descripcion": "El Pokemon no atacara en turnos consecutivos."},
    "autoestima":          {"nombre": "Autoestima",          "descripcion": "Potencia el Ataque al debilitar a un objetivo."},
    # ── B ────────────────────────────────────────────────────────────────────
    "baba":                {"nombre": "Baba",                "descripcion": "Baja la Velocidad del Pokemon con el que entra en contacto."},
    "baba_venenosa":       {"nombre": "Baba Venenosa",       "descripcion": "Puede envenenar al Pokemon que entra en contacto fisico."},
    "banco":               {"nombre": "Banco",               "descripcion": "Forma bancos con sus congeneres, otorgandole mas fuerza."},
    "bateria":             {"nombre": "Bateria",             "descripcion": "Potencia los movimientos especiales de los aliados."},
    "bayoneta":            {"nombre": "Bayoneta",            "descripcion": "Puede envenenar al rival que entre en contacto."},
    "bondad":              {"nombre": "Bondad",              "descripcion": "Potencia movimientos de tipo Normal que afectan a aliados."},
    "bromista":            {"nombre": "Bromista",            "descripcion": "Permite lanzar ataques de estado en primer lugar."},
    "bucle_aire":          {"nombre": "Bucle Aire",          "descripcion": "Anula los efectos del tiempo atmosferico."},
    # ── C ────────────────────────────────────────────────────────────────────
    "cabeza_roca":         {"nombre": "Cabeza Roca",         "descripcion": "Impide que el Pokemon se dane con sus movimientos de retroceso."},
    "cacheo":              {"nombre": "Cacheo",              "descripcion": "Permite ver el objeto que lleva el rival."},
    "cadena_toxica":       {"nombre": "Cadena Toxica",       "descripcion": "30 % de envenenar gravemente al atacar."},
    "calculo_final":       {"nombre": "Calculo Final",       "descripcion": "Potencia el movimiento si es el ultimo en atacar."},
    "caldero_debacle":     {"nombre": "Caldero Debacle",     "descripcion": "Baja el At. Especial de todos los demas Pokemon."},
    "cambio_color":        {"nombre": "Cambio Color",        "descripcion": "Adopta el tipo del ultimo movimiento recibido."},
    "cambio_heroico":      {"nombre": "Cambio Heroico",      "descripcion": "Se transforma a Forma Heroe al volver al campo."},
    "cambio_tactico":      {"nombre": "Cambio Tactico",      "descripcion": "Cambia de forma segun su estilo de combate."},
    "caparazon":           {"nombre": "Caparazon",           "descripcion": "Bloquea los golpes criticos."},
    "cara_de_hielo":       {"nombre": "Cara de Hielo",       "descripcion": "Absorbe dano con hielo, cambiando de forma."},
    "carga_cuark":         {"nombre": "Carga Cuark",         "descripcion": "Potencia la estadistica mas alta en Campo Electrico o con Booster Energia."},
    "carnal":              {"nombre": "Carnal",              "descripcion": "Inflige mas dano a Pokemon con mayor peso."},
    "carrillo":            {"nombre": "Carrillo",            "descripcion": "Recupera PS al comer bayas."},
    "cero_a_heroe":        {"nombre": "Cero a Heroe",        "descripcion": "Al volver al combate cambia a Forma Heroe (Palafin)."},
    "chorro_arena":        {"nombre": "Chorro Arena",        "descripcion": "Crea una tormenta de arena al entrar en combate."},
    "cielo_despejado":     {"nombre": "Cielo Despejado",     "descripcion": "Anula las condiciones climaticas."},
    "clorofila":           {"nombre": "Clorofila",           "descripcion": "Sube la Velocidad cuando hay sol."},
    "cobardia":            {"nombre": "Cobardia",            "descripcion": "El miedo a algunos ataques sube su Velocidad."},
    "cosecha":             {"nombre": "Cosecha",             "descripcion": "A veces recupera la baya consumida al final del turno."},
    "cosecha_limite":      {"nombre": "Cosecha Limite",      "descripcion": "Reduce el dano recibido al maximo de HP."},
    "cuenco_de_ruina":     {"nombre": "Cuenco de Ruina",     "descripcion": "Baja el At. Especial de los demas Pokemon (Chi-Yu)."},
    "cuerpo_magico":       {"nombre": "Cuerpo Magico",       "descripcion": "Impide movimientos de estado enemigos."},
    "cuerpo_marino":       {"nombre": "Cuerpo Marino",       "descripcion": "Impide cambios de estadisticas salvo propios."},
    "cuerpo_puro":         {"nombre": "Cuerpo Puro",         "descripcion": "Impide cambios de estadisticas provocados por el rival."},
    "cuerpo_roca":         {"nombre": "Cuerpo Roca",         "descripcion": "Reduce al 50 % el dano de movimientos fisicos."},
    "cuerpo_rudo":         {"nombre": "Cuerpo Rudo",         "descripcion": "Dana a los rivales que usan ataques de contacto."},
    "cuerpo_solido":       {"nombre": "Cuerpo Solido",       "descripcion": "No cede a los movimientos de empuje."},
    "cuerpo_viscoso":      {"nombre": "Cuerpo Viscoso",      "descripcion": "Ralentiza al rival que entra en contacto."},
    "cursor":              {"nombre": "Cursor",              "descripcion": "Permite impactar aunque el rival use proteccion."},
    # ── D ────────────────────────────────────────────────────────────────────
    "defensa_hoja":        {"nombre": "Defensa Hoja",        "descripcion": "Elimina problemas de estado bajo el sol intenso."},
    "descarga":            {"nombre": "Descarga",            "descripcion": "Puede paralizar al rival en contacto."},
    "despiste":            {"nombre": "Despiste",            "descripcion": "Dobla la probabilidad de fallar movimientos del rival al 50 %."},
    "detonacion":          {"nombre": "Detonacion",          "descripcion": "Aumenta la potencia de movimientos de fuego al bajar PS."},
    "dicha":               {"nombre": "Dicha",               "descripcion": "Inmune a movimientos de tipo Hada."},
    "dinamo":              {"nombre": "Dinamo",              "descripcion": "Golpes criticos no bajan el atq del portador."},
    "disfraz":             {"nombre": "Disfraz",             "descripcion": "Una vez por combate ignora un ataque (Mimikyu)."},
    "don_floral":          {"nombre": "Don Floral",          "descripcion": "Potencia Ataque y Def. Especial bajo sol intenso."},
    "dragonize":           {"nombre": "Dragonize",           "descripcion": "Los movimientos Normales pasan a ser de tipo Dragon."},
    # ── E ────────────────────────────────────────────────────────────────────
    "efecto_espora":       {"nombre": "Efecto Espora",       "descripcion": "Puede dormir/paralizar/envenenar al rival en contacto."},
    "elec_estatica":       {"nombre": "Electricidad Estatica","descripcion": "30 % de paralizar al rival al contacto."},
    "electrogenesis":      {"nombre": "Electrogenesis",      "descripcion": "Sube el At. Especial al entrar en combate."},
    "electromotor":        {"nombre": "Electromotor",        "descripcion": "Sube la Velocidad al recibir un ataque Electrico."},
    "electromorfosis":     {"nombre": "Electromorfosis",     "descripcion": "Potencia el proximo ataque Electrico al recibir dano."},
    "encadenado":          {"nombre": "Encadenado",          "descripcion": "Impide al rival intercambiar o huir."},
    "energia_dragon":      {"nombre": "Energia Dragon",      "descripcion": "Potencia movimientos Dragon segun PS restantes (Regidrago)."},
    "energia_eolica":      {"nombre": "Energia Eolica",      "descripcion": "Potencia el At. Especial al recibir un movimiento volador."},
    "energia_pura":        {"nombre": "Energia Pura",        "descripcion": "Multiplica el Ataque x2."},
    "energia_rabiosa":     {"nombre": "Energia Rabiosa",     "descripcion": "Potencia el At. si recibe golpe critico."},
    "enjambre":            {"nombre": "Enjambre",            "descripcion": "Potencia movimientos de tipo Bicho con PS bajos."},
    "enorme_poder":        {"nombre": "Enorme Poder",        "descripcion": "Multiplica el Ataque x2."},
    "ensanamiento":        {"nombre": "Ensanamiento",        "descripcion": "Potencia el Ataque al debilitar a un rival."},
    "entusiasmo":          {"nombre": "Entusiasmo",          "descripcion": "Sube el At. fisico a costa de precision."},
    "escama_especial":     {"nombre": "Escama Especial",     "descripcion": "Sube la Def. Especial si tiene un problema de estado."},
    "escudo_magma":        {"nombre": "Escudo Magma",        "descripcion": "Impide quemaduras al portador."},
    "escudo_recio":        {"nombre": "Escudo Recio",        "descripcion": "Reduce el dano recibido si esta con los PS al maximo."},
    "espada_de_ruina":     {"nombre": "Espada de Ruina",     "descripcion": "Baja el At. fisico de los demas Pokemon (Chien-Pao)."},
    "espejo_magico":       {"nombre": "Espejo Magico",       "descripcion": "Devuelve los movimientos de estado al rival."},
    "espesura":            {"nombre": "Espesura",            "descripcion": "Potencia movimientos de tipo Planta con PS bajos."},
    "espiritu_vital":      {"nombre": "Espiritu Vital",      "descripcion": "Impide que el Pokemon se duerma."},
    "estatica":            {"nombre": "Estatica",            "descripcion": "30 % de paralizar al rival al contacto."},
    # ── F ────────────────────────────────────────────────────────────────────
    "filtro":              {"nombre": "Filtro",              "descripcion": "Reduce el dano de ataques supereficaces."},
    "firmeza":             {"nombre": "Firmeza",             "descripcion": "No le afectan los golpes de retiro."},
    "flaqueza":            {"nombre": "Flaqueza",            "descripcion": "Reduce las estadisticas al entrar con un problema de estado."},
    "foco_interno":        {"nombre": "Foco Interno",        "descripcion": "Impide que el Pokemon se acobarde."},
    "francotirador":       {"nombre": "Francotirador",       "descripcion": "Potencia los golpes criticos."},
    "fuerte_afecto":       {"nombre": "Fuerte Afecto",       "descripcion": "Potencia los movimientos de tipo Hada."},
    "fuerza_bruta":        {"nombre": "Fuerza Bruta",        "descripcion": "Ignora efectos de objetos del rival (como bayas)."},
    # ── G ────────────────────────────────────────────────────────────────────
    "garra_dura":          {"nombre": "Garra Dura",          "descripcion": "Potencia los movimientos de contacto."},
    "gelido":              {"nombre": "Gelido",              "descripcion": "Puede congelar al rival en contacto."},
    "general_supremo":     {"nombre": "General Supremo",     "descripcion": "Potencia Ataque y Velocidad al entrar tras caer un aliado."},
    "gran_encanto":        {"nombre": "Gran Encanto",        "descripcion": "Potencia movimientos del mismo genero rival."},
    "guts":                {"nombre": "Agallas (Guts)",      "descripcion": "Sube el Ataque si sufre un problema de estado."},
    # ── H ────────────────────────────────────────────────────────────────────
    "hambre_muda":         {"nombre": "Hambre Muda",         "descripcion": "Cambia entre Modo Lleno/Voraz al usar un movimiento."},
    "hidratacion":         {"nombre": "Hidratacion",         "descripcion": "Cura problemas de estado bajo lluvia."},
    "hipertorque":         {"nombre": "Hipertorque",         "descripcion": "Impide que los movimientos sean modificados por ataques multiples."},
    "holgazaneria":        {"nombre": "Holgazaneria",        "descripcion": "Solo puede atacar un turno de cada dos."},
    "humo_blanco":         {"nombre": "Humo Blanco",         "descripcion": "Impide que le bajen las estadisticas."},
    # ── I ────────────────────────────────────────────────────────────────────
    "iluminacion":         {"nombre": "Iluminacion",         "descripcion": "Aumenta la probabilidad de encuentros con Pokemon salvajes."},
    "ilusion":             {"nombre": "Ilusion",             "descripcion": "Entra disfrazado del ultimo Pokemon del equipo (Zoroark)."},
    "iman":                {"nombre": "Iman",                "descripcion": "Impide que los Pokemon de tipo Acero abandonen el combate."},
    "impasible":           {"nombre": "Impasible",           "descripcion": "Aumenta el At. Especial al recibir un golpe critico."},
    "impostor":            {"nombre": "Impostor",            "descripcion": "Se transforma en el rival al entrar (Ditto)."},
    "infiltrador":         {"nombre": "Infiltrador",         "descripcion": "Atraviesa barreras y subtitutos."},
    "insomnio":            {"nombre": "Insomnio",            "descripcion": "Impide que el Pokemon se duerma."},
    "intimidacion":        {"nombre": "Intimidacion",        "descripcion": "Baja el Ataque del rival al entrar."},
    # ── L ────────────────────────────────────────────────────────────────────
    "levitacion":          {"nombre": "Levitacion",          "descripcion": "Inmune a ataques de tipo Tierra."},
    "libero":              {"nombre": "Libero",              "descripcion": "Cambia al tipo del movimiento que usa (Cinderace)."},
    "ligereza":            {"nombre": "Ligereza",            "descripcion": "Dobla la Velocidad al llevar algunos objetos."},
    "llovizna":            {"nombre": "Llovizna",            "descripcion": "Invoca lluvia al entrar en combate."},
    # ── M ────────────────────────────────────────────────────────────────────
    "mandibula_dragon":    {"nombre": "Mandibula Dragon",    "descripcion": "Potencia movimientos de tipo Dragon tipo mordisco."},
    "mandibula_fuerte":    {"nombre": "Mandibula Fuerte",    "descripcion": "Potencia los movimientos tipo mordisco."},
    "mano_rapida":         {"nombre": "Mano Rapida",         "descripcion": "A veces permite atacar primero."},
    "manto_frondoso":      {"nombre": "Manto Frondoso",      "descripcion": "Bajo sol intenso, reduce dano especial recibido."},
    "manto_llama":         {"nombre": "Manto Llama",         "descripcion": "Reduce el dano de movimientos especiales a la mitad."},
    "manto_niveo":         {"nombre": "Manto Niveo",         "descripcion": "Aumenta la Def. en tormenta de nieve."},
    "mar_llamas":          {"nombre": "Mar Llamas",          "descripcion": "Potencia movimientos Fuego con PS bajos."},
    "mente_fuerte":        {"nombre": "Mente Fuerte",        "descripcion": "Inmune al intimidamiento y algunos estados."},
    "motor_cuantico":      {"nombre": "Motor Cuantico",      "descripcion": "Potencia la stat mas alta en Campo Electrico (Paradojas)."},
    "mucosidad":           {"nombre": "Mucosidad",           "descripcion": "Reduce el dano especial recibido a la mitad."},
    "multiescama":         {"nombre": "Multiescama",         "descripcion": "Reduce a la mitad el dano recibido si esta con PS al maximo."},
    # ── N ────────────────────────────────────────────────────────────────────
    "nevada":              {"nombre": "Nevada",              "descripcion": "Invoca tormenta de nieve al entrar."},
    "nevera":              {"nombre": "Nevera",              "descripcion": "Movimientos Normales pasan a ser tipo Hielo."},
    "nado_rapido":         {"nombre": "Nado Rapido",         "descripcion": "Dobla la Velocidad bajo lluvia."},
    # ── O ────────────────────────────────────────────────────────────────────
    "oido_fino":           {"nombre": "Oido Fino",           "descripcion": "Impide ser confundido."},
    # ── P ────────────────────────────────────────────────────────────────────
    "pies_rapidos":        {"nombre": "Pies Rapidos",        "descripcion": "Aumenta la Velocidad si sufre un problema de estado."},
    "piel_arenosa":        {"nombre": "Piel Arenosa",        "descripcion": "Recupera 1/16 PS por turno en tormenta de arena."},
    "piel_dura":           {"nombre": "Piel Dura",           "descripcion": "Impide golpes criticos."},
    "piel_tosca":          {"nombre": "Piel Tosca",          "descripcion": "Dana al rival con movimientos de contacto."},
    "presion":             {"nombre": "Presion",             "descripcion": "Consume 2 PP por movimiento recibido."},
    "propulsion_cuantica": {"nombre": "Propulsion Cuantica", "descripcion": "Potencia la stat mas alta en Campo Electrico (Iron)."},
    "protosintesis":       {"nombre": "Protosintesis",       "descripcion": "Potencia la stat mas alta bajo sol intenso (Paradojas)."},
    "puno_experto":        {"nombre": "Puno Experto",        "descripcion": "Potencia movimientos de tipo Lucha un 30 %."},
    "puno_fantasma":       {"nombre": "Puno Fantasma",       "descripcion": "Movimientos de contacto pasan a ser tipo Fantasma (Urshifu)."},
    # ── R ────────────────────────────────────────────────────────────────────
    "regeneracion":        {"nombre": "Regeneracion",        "descripcion": "Recupera 1/3 de sus PS al cambiar."},
    "rompemoldes":         {"nombre": "Rompemoldes",         "descripcion": "Ignora las habilidades del rival al atacar."},
    # ── S ────────────────────────────────────────────────────────────────────
    "sand_veil":           {"nombre": "Velo Arena",          "descripcion": "Aumenta la evasion en tormenta de arena."},
    "sereno_gracia":       {"nombre": "Sereno Gracia",       "descripcion": "Dobla la probabilidad de efectos adicionales."},
    "sincronia":           {"nombre": "Sincronia",           "descripcion": "Copia el problema de estado al rival."},
    "suerte":              {"nombre": "Suerte",              "descripcion": "Aumenta la probabilidad de golpes criticos."},
    # ── T ────────────────────────────────────────────────────────────────────
    "tableta_de_ruina":    {"nombre": "Tableta de Ruina",    "descripcion": "Baja la Def. fisica de los demas Pokemon (Wo-Chien)."},
    "terravoltage":        {"nombre": "Terravoltaje",        "descripcion": "Ignora la habilidad del defensor (Kyurem-Blanco)."},
    "torque_tecnologico":  {"nombre": "Torque Tecnologico",  "descripcion": "Potencia movimientos de baja potencia."},
    "torrente":            {"nombre": "Torrente",            "descripcion": "Potencia movimientos Agua con PS bajos."},
    "transparen":          {"nombre": "Transparen",          "descripcion": "Inmune a movimientos que afectan al equipo."},
    "trastorno":           {"nombre": "Trastorno",           "descripcion": "Anula efectos de bayas del rival."},
    "turboblaze":          {"nombre": "Turboblaze",          "descripcion": "Ignora la habilidad del defensor (Kyurem-Negro)."},
    # ── V ────────────────────────────────────────────────────────────────────
    "vasija_de_ruina":     {"nombre": "Vasija de Ruina",     "descripcion": "Baja la Def. Especial de los demas Pokemon (Ting-Lu)."},
    "vista_lince":         {"nombre": "Vista Lince",         "descripcion": "Impide que baje su precision."},
    "volcan":              {"nombre": "Volcan",              "descripcion": "Inmune a movimientos de tipo Fuego (Heatran)."},
    # ── Z ────────────────────────────────────────────────────────────────────
    "zona_de_hierba":      {"nombre": "Zona de Hierba",      "descripcion": "Invoca Campo de Hierba al entrar (Rillaboom)."},
}


def buscar_habilidad_champions(nombre: str) -> dict | None:
    """Busca habilidad por clave o nombre exacto (case-insensitive)."""
    key = nombre.lower().replace(" ", "_").replace("-", "_")
    if key in HABILIDADES_CHAMPIONS:
        return HABILIDADES_CHAMPIONS[key]
    for v in HABILIDADES_CHAMPIONS.values():
        if v["nombre"].lower() == nombre.lower():
            return v
    return None


def listar_habilidades_champions() -> list[str]:
    return [v["nombre"] for v in HABILIDADES_CHAMPIONS.values()]
