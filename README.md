# 🛡️ ShieldOps Pokémon — Sistema Completo 2026

<div align="center">

![VGC 2026](https://img.shields.io/badge/VGC-2026-orange) ![LZA S7](https://img.shields.io/badge/LZA-Battle%20Club%20S7-purple) ![GO S26](https://img.shields.io/badge/GO-Battle%20League%20S26-yellow)

**Motor de cálculo competitivo para Escarlata/Púrpura, Leyendas Z-A y Pokémon GO**

</div>

---

## 🚀 Inicio Rápido

### 📥 Descargar y Ejecutar

#### 1. Descargar el ZIP

Descarga **ShieldOps-CONECTADO.zip** de donde lo obtuviste y descomprímelo.

#### 2. Abrir el Frontend

```bash
# Windows
start ShieldOps-Proyecto\frontend\index.html

# Mac
open ShieldOps-Proyecto/frontend/index.html

# Linux
xdg-open ShieldOps-Proyecto/frontend/index.html
```

> ⚠️ **Importante:** El frontend funciona **sin instalar nada** — solo ábrelo en Chrome o Edge.

### 🤖 ¿Usar los 3 Cerebros o No?

| Característica | Sin Cerebros (Frontend solo) | Con Cerebros (Backend) |
|----------------|------------------------------|----------------------|
| **Calculadora de daño** | ✅ Funciona (JavaScript) | ✅ Verificación extra |
| **Equipos predefinidos** | ✅ Funciona | ✅ Validación de legality |
| **Guía de entrenamiento** | ✅ Funciona | ✅ Mejores recomendaciones |
| **Agente IA** | ✅ Funciona (Gemini) | ✅ Mejor contexto |
| **Indicador de estado** | ⚡ "Modo Offline" | ✅ "3/3 Cerebros Online" |
| **Instalación** | Ninguna | Requiere Python + pip |
| **Velocidad** | Instantáneo | Depende de la red |

#### Recomendación

- **Sin backend:** Ideal para uso rápido — todo funciona localmente en JavaScript.
- **Con backend:** Para verificación precisa, validaciones adicionales y futuro desarrollo.

#### Diferencia en los Cálculos

Los 3 cerebros (backend Python) realizan cálculos más precisos siguiendo las reglas oficiales de cada juego:
- **EyP:** Gen IX, 16 rolls de daño, Tera-type, Mega evolutions
- **LZA:** Action Time PvP, startup frames, cooldowns
- **GO:** CP fórmula, multiplicadores GO (×1.2 STAB, ×1.6 super efectivo)

El frontend tiene una implementación en JavaScript que cubre ~95% de los casos. El backend verifica y valida estos cálculos con lógica 100% oficial.

#### 3. Configurar API Key (opcional)

Para el agente IA:
1. Ve a [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Crea una API key (es gratis)
3. Pégala en el recuadro amarillo del frontend y guarda

---

## 🖥️ Desplegar Backend (Opcional)

El frontend funciona sin backend. Pero si quieres los **3 cerebros conectados**:

### Windows (PowerShell)

```powershell
# 1. Entra a la carpeta del backend
cd ruta\ShieldOps-Proyecto\backend

# 2. Crea entorno virtual
python -m venv .venv

# 3. Activa el entorno
.venv\Scripts\activate
# Verás (.venv) al inicio de la línea

# 4. Instala dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. Verifica los tests (deben dar 69 passed)
python -m pytest tests/ -v

# 6. Inicia el servidor en puerto 8001
uvicorn main:app --reload --host 0.0.0.0 --port 8001

# Verás: INFO: Uvicorn running on http://0.0.0.0:8001
```

### Mac / Linux / Kali

```bash
# 1. Entra a la carpeta del backend
cd ruta/ShieldOps-Proyecto/backend

# 2. Crea entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instala dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Kali Linux (si da error de sistema)
pip install -r requirements.txt --break-system-packages
pip install -r requirements-dev.txt --break-system-packages

# 4. Verifica los tests
python -m pytest tests/ -v

# 5. Inicia el servidor en puerto 8001
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Verificar que los Cerebros Funcionan

Con el servidor corriendo, abre una **nueva terminal**:

```bash
# Estado de los 3 cerebros
curl http://localhost:8001/api/v1/health

# Cerebro A — EyP VGC 2026
curl http://localhost:8001/api/v1/eyp/health

# Cerebro B — LZA Action PvP
curl http://localhost:8001/api/v1/lza/health

# Cerebro C — Pokémon GO
curl http://localhost:8001/api/v1/go/health
```

### Conectar Frontend al Backend

Edita `index.html` y cambia:

```javascript
// Donde dice:
var BACKEND = null;

// Cambia a:
var BACKEND = "http://localhost:8001/api/v1";
```

---

## 📁 Estructura del Proyecto

```
ShieldOps-Proyecto/
├── frontend/
│   ├── index.html          ← Aplicación completa
│   └── README.md           ← Guía del frontend
└── backend/
    ├── main.py             ← FastAPI app
    ├── requirements.txt
    ├── requirements-dev.txt
    ├── core/
    │   └── types.py        ← Tabla efectividad tipos
    ├── cerebros/
    │   ├── eyp/            ← Cerebro A: EyP VGC
    │   ├── lza/            ← Cerebro B: LZA Action
    │   └── go/             ← Cerebro C: Pokémon GO
    └── tests/
        ├── unit/           ← 54 tests
        └── integration/     ← 15 tests
```

---

## 🧪 Tests

| Suite | Tests | Cobertura |
|-------|-------|-----------|
| `unit/test_eyp.py` | 19 | Stats Gen IX, STAB, Tera, 16 rolls |
| `unit/test_lza.py` | 16 | Startup frames, cooldowns, Mega |
| `unit/test_go.py` | 19 | CP, efectividad ×1.6/x0.391 |
| `integration/test_api.py` | 15 | Endpoints, aislamiento |
| **TOTAL** | **69** | ✅ 0 fallos |

---

## 🔧 Tecnologías

| Componente | Tecnología |
|------------|------------|
| Frontend | HTML/CSS/JS vanilla |
| IA | Gemini 2.5 Flash |
| Backend | FastAPI · Pydantic v2 · Uvicorn |
| Python | 3.12+ |
| Tests | pytest · httpx |

---

## 📊 Diferencias entre Juegos

| Mecánica | EyP / LZA | Pokémon GO |
|----------|-----------|------------|
| STAB | ×1.5 | ×1.2 |
| Super efectivo | ×2.0 | ×1.6 |
| Poco efectivo | ×0.5 | ×0.625 |
| Inmune | ×0 | ×0.391 |
| IVs | 0–31 | 0–15 |
| Equipo | 6 Pokémon | 3 Pokémon |
| Nivel | 50 (fijo) | 1–51 |

---

## 📄 Licencia

MIT — **MikeUchiha122** · Abril 2026

---

<div align="center">

*"El mejor set es el que el rival no puede predecir."*

</div>