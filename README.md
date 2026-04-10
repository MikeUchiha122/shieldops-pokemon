# 🛡️ ShieldOps Pokémon — Sistema Completo 2026

<div align="center">

![VGC 2026](https://img.shields.io/badge/VGC-2026-orange) ![LZA S7](https://img.shields.io/badge/LZA-Battle%20Club%20S7-purple) ![GO S26](https://img.shields.io/badge/GO-Battle%20League%20S26-yellow)

**Motor de cálculo competitivo para Escarlata/Púrpura, Leyendas Z-A y Pokémon GO**

🌐 **Web:** https://MikeUchiha122.github.io/shieldops-pokemon

</div>

---

## 🚀 Inicio Rápido

### ⚡ Online (Recomendado)

Abre en tu navegador: **https://MikeUchiha122.github.io/shieldops-pokemon**

> Funciona 100% offline — todos los cálculos se hacen localmente en JavaScript

### 💻 Local (Frontend)

```bash
# Windows
start index.html

# Mac
open index.html

# Linux
xdg-open index.html
```

---

## 📁 Estructura del Proyecto

```
shieldops-pokemon/
├── 🖥️  index.html          ← Aplicación completa (todo en uno)
├── 🐍  backend/             ← Backend FastAPI (opcional)
│   ├── main.py             ← Servidor Python
│   ├── core/               ← Tipos y tablas de efectividad
│   ├── cerebros/           ← 3 motores de cálculo
│   │   ├── eyp/            ← Escarlata/Púrpura VGC
│   │   ├── lza/            ← Leyendas Z-A Action PvP
│   │   └── go/             ← Pokémon GO GBL
│   └── tests/              ← 69 tests
├── 🐳 Dockerfile            ← Para desplegar en Railway
└── 📖 README.md            ← Este archivo
```

---

## 🛠️ Instalación del Backend (Opcional)

El frontend funciona sin el backend. Pero si quieres los 3 cerebros conectados:

### Windows (PowerShell)

```powershell
# 1. Entrar al backend
cd backend

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar
.venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt -r requirements-dev.txt

# 5. Verificar tests (69 passed)
python -m pytest tests/ -v

# 6. Iniciar servidor en puerto 8001
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Mac / Linux / Kali

```bash
# 1. Entrar al backend
cd backend

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt -r requirements-dev.txt

# Kali Linux (si hay error)
pip install -r requirements.txt --break-system-packages

# 4. Verificar tests (69 passed)
python -m pytest tests/ -v

# 5. Iniciar servidor en puerto 8001
uvicorn main:app --reload --host 0.0.0.0 --port 8001
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

## ☁️ Desplegar en GitHub Pages

```bash
# 1. Clone el repo
git clone https://github.com/MikeUchiha122/shieldops-pokemon.git
cd shieldops-pokemon

# 2. El archivo index.html ya está en la raíz
# Solo necesitas hacer:

git add .
git commit -m "Actualización"
git push

# 3. Activa GitHub Pages:
# Settings → Pages → Branch: main → Save

# URL: https://MikeUchiha122.github.io/shieldops-pokemon
```

---

## 🧪 Tests

| Suite | Tests | Estado |
|-------|-------|--------|
| `unit/test_eyp.py` | 19 | ✅ Gen IX, STAB, Tera, 16 rolls |
| `unit/test_lza.py` | 16 | ✅ Startup frames, Mega |
| `unit/test_go.py` | 19 | ✅ CP, efectividad ×1.6 |
| `integration/test_api.py` | 15 | ✅ Endpoints |
| **TOTAL** | **69** | ✅ 0 fallos |

---

## 🔧 Tecnologías

<div align="center">

| Componente | Tecnología |
|------------|------------|
| Frontend | HTML/CSS/JS vanilla |
| IA | Gemini 2.5 Flash |
| Backend | FastAPI · Pydantic v2 · Uvicorn |
| Python | 3.12+ |
| Tests | pytest · httpx |
| Deploy | GitHub Pages |

</div>

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