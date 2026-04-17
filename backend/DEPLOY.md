# ShieldOps Backend — Guia de Despliegue

## Estructura

```
backend/
├── main.py                          # FastAPI — monta los 4 routers en /api/v1/
├── requirements.txt                 # fastapi, uvicorn, pydantic
├── core/
│   └── types.py                     # Tabla de tipos compartida, APIResponse
└── cerebros/
    ├── eyp/                         # Cerebro A: Escarlata/Purpura VGC 2026
    │   ├── data/
    │   │   ├── pokemon.py           # 35+ Pokemon VGC, efectividad_eyp()
    │   │   ├── movimientos.py       # 80+ movimientos Gen IX
    │   │   └── objetos.py           # 30+ items competitivos
    │   ├── engine/
    │   │   ├── damage.py            # Formula Gen IX, 16 rolls, Tera, STAB
    │   │   └── guia.py              # Simulacion vs 10 amenazas meta, top 3 builds
    │   ├── models/schemas.py
    │   └── api/router.py            # /eyp/dano /eyp/guia-pokemon /eyp/mejor-equipo
    ├── lza/                         # Cerebro B: Leyendas Z-A Battle Club S7
    │   ├── data/
    │   │   ├── pokemon.py           # 30+ Pokemon, startup_frames, Mega data
    │   │   ├── movimientos.py       # 60+ movimientos Action Time
    │   │   └── objetos.py           # Items LZA (Turbocinta, Piedra Mega...)
    │   ├── engine/
    │   │   ├── damage.py            # Dano Action Time, sin EVs/IVs
    │   │   └── guia.py              # Guia con/sin Mega, dodgeable si frames > 12
    │   ├── models/schemas.py
    │   └── api/router.py            # /lza/dano /lza/guia-pokemon /lza/mejor-equipo
    ├── go/                          # Cerebro C: Pokemon GO Battle League
    │   ├── data/
    │   │   ├── pokemon.py           # 30+ Pokemon GO (stats Niantic), efectividad_go()
    │   │   ├── movimientos.py       # Fast moves + Charged moves con energia
    │   │   └── (sin objetos GO)
    │   ├── engine/
    │   │   ├── damage.py            # STAB x1.2, x1.6/x0.625/x0.391, CP formula
    │   │   └── guia.py              # Optimizacion IVs (0-15) por CP cap, DPS/TDO
    │   ├── models/schemas.py        # CPM_TABLE, IVs 0-15, ligas Great/Ultra/Master
    │   └── api/router.py            # /go/dano /go/cp /go/guia-pokemon /go/catalogo
    └── champions/                   # Cerebro D: Pokemon Champions Singles
        ├── data/
        │   ├── pokemon.py           # 25+ Pokemon multi-gen (Tiers S/A/B)
        │   ├── movimientos.py       # 80+ movimientos competitivos
        │   └── objetos.py           # 40+ items (berries tipo, Life Orb, Choice...)
        ├── engine/
        │   ├── damage.py            # Formula Gen IX, 16 rolls, sin Tera/Mega
        │   └── guia.py              # Simulacion vs 10 amenazas Singles meta
        ├── models/schemas.py
        └── api/router.py            # /champions/dano /champions/guia-pokemon ...
```

---

## Local — Windows (INICIAR.bat)

Ejecutar `INICIAR.bat` en la raiz del proyecto. Hace todo automaticamente.

## Local — Mac / Linux

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Verificar:
```bash
curl http://localhost:8001/api/v1/health
```

---

## Railway (produccion)

El `railway.toml` en la raiz ya esta configurado con:
- Builder: NIXPACKS
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health check: `/api/v1/health`

Solo conecta el repo en https://railway.app y presiona Deploy.

---

## Endpoints de salud

```
GET /api/v1/health              <- Estado global (4 cerebros)
GET /api/v1/eyp/health
GET /api/v1/lza/health
GET /api/v1/go/health
GET /api/v1/champions/health
GET /docs                       <- Swagger UI interactivo
```

---

## Aislamiento entre cerebros

Cada cerebro importa UNICAMENTE de su propio directorio y de `core/types.py`.
No hay imports cruzados entre `eyp/`, `lza/`, `go/` y `champions/`.

La tabla de tipos (`core/types.py`) es compartida pero cada cerebro aplica
sus propios multiplicadores:
- EyP / LZA / Champions: x2.0 / x0.5 / x0.0
- GO: x1.6 / x0.625 / x0.391

---

## Seguridad

- Todos los inputs pasan por validacion Pydantic v2
- Sin eval(), exec() ni pickle en ningun modulo
- IVs, EVs y stats validados con rangos estrictos
- CORS configurado — ajustar `allow_origins` en produccion
