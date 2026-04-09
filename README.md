# ShieldOps Pokémon — Proyecto Completo 2026

> VGC 2026 · LZA Battle Club S7 · GO Battle League S26

## Estructura

```
ShieldOps-Proyecto/
├── frontend/
│   ├── index.html          ← Abrir esto en Chrome/Edge (216KB, todo incluido)
│   └── README.md           ← Guía de uso del frontend
└── backend/
    ├── main.py             ← FastAPI app — 3 cerebros
    ├── requirements.txt
    ├── requirements-dev.txt
    ├── DEPLOY.md           ← Guía de deploy paso a paso
    ├── core/
    │   └── types.py        ← Tabla efectividad, tipos compartidos
    ├── cerebros/
    │   ├── eyp/            ← Cerebro A: EyP VGC 2026
    │   ├── lza/            ← Cerebro B: LZA Action PvP
    │   └── go/             ← Cerebro C: Pokémon GO
    └── tests/
        ├── unit/           ← 54 tests unitarios
        └── integration/    ← 15 tests de integración
```

## Inicio rápido

### Frontend (ya desplegado en GitHub Pages)
```bash
# Está en: https://MikeUchiha122.github.io/shieldops-pokemon/
# Para actualizar localmente:
open frontend/index.html   # Mac
start frontend/index.html  # Windows
```

### Backend (local)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Mac/Linux
# .venv\Scripts\activate           # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Tests — deben dar 69 passed, 0 failed
python -m pytest tests/ -v

# Servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# API docs: http://localhost:8000/docs
```

## Tests

| Suite | Tests | Cobertura |
|---|---|---|
| unit/test_eyp.py | 19 | Stats Gen IX, STAB, Tera, 16 rolls |
| unit/test_lza.py | 16 | Startup frames, cooldowns, Mega |
| unit/test_go.py | 19 | CP, efectividad x1.6/x0.391 |
| integration/test_api.py | 15 | Endpoints, aislamiento cerebros |
| **TOTAL** | **69** | **0 fallos** |

## Tecnologías

- **Frontend**: HTML/CSS/JS vanilla · Gemini 2.5 Flash · GitHub Pages
- **Backend**: FastAPI · Pydantic v2 · Uvicorn · Python 3.12+
- **Deploy**: GitHub Pages (frontend) · Railway (backend)
