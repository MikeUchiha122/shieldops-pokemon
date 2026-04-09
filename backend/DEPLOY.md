# ShieldOps Backend — Guía de Despliegue

## Estructura del proyecto

```
shieldops_backend/
├── main.py                          # FastAPI app — monta los 3 routers
├── requirements.txt                 # Producción
├── requirements-dev.txt             # Tests y desarrollo
├── core/
│   └── types.py                     # Tipos compartidos (tabla efectividad, APIResponse)
├── cerebros/
│   ├── eyp/                         # Cerebro A: Escarlata/Púrpura VGC
│   │   ├── models/schemas.py        # Pydantic: PokemonEyP, EVsEyP, IVsEyP...
│   │   ├── engine/damage.py         # Motor daño Gen IX (16 rolls, Tera, STAB)
│   │   └── api/router.py            # FastAPI: /eyp/dano, /eyp/validar-equipo
│   ├── lza/                         # Cerebro B: Leyendas Z-A Action PvP
│   │   ├── models/schemas.py        # Pydantic: PokemonLZA, startup_frames, cooldowns
│   │   ├── engine/damage.py         # Motor Action Time (sin habilidades, esquive)
│   │   └── api/router.py            # FastAPI: /lza/dano, /lza/validar-combate
│   └── go/                          # Cerebro C: Pokémon GO
│       ├── models/schemas.py        # Pydantic: PokemonGO, IVs 0-15, CPM
│       ├── engine/damage.py         # Motor GO (STAB x1.2, inmune x0.391, CP)
│       └── api/router.py            # FastAPI: /go/dano, /go/cp, /go/validar-equipo
└── tests/
    ├── unit/                        # 54 tests unitarios
    └── integration/                 # 15 tests de integración API
```

---

## Despliegue seguro en el repositorio existente

### Paso 1 — Crear rama aislada (nunca directo a main)

```bash
git checkout main
git pull origin main
git checkout -b feat/backend-3-cerebros
```

### Paso 2 — Copiar el backend al repositorio

```bash
# Desde el directorio raíz de tu repo (donde está shieldops.html)
cp -r shieldops_backend/ .

# Verificar estructura
ls shieldops_backend/
```

### Paso 3 — Entorno virtual (Windows PowerShell)

```powershell
cd shieldops_backend

# Crear entorno virtual
python -m venv .venv

# Activar
.venv\Scripts\activate

# Instalar dependencias de producción
pip install -r requirements.txt

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

### Paso 3 — Entorno virtual (Mac / Linux / Kali)

```bash
cd shieldops_backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Paso 4 — Ejecutar todos los tests antes de subir

```bash
python -m pytest tests/ -v --tb=short
# Resultado esperado: 69 passed, 0 failed
```

### Paso 5 — Levantar el servidor localmente

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Verifica en el navegador:
- http://localhost:8000/docs          → Swagger UI con los 3 cerebros
- http://localhost:8000/api/v1/health → Estado global JSON

### Paso 6 — Commit y push

```bash
# Desde la raíz del repo
git add shieldops_backend/
git commit -m "feat: backend 3 cerebros (EyP/LZA/GO) — 69 tests OK"
git push origin feat/backend-3-cerebros
```

### Paso 7 — Pull Request y merge

```
GitHub → Pull Requests → New PR
  Base: main
  Compare: feat/backend-3-cerebros
  Título: "feat: ShieldOps Backend — 3 Cerebros Pokémon"
```

---

## Despliegue en Railway (producción)

### railway.toml (crear en la raíz del repo)

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn shieldops_backend.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/api/v1/health"
healthcheckTimeout = 30
```

### Variables de entorno (Railway → Variables)

```
PORT=8000
PYTHONPATH=/app
```

### Comandos Railway CLI

```bash
npm install -g @railway/cli
railway login
railway link          # Vincular con tu proyecto existente
railway up            # Desplegar
railway logs          # Ver logs en tiempo real
```

---

## Endpoints disponibles

| Método | Ruta | Cerebro | Descripción |
|--------|------|---------|-------------|
| GET | /api/v1/health | Global | Estado de los 3 cerebros |
| GET | /api/v1/eyp/health | EyP | Estado motor VGC |
| POST | /api/v1/eyp/dano | EyP | Daño Gen IX, 16 rolls, Tera |
| POST | /api/v1/eyp/validar-equipo | EyP | Legalidad VGC 2026 |
| GET | /api/v1/lza/health | LZA | Estado motor Action PvP |
| POST | /api/v1/lza/dano | LZA | Daño Action Time, sin habilidades |
| POST | /api/v1/lza/validar-combate | LZA | Switches, Mega, estado |
| GET | /api/v1/go/health | GO | Estado motor GO |
| POST | /api/v1/go/dano | GO | Daño GO (STAB x1.2, inmune x0.391) |
| POST | /api/v1/go/cp | GO | CP + nivel óptimo por liga |
| POST | /api/v1/go/validar-equipo | GO | CP caps Great/Ultra/Master |

---

## Notas de seguridad

- **Sin `eval()`, `exec()` ni `pickle`** en ningún módulo.
- Todos los inputs pasan por validación Pydantic v2 con `extra="ignore"`.
- Los campos `nombre` y `habilidad` rechazan caracteres de inyección SQL/HTML.
- IVs y EVs validados con rangos estrictos (0-15 GO, 0-31 EyP, 0-252 por stat).
- CORS configurado — ajustar `allow_origins` en producción.
