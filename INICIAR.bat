@echo off
setlocal EnableDelayedExpansion
title ShieldOps Pokemon -- Iniciando 4 Cerebros

echo.
echo  ============================================================
echo   ShieldOps Pokemon -- Launcher v2.0
echo   Cerebros: EyP (VGC 2026) / LZA / GO / Champions
echo  ============================================================
echo.

:: ── 1. Verificar Python ───────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python no encontrado.
    echo.
    echo  Instala Python 3.12+ desde:
    echo    https://www.python.org/downloads/
    echo.
    echo  IMPORTANTE: marca "Add Python to PATH" al instalar.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo  [OK] %PYVER%

:: ── 2. Crear entorno virtual si no existe ─────────────────────────────
if not exist "%~dp0backend\.venv\Scripts\activate.bat" (
    echo  [..] Creando entorno virtual (solo la primera vez)...
    python -m venv "%~dp0backend\.venv"
    if errorlevel 1 (
        echo  [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
    echo  [OK] Entorno virtual creado
) else (
    echo  [OK] Entorno virtual listo
)

:: ── 3. Instalar dependencias ──────────────────────────────────────────
echo  [..] Instalando/verificando dependencias...
call "%~dp0backend\.venv\Scripts\activate.bat"
pip install -r "%~dp0backend\requirements.txt" --quiet --disable-pip-version-check
if errorlevel 1 (
    echo  [ERROR] Fallo al instalar dependencias.
    echo  Revisa tu conexion a internet o ejecuta como Administrador.
    pause
    exit /b 1
)
echo  [OK] Dependencias OK (fastapi, uvicorn, pydantic)

:: ── 4. Apuntar el frontend al backend local ───────────────────────────
echo  [..] Configurando frontend -> http://localhost:8001/api/v1 ...
powershell -NoProfile -Command ^
  "(Get-Content '%~dp0index.html' -Raw) -replace 'var BACKEND = null;', 'var BACKEND = ""http://localhost:8001/api/v1"";' | Set-Content '%~dp0index.html' -Encoding UTF8"
echo  [OK] Frontend configurado

:: ── 5. Lanzar backend en ventana separada ────────────────────────────
echo  [..] Iniciando backend (puerto 8001)...
start "ShieldOps -- 4 Cerebros Backend" cmd /k ^
  "cd /d "%~dp0backend" && call .venv\Scripts\activate.bat && echo. && echo  [EyP] http://localhost:8001/api/v1/eyp/health && echo  [LZA] http://localhost:8001/api/v1/lza/health && echo  [GO]  http://localhost:8001/api/v1/go/health && echo  [CHM] http://localhost:8001/api/v1/champions/health && echo  [DOC] http://localhost:8001/docs && echo. && uvicorn main:app --host 0.0.0.0 --port 8001 --reload"

:: ── 6. Esperar hasta que el servidor responda ─────────────────────────
echo  [..] Esperando que el servidor levante...
:WAIT
powershell -NoProfile -Command ^
  "try { Invoke-WebRequest -Uri 'http://localhost:8001/api/v1/health' -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    timeout /t 2 /nobreak >nul
    goto WAIT
)
echo  [OK] Backend online -- 4/4 Cerebros activos

:: ── 7. Abrir la app en el navegador predeterminado ───────────────────
echo  [..] Abriendo ShieldOps en el navegador...
start "" "%~dp0index.html"

echo.
echo  ============================================================
echo   ShieldOps corriendo correctamente.
echo.
echo   Frontend : %~dp0index.html
echo   Backend  : http://localhost:8001/docs
echo   Swagger  : http://localhost:8001/docs
echo.
echo   Cierra la ventana "4 Cerebros Backend" para detener.
echo  ============================================================
echo.
pause
endlocal
