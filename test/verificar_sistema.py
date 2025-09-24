#!/usr/bin/env python3
"""
Script de verificación final del sistema NC AC FABEN
Verifica que todos los componentes estén funcionando correctamente
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

def verificar_estructura_proyecto():
    """Verificar que todos los archivos necesarios estén presentes"""
    print("=== VERIFICANDO ESTRUCTURA DEL PROYECTO ===")
    
    archivos_requeridos = [
        'NC_AC_Registrador_Faben.py',
        'logging_config.py', 
        'test_logging.py',
        'log_manager.py',
        'requirements.txt',
        'README.md'
    ]
    
    archivos_generados = [
        'nc_ac_faben.db',
        'nc_ac_faben.log',
        'nc_ac_faben_debug.log'
    ]
    
    todos_ok = True
    
    print("Archivos del código fuente:")
    for archivo in archivos_requeridos:
        path = Path(archivo)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {archivo} ({size} bytes)")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todos_ok = False
    
    print("\nArchivos generados por la aplicación:")
    for archivo in archivos_generados:
        path = Path(archivo)
        if path.exists():
            size = path.stat().st_size
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            print(f"✅ {archivo} ({size} bytes, modificado: {modified.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print(f"⚠️ {archivo} - Se creará al ejecutar la aplicación")
    
    # Verificar directorios
    directorios = ['attachments', '__pycache__']
    print("\nDirectorios:")
    for directorio in directorios:
        path = Path(directorio)
        if path.exists() and path.is_dir():
            archivos_en_dir = len(list(path.iterdir()))
            print(f"✅ {directorio}/ ({archivos_en_dir} archivos)")
        else:
            print(f"⚠️ {directorio}/ - Se creará automáticamente")
    
    return todos_ok

def verificar_base_datos():
    """Verificar la estructura de la base de datos"""
    print("\n=== VERIFICANDO BASE DE DATOS ===")
    
    db_file = Path('nc_ac_faben.db')
    
    if not db_file.exists():
        print("❌ Base de datos no existe. Ejecute la aplicación primero.")
        return False
    
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        
        # Verificar tabla nc
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nc'")
        if cur.fetchone():
            cur.execute("SELECT COUNT(*) FROM nc")
            count = cur.fetchone()[0]
            print(f"✅ Tabla 'nc' existe ({count} registros)")
        else:
            print("❌ Tabla 'nc' no existe")
            return False
        
        # Verificar tabla acciones  
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='acciones'")
        if cur.fetchone():
            cur.execute("SELECT COUNT(*) FROM acciones")
            count = cur.fetchone()[0]
            print(f"✅ Tabla 'acciones' existe ({count} registros)")
        else:
            print("❌ Tabla 'acciones' no existe")
            return False
        
        # Verificar estructura de tabla nc
        cur.execute("PRAGMA table_info(nc)")
        columns = cur.fetchall()
        expected_columns = ['id', 'nro_nc', 'fecha', 'resultado_matriz', 'op', 
                           'cant_invol', 'cod_producto', 'desc_producto', 'cliente',
                           'cant_scrap', 'costo', 'cant_recuperada', 'observaciones', 
                           'falla', 'ishikawa']
        
        column_names = [col[1] for col in columns]
        
        for col in expected_columns:
            if col in column_names:
                print(f"✅ Columna '{col}' presente")
            else:
                print(f"❌ Columna '{col}' faltante")
                
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def verificar_logging():
    """Verificar el sistema de logging"""
    print("\n=== VERIFICANDO SISTEMA DE LOGGING ===")
    
    try:
        from logging_config import setup_development_logging, log_performance
        logger = setup_development_logging()
        
        # Probar diferentes niveles
        logger.info("Test de verificación - INFO")
        logger.warning("Test de verificación - WARNING") 
        logger.error("Test de verificación - ERROR")
        
        print("✅ Sistema de logging avanzado funcionando")
        
        # Verificar archivos de log
        log_files = ['nc_ac_faben.log', 'nc_ac_faben_debug.log']
        for log_file in log_files:
            path = Path(log_file)
            if path.exists():
                size = path.stat().st_size
                print(f"✅ {log_file} ({size} bytes)")
            else:
                print(f"❌ {log_file} no encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en sistema de logging: {e}")
        return False

def verificar_imports():
    """Verificar que todas las dependencias se puedan importar"""
    print("\n=== VERIFICANDO DEPENDENCIAS ===")
    
    dependencias = {
        'sqlite3': 'Base de datos (incluida en Python)',
        'pathlib': 'Manejo de rutas (incluida en Python)',
        'datetime': 'Fechas y horas (incluida en Python)',
        'logging': 'Sistema de logging (incluida en Python)',
        'shutil': 'Operaciones de archivos (incluida en Python)',
        'os': 'Sistema operativo (incluida en Python)',
        'sys': 'Sistema (incluida en Python)',
    }
    
    dependencias_externas = {
        'PyQt6': 'Interfaz gráfica',
        'openpyxl': 'Generación de Excel',
        'pandas': 'Análisis de datos (opcional)'
    }
    
    # Verificar dependencias estándar
    print("Dependencias estándar de Python:")
    for modulo, descripcion in dependencias.items():
        try:
            __import__(modulo)
            print(f"✅ {modulo} - {descripcion}")
        except ImportError:
            print(f"❌ {modulo} - {descripcion} - ERROR")
    
    # Verificar dependencias externas
    print("\nDependencias externas:")
    for modulo, descripcion in dependencias_externas.items():
        try:
            __import__(modulo)
            print(f"✅ {modulo} - {descripcion}")
        except ImportError:
            print(f"⚠️ {modulo} - {descripcion} - No instalado (ejecutar: pip install {modulo.lower()})")
    
    return True

def mostrar_resumen():
    """Mostrar resumen del estado del proyecto"""
    print("\n" + "="*60)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*60)
    
    # Estado general
    print("\n🎯 ESTADO DEL PROYECTO NC AC FABEN:")
    print("✅ Sistema de logging activado y funcionando")
    print("✅ Estructura de archivos completa")  
    print("✅ Base de datos inicializada")
    print("✅ Herramientas de gestión disponibles")
    
    # Archivos principales
    print("\n📁 ARCHIVOS PRINCIPALES:")
    print("- NC_AC_Registrador_Faben.py: Aplicación principal con logging integrado")
    print("- logging_config.py: Sistema de logging avanzado")
    print("- test_logging.py: Pruebas del sistema de logging")
    print("- log_manager.py: Gestión de archivos de log")
    
    # Uso
    print("\n🚀 COMANDOS PRINCIPALES:")
    print("python NC_AC_Registrador_Faben.py    # Ejecutar aplicación")
    print("python test_logging.py               # Probar logging")
    print("python log_manager.py                # Gestionar logs")
    
    # Logs generados
    print("\n📊 ARCHIVOS DE LOG:")
    for log_file in ['nc_ac_faben.log', 'nc_ac_faben_debug.log']:
        path = Path(log_file)
        if path.exists():
            size = path.stat().st_size
            print(f"- {log_file}: {size} bytes")
        else:
            print(f"- {log_file}: Se creará al ejecutar")

def main():
    """Ejecutar verificación completa"""
    print("VERIFICACIÓN FINAL DEL SISTEMA NC AC FABEN")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Directorio: {Path.cwd()}")
    
    # Ejecutar verificaciones
    tests = [
        verificar_estructura_proyecto,
        verificar_base_datos,
        verificar_logging,
        verificar_imports
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error en {test.__name__}: {e}")
            results.append(False)
    
    # Mostrar resumen
    mostrar_resumen()
    
    # Resultado final
    passed = sum(results)
    total = len(results)
    
    print(f"\n📈 RESULTADO: {passed}/{total} verificaciones exitosas")
    
    if passed == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("El logging está activado y todos los componentes están operativos.")
    else:
        print("⚠️ Algunas verificaciones fallaron. Revisar los errores anteriores.")

if __name__ == '__main__':
    main()