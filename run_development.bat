@echo off
REM ============================================================
REM NC AC Registrador - Modo Desarrollo
REM Ejecuta la aplicación directamente desde Python
REM ============================================================

echo.
echo ========================================
echo   NC AC Registrador - Modo Desarrollo
echo ========================================
echo.

REM Verificar que Python está disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo Por favor:
    echo 1. Instala Python desde https://python.org
    echo 2. Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

REM Mostrar versión de Python
echo 🐍 Versión de Python:
python --version
echo.

REM Verificar si existe el archivo principal
if not exist "NC_AC_Registrador_Faben.py" (
    echo ❌ ERROR: No se encuentra el archivo principal NC_AC_Registrador_Faben.py
    echo.
    echo Asegúrate de ejecutar este archivo desde la carpeta correcta.
    echo.
    pause
    exit /b 1
)

REM Verificar dependencias principales
echo 🔍 Verificando dependencias...
python -c "import PyQt6; print('✅ PyQt6 disponible')" 2>nul || (
    echo ❌ ERROR: PyQt6 no está instalado
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

python -c "import pandas; print('✅ Pandas disponible')" 2>nul || (
    echo ⚠️  Pandas no disponible, instalando...
    pip install pandas
)

python -c "import openpyxl; print('✅ OpenPyXL disponible')" 2>nul || (
    echo ⚠️  OpenPyXL no disponible, instalando...
    pip install openpyxl
)

echo.
echo 🚀 Iniciando aplicación en modo desarrollo...
echo.
echo ============================================
echo   Presiona Ctrl+C para salir de la app
echo ============================================
echo.

REM Ejecutar la aplicación
python NC_AC_Registrador_Faben.py

REM Verificar código de salida
if errorlevel 1 (
    echo.
    echo ❌ La aplicación terminó con errores
    echo.
    echo 📋 Verifica los logs en la carpeta 'log' para más detalles:
    if exist "log\nc_ac_faben.log" (
        echo    - log\nc_ac_faben.log
    )
    if exist "log\nc_ac_faben_debug.log" (
        echo    - log\nc_ac_faben_debug.log
    )
    echo.
) else (
    echo.
    echo ✅ Aplicación cerrada correctamente
    echo.
)

echo Presiona cualquier tecla para salir...
pause >nul