# 🎮 ShieldOps Pokémon GO

**Sistema competitivo GO Battle League — Season 26 (Mar–Jun 2026)**  
Python 3.12+ · Great / Ultra / Master League · Gemini 2.5 Flash

---

## ¿Qué incluye?

| Módulo | Descripción |
|---|---|
| **Motor de daño** | Fórmula oficial GO con CPM, STAB ×1.2, efectividad ×1.6/×0.625, Shadow bonus |
| **Calculadora de IVs** | Evalúa si los IVs son óptimos por liga (IVs bajos de Ataque en GL/UL) |
| **Generador de equipos** | Meta S26: Great, Ultra y Master · 3 estilos: Agresivo, Balanceado, Budget |
| **Hack-Check** | Valida CP, IVs (0–15), moves, Elite TMs y Shadow bonus |
| **CLI** | `team`, `damage`, `iv-check`, `hack-check` con Rich UI |
| **Demo HTML** | `shieldops_go_demo.html` — todos los módulos con IA (Gemini) |

---

## Diferencias clave vs VGC

| | VGC (EyP/LZA) | Pokémon GO |
|---|---|---|
| IVs | 0–31 | **0–15** |
| STAB | ×1.5 | **×1.2** |
| Super eficaz | ×2.0 | **×1.6** |
| Poco eficaz | ×0.5 | **×0.625** |
| IVs altos | siempre mejor | **IVs Atk bajos = más bulk** en GL/UL |
| Equipo | 6 Pokémon | **3 Pokémon** |
| Niveles | 50 fijo | **1–51, CPM por nivel** |

---

## Instalación rápida

```bash
pip install -r requirements.txt
# Kali Linux: añadir --break-system-packages
pip install pytest-cov
python -m pytest tests/unit/ -v
# Esperado: 16 passed, coverage 85%+
```

---

## Comandos CLI

```bash
# Generar equipo meta
python main.py team great balanced
python main.py team ultra aggro
python main.py team master budget

# Calcular daño
python main.py damage data/raw/giratina_a.json data/raw/galarian_stunfisk.json "Shadow Ball"

# Evaluar IVs
python main.py iv-check data/raw/galarian_stunfisk.json great

# Hack-Check
python main.py hack-check data/raw/giratina_a.json ultra
```

---

## Meta Season 26 (datos reales)

**Great League (≤1500 CP):** Malamar · Empoleon · Forretress · Galarian Stunfisk · Obstagoon · Swampert  
**Ultra League (≤2500 CP):** Giratina-A · Walrein · Cresselia · Florges · Galarian Moltres · Regidrago  
**Master League:** Zacian-C · Origin Palkia · Zekrom · Lunala · Reshiram · Metagross

---

*Autor: MikeUchiha122 · github.com/MikeUchiha122 · Abril 2026*
