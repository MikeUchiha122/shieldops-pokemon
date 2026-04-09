# 🛡️ ShieldOps Pokémon — Sistema Completo 2026

**VGC 2026 · LZA Battle Club S7 · GO Battle League S26**  
Un solo archivo HTML · Gemini 2.5 Flash · Sin instalación

---

## Inicio rápido — 3 pasos

1. Descomprime **ShieldOps-Completo.zip**
2. Abre **`ShieldOps/index.html`** en Chrome o Edge
3. Pega tu API key en el recuadro amarillo → **Guardar**

API key gratuita (sin tarjeta): **aistudio.google.com/apikey**

> El backend Python (`python-v3/` y `python-go/`) es **completamente opcional**.
> `shieldops.html` funciona al 100% sin instalar nada más.

---

## Contenido

Un solo archivo con dos modos. La barra superior los cambia:

### ⚡ ShieldOps v3 — EyP VGC 2026 + LZA Battle Club S7

| Panel | Descripción |
|---|---|
| ⚡ EyP — VGC 2026 | 7 arquetipos, flujo 3 pasos, export Showdown (.txt / PDF) |
| ✦ LZA — Battle Club S7 | 7 arquetipos, 3 Pokémon/equipo, 1 Mega/batalla, 20 Pokémon |
| 💥 Motor de Daño | Gen IX, 16 rolls, EVs/boosts, Tera/Mega |
| 📋 Guía Entrenamiento | ✨ Automático + ⚙️ Experto, 8 192 tokens |
| 🤖 Agente Meta Live | IA campeón mundial + Google Search en tiempo real |
| 🔍 Hack-Check | EVs, movimientos baneados, habilidades ilegales |
| ⚡ Speed Tiers | Velocidades Nivel 50 con todos los modificadores |
| 🗺️ Tabla de Tipos | Interactiva — EyP / LZA / GO con multiplicadores correctos |

### 🎮 ShieldOps GO — GO Battle League Season 26

| Panel | Descripción |
|---|---|
| 🏆 Equipos PvP | 9 equipos meta S26 (Great / Ultra / Master × 3 estilos) |
| 💥 Calculadora | Fórmula GO con CPM, STAB ×1.2, ×1.6 super eficaz |
| 📋 Guía IVs | IA: IVs óptimos, Candies, Polvo Estelar, moveset |
| 🤖 Agente Meta | Campeón GBL + Google Search, Season 26 |
| 🔍 Validar IVs | CP, IVs 0-15, estrategia por liga con barras visuales |

---

## El Agente IA

El agente incorpora el conocimiento de los mejores jugadores del mundo:

**Para EyP/LZA:** Wolfe Glick (campeón VGC), Sejun Park, top Regionales 2026.  
Cita: Pikalytics, Smogon VGC, Game8, Dexerto, resultados Battle Club S7.

**Para GO:** Top players de PvPoke, Silph Arena, GO Hub, Season 26.

El agente conoce y diferencia las mecánicas de cada juego:

| Mecánica | EyP / LZA | Pokémon GO |
|---|---|---|
| STAB | ×1.5 | ×1.2 |
| Super eficaz | ×2.0 | ×1.6 |
| Poco eficaz | ×0.5 | ×0.625 |
| "Inmune" | ×0 | ×0.391 (¡no es 0!) |
| IVs | 0–31 | 0–15 |
| IVs Ataque óptimos | siempre altos | **bajos en GL/UL** |
| Equipo | 6 Pokémon | 3 Pokémon |
| Nivel | 50 fijo | 1–51 con CPM |

---

## Movimientos en 3 idiomas

Los movimientos se muestran como **Inglés · España · Latinoamérica** cuando difieren.

| Inglés | España | Latinoamérica |
|---|---|---|
| Draco Meteor | Cometa Draco | Meteoro Dragón |
| Flash Cannon | Foco Resplandor | Cañón Destello |
| Fake Out | Finta | Ataque Finta |
| Flare Blitz | Nitrocarga | Carga de Fuego |
| Trick Room | Cambio de Sala | Sala Cambiada |
| Tailwind | Viento Afín | Viento Aliado |

> LZA es el primer juego de la serie principal con traducción oficial al español latinoamericano.

---

## Despliegue en GitHub Pages

```bash
# 1. Renombrar a index.html
mv shieldops.html index.html   # Mac/Linux
# Windows: Rename-Item shieldops.html index.html

# 2. Subir a GitHub
git init
git add index.html README.md
git commit -m "feat: ShieldOps Pokémon v1.0"
git branch -M main
git remote add origin https://github.com/MikeUchiha122/shieldops-pokemon.git
git push -u origin main

# 3. Activar GitHub Pages
# Settings → Pages → Branch: main / Folder: / (root) → Save
# URL: https://MikeUchiha122.github.io/shieldops-pokemon/
```

---

## Backend Python (opcional)

```bash
# EyP + LZA
cd python-v3
pip install -r requirements.txt    # Kali: --break-system-packages
pip install pytest-cov
cp .env.example .env               # GEMINI_API_KEY=tu_key
python -m pytest tests/unit/ -v    # 11 passed, 89.76%

# GO Battle League  
cd python-go
pip install -r requirements.txt
python -m pytest tests/unit/ -v --no-cov    # 17 passed
```

---

## API Gemini — gratis

| Modelo | Req/día | Notas |
|---|---|---|
| `gemini-2.5-flash` | 250 | Default |
| `gemini-2.5-flash-lite-preview-06-17` | 1 000 | Si llegas al límite |
| `gemini-2.5-pro` | 100 | Análisis profundos |

Cada modo (v3 y GO) guarda su API key por separado en el navegador.

---

*"El mejor set es el que el rival no puede predecir."*  
**MikeUchiha122** · [github.com/MikeUchiha122](https://github.com/MikeUchiha122) · Abril 2026
