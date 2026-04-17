# ShieldOps Pokemon

Motor de calculo competitivo para los 4 juegos de Pokemon activos en 2026.

| Cerebro | Juego | Formato | Mecanica clave |
|---------|-------|---------|----------------|
| **A — EyP** | Escarlata / Purpura | VGC 2026 Reg F (Dobles) | Gen IX, 16 rolls, EVs/IVs/Natures |
| **B — LZA** | Leyendas Z-A | Battle Club S7 (Action PvP) | startup_frames, cooldown_ms, Mega |
| **C — GO** | Pokemon GO | GO Battle League S26 | CP, IVs 0-15, x1.6/x0.625/x0.391 |
| **D — Champions** | Pokemon Champions | Singles multi-gen (Gen I-IX) | formula Gen IX, sin Tera/Mega/Dmax |

---

## Inicio rapido — Windows

**Descarga el repo, abre la carpeta y haz doble clic en `INICIAR.bat`.**

El script hace todo solo:
1. Verifica Python 3.12+
2. Crea el entorno virtual en `backend/.venv/`
3. Instala `fastapi`, `uvicorn`, `pydantic`
4. Apunta el frontend a `localhost:8001`
5. Arranca el backend en una ventana nueva
6. Abre `index.html` en el navegador con los 4 cerebros online

> Requiere Python 3.12+ instalado con "Add Python to PATH" marcado.
> Descarga: https://www.python.org/downloads/

---

## Inicio manual — Mac / Linux

```bash
# 1. Entrar al backend
cd backend

# 2. Crear e iniciar entorno virtual
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Arrancar el servidor
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

Luego editar `index.html` y cambiar:
```javascript
var BACKEND = null;
// por:
var BACKEND = "http://localhost:8001/api/v1";
```

Abrir `index.html` en el navegador.

---

## Verificar los 4 cerebros

```bash
curl http://localhost:8001/api/v1/health

curl http://localhost:8001/api/v1/eyp/health
curl http://localhost:8001/api/v1/lza/health
curl http://localhost:8001/api/v1/go/health
curl http://localhost:8001/api/v1/champions/health
```

Swagger UI completo: http://localhost:8001/docs

---

## Endpoints

| Metodo | Ruta | Cerebro | Descripcion |
|--------|------|---------|-------------|
| GET | /api/v1/health | Global | Estado de los 4 cerebros |
| POST | /api/v1/eyp/dano | EyP | Dano Gen IX, 16 rolls |
| POST | /api/v1/eyp/guia-pokemon | EyP | Top 3 builds VGC vs amenazas meta |
| POST | /api/v1/eyp/mejor-equipo | EyP | Equipo VGC alrededor de un ancla |
| GET | /api/v1/eyp/catalogo | EyP | Catalogo VGC 2026 |
| POST | /api/v1/lza/dano | LZA | Dano Action Time |
| POST | /api/v1/lza/guia-pokemon | LZA | Guia con/sin Mega, startup frames |
| POST | /api/v1/lza/mejor-equipo | LZA | Equipo Battle Club |
| GET | /api/v1/lza/catalogo | LZA | Catalogo LZA |
| POST | /api/v1/go/dano | GO | Dano GO (STAB x1.2, inmune x0.391) |
| POST | /api/v1/go/cp | GO | CP + nivel optimo por liga |
| POST | /api/v1/go/guia-pokemon | GO | IVs optimos + moveset por liga |
| GET | /api/v1/go/catalogo | GO | Catalogo GO por liga |
| POST | /api/v1/champions/dano | Champions | Dano Singles Gen IX |
| POST | /api/v1/champions/guia-pokemon | Champions | Top 3 builds Singles multi-gen |
| POST | /api/v1/champions/mejor-equipo | Champions | Equipo de 6 alrededor de un ancla |
| GET | /api/v1/champions/catalogo | Champions | Catalogo por tier (S/A/B) |
| GET | /api/v1/champions/movimientos | Champions | Movimientos por tipo |

---

## Diferencias entre juegos

| Mecanica | EyP / LZA / Champions | Pokemon GO |
|----------|-----------------------|------------|
| STAB | x1.5 | x1.2 |
| Super efectivo | x2.0 | x1.6 |
| Poco efectivo | x0.5 | x0.625 |
| Inmune | x0.0 | x0.391 |
| IVs | 0–31 | 0–15 |
| Nivel | 50 (competitivo) | 1–51 |
| Equipo | 6 Pokemon | 3 Pokemon |

---

## Estructura del proyecto

```
shieldops-pokemon/
├── INICIAR.bat                  <- Launcher Windows (instala + arranca todo)
├── index.html                   <- Frontend completo (HTML/JS/CSS)
├── backend/
│   ├── main.py                  <- FastAPI — monta los 4 routers
│   ├── requirements.txt
│   ├── core/
│   │   └── types.py             <- Tabla de tipos compartida (18 tipos)
│   └── cerebros/
│       ├── eyp/                 <- Cerebro A: EyP VGC 2026
│       │   ├── data/            <- pokemon.py, movimientos.py, objetos.py
│       │   ├── engine/          <- damage.py, guia.py
│       │   └── api/router.py
│       ├── lza/                 <- Cerebro B: Leyendas Z-A
│       │   ├── data/
│       │   ├── engine/
│       │   └── api/router.py
│       ├── go/                  <- Cerebro C: Pokemon GO
│       │   ├── data/
│       │   ├── engine/
│       │   └── api/router.py
│       └── champions/           <- Cerebro D: Champions Singles
│           ├── data/
│           ├── engine/
│           ├── models/
│           └── api/router.py
├── Dockerfile
└── railway.toml
```

---

## Despliegue en Railway (produccion)

El `railway.toml` ya esta configurado. Solo conecta el repo en railway.app y despliega.

El frontend detecta automaticamente si el backend esta online y muestra el estado de cada cerebro.

---

## Tecnologias

- **Frontend:** HTML / CSS / JavaScript vanilla
- **IA en frontend:** Gemini 2.5 Flash (API key del usuario)
- **Backend:** FastAPI + Pydantic v2 + Uvicorn
- **Python:** 3.12+

---

MIT — MikeUchiha122 · 2026
