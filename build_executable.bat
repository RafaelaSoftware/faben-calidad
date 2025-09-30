@echo off
REM ============================================================
REM NC AC Registrador - Compilador Simple y Compatible
REM Versión simplificada que evita conflictos comunes
REM ============================================================

echo.
echo =============================================
echo   NC AC Registrador - Compilador SIMPLE
echo =============================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está disponible
    pause
    exit /b 1
)

echo 🐍 Python disponible: 
python --version

REM Verificar archivo principal
if not exist "NC_AC_Registrador_Faben.py" (
    echo ❌ ERROR: Archivo principal no encontrado
    pause
    exit /b 1
)

REM Instalar PyInstaller si no está disponible
echo 🔍 Verificando PyInstaller...
python -c "import PyInstaller" 2>nul || (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
)

REM Verificar dependencias esenciales únicamente
echo 🔍 Verificando dependencias mínimas...
python -c "import PyQt6; print('✅ PyQt6 OK')" 2>nul || (
    echo 📦 Instalando PyQt6...
    pip install PyQt6
)

python -c "import openpyxl; print('✅ OpenPyXL OK')" 2>nul || (
    echo 📦 Instalando OpenPyXL...
    pip install openpyxl
)

echo.
echo 🧹 Limpiando compilaciones anteriores...
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build" rmdir /s /q "build" 2>nul
if exist "*.spec" del /q "*.spec" 2>nul

echo.
echo 🏗️  Compilando con configuración SIMPLE...
echo    (Este método es más lento pero más compatible)
echo.

REM Compilación simple sin problemas de dependencias
pyinstaller ^
    --distpath dist ^
    --workpath build ^
    --specpath . ^
    --name "NC_AC_Registrador_Faben" ^
    --windowed ^
    --noconfirm ^
    --clean ^
    --add-data "*.db;." ^
    NC_AC_Registrador_Faben.py

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Compilación falló
    echo.
    echo 🔧 Probando método ALTERNATIVO...
    echo.
    
    REM Método alternativo: compilación básica
    pyinstaller --windowed --onedir --name "NC_AC_Registrador_Faben" NC_AC_Registrador_Faben.py
    
    if errorlevel 1 (
        echo ❌ ERROR: Ambos métodos fallaron
        echo.
        echo 💡 Soluciones posibles:
        echo    1. Reinstalar PyInstaller: pip uninstall pyinstaller ^&^& pip install pyinstaller
        echo    2. Usar entorno virtual limpio
        echo    3. Ejecutar como administrador
        echo.
        pause
        exit /b 1
    )
)

REM Verificar resultado
if not exist "dist\NC_AC_Registrador_Faben\NC_AC_Registrador_Faben.exe" (
    echo ❌ ERROR: Ejecutable no generado correctamente
    pause
    exit /b 1
)

echo.
echo ✅ ¡Compilación exitosa!
echo.
echo 📂 Ubicación: dist\NC_AC_Registrador_Faben\
for %%I in ("dist\NC_AC_Registrador_Faben\NC_AC_Registrador_Faben.exe") do echo 📊 Tamaño: %%~zI bytes

echo.
echo 🧹 Limpiando...
if exist "build" rmdir /s /q "build" 2>nul
if exist "*.spec" del /q "*.spec" 2>nul

echo.
echo 🎯 Preparando distribución...
if not exist "NC_AC_FABEN_Distribution" mkdir "NC_AC_FABEN_Distribution"

echo    - Copiando ejecutable y dependencias...
xcopy "dist\NC_AC_Registrador_Faben" "NC_AC_FABEN_Distribution" /E /I /Y >nul

echo    - Copiando archivos adicionales...
if exist "nc_ac_faben.db" copy "nc_ac_faben.db" "NC_AC_FABEN_Distribution\" >nul

if not exist "NC_AC_FABEN_Distribution\log" mkdir "NC_AC_FABEN_Distribution\log"
if not exist "NC_AC_FABEN_Distribution\attachments" mkdir "NC_AC_FABEN_Distribution\attachments"

echo.
echo ✅ ¡Distribución lista!
echo.
echo 📦 Carpeta: NC_AC_FABEN_Distribution\
echo    - NC_AC_Registrador_Faben.exe (ejecutable)
echo    - Bibliotecas y dependencias
echo    - nc_ac_faben.db (base de datos)
echo    - log\ y attachments\ (carpetas de trabajo)
echo.

echo 🧪 ¿Probar el ejecutable? (S/N)
set /p test="> "
if /i "%test%"=="S" (
    echo.
    echo 🚀 Iniciando prueba...
    start "" "NC_AC_FABEN_Distribution\NC_AC_Registrador_Faben.exe"
    echo ✅ Ejecutable lanzado
    echo.
)

echo 🎉 ¡Proceso completado!
echo.
pause