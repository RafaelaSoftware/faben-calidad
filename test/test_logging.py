#!/usr/bin/env python3
"""
Script de prueba para el sistema de logging de NC AC FABEN
Útil para verificar que el logging funciona correctamente
"""

import sys
from pathlib import Path

# Añadir el directorio padre al path para importar módulos locales
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

def test_logging_basic():
    """Prueba básica del sistema de logging"""
    print("=== PRUEBA DE LOGGING BÁSICO ===")
    
    try:
        from log import setup_development_logging, log_performance
        logger = setup_development_logging()
        
        # Probar diferentes niveles
        logger.debug("Este es un mensaje DEBUG")
        logger.info("Este es un mensaje INFO")  
        logger.warning("Este es un mensaje WARNING")
        logger.error("Este es un mensaje ERROR")
        logger.critical("Este es un mensaje CRITICAL")
        
        print("✅ Logging básico funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en logging básico: {e}")
        return False

def test_logging_performance():
    """Prueba del decorador de performance"""
    print("\n=== PRUEBA DE PERFORMANCE LOGGING ===")
    
    try:
        from log import setup_development_logging, log_performance
        import time
        
        logger = setup_development_logging()
        
        @log_performance
        def funcion_ejemplo(duracion=1):
            """Función de ejemplo para probar performance logging"""
            logger.info(f"Simulando trabajo por {duracion} segundos...")
            time.sleep(duracion)
            return f"Trabajo completado en {duracion}s"
        
        resultado = funcion_ejemplo(0.5)
        logger.info(f"Resultado: {resultado}")
        
        print("✅ Performance logging funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en performance logging: {e}")
        return False

def test_logging_database_simulation():
    """Simular logging de operaciones de base de datos"""
    print("\n=== PRUEBA DE LOGGING DE BASE DE DATOS ===")
    
    try:
        from log import setup_development_logging, get_module_logger
        
        # Logger específico para base de datos
        db_logger = get_module_logger('database')
        
        # Simular operaciones de base de datos
        db_logger.info("Conectando a base de datos...")
        db_logger.info("Ejecutando consulta: SELECT * FROM nc")
        db_logger.info("3 registros encontrados")
        db_logger.info("Conexión cerrada exitosamente")
        
        # Simular un error
        db_logger.warning("Advertencia: Registro duplicado detectado")
        db_logger.error("Error simulado: Conexión perdida")
        
        print("✅ Logging de base de datos funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en logging de BD: {e}")
        return False

def test_logging_files():
    """Verificar que los archivos de log se crean correctamente"""
    print("\n=== PRUEBA DE ARCHIVOS DE LOG ===")
    
    try:
        log_file = Path.cwd() / 'nc_ac_faben.log'
        debug_file = Path.cwd() / 'nc_ac_faben_debug.log'
        
        # Verificar que existen
        files_ok = True
        
        if log_file.exists():
            size = log_file.stat().st_size
            print(f"✅ Archivo principal: {log_file} ({size} bytes)")
        else:
            print(f"⚠️ Archivo principal no encontrado: {log_file}")
            files_ok = False
            
        if debug_file.exists():
            size = debug_file.stat().st_size
            print(f"✅ Archivo debug: {debug_file} ({size} bytes)")
        else:
            print(f"⚠️ Archivo debug no encontrado: {debug_file}")
            files_ok = False
        
        return files_ok
        
    except Exception as e:
        print(f"❌ Error verificando archivos: {e}")
        return False

def test_logging_production():
    """Prueba de configuración de producción"""
    print("\n=== PRUEBA DE CONFIGURACIÓN DE PRODUCCIÓN ===")
    
    try:
        from log import setup_production_logging
        import logging
        
        # Limpiar logging anterior
        logging.shutdown()
        
        logger = setup_production_logging()
        logger.info("Configuración de producción activada")
        logger.warning("Test de warning en producción")
        logger.error("Test de error en producción")
        
        print("✅ Configuración de producción funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de producción: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("INICIANDO PRUEBAS DEL SISTEMA DE LOGGING")
    print("=" * 50)
    
    tests = [
        test_logging_basic,
        test_logging_performance, 
        test_logging_database_simulation,
        test_logging_files,
        test_logging_production
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error ejecutando {test.__name__}: {e}")
            results.append(False)
    
    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE PRUEBAS")
    passed = sum(results)
    total = len(results)
    print(f"Pruebas exitosas: {passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema de logging está funcionando correctamente.")
    else:
        print(f"⚠️ {total - passed} pruebas fallaron. Revisar la configuración.")
    
    print(f"\nArchivos de log generados:")
    print(f"- nc_ac_faben.log (principal)")
    print(f"- nc_ac_faben_debug.log (debug/errores)")

if __name__ == '__main__':
    main()