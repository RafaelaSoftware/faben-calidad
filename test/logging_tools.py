#!/usr/bin/env python3
"""
Script de conveniencia para ejecutar las herramientas de logging
desde la carpeta principal del proyecto
"""

import sys
from pathlib import Path

# Agregar la carpeta log al path
log_dir = Path(__file__).parent / 'log'
sys.path.insert(0, str(log_dir))

def main():
    """Mostrar menú de herramientas disponibles"""
    print("🔧 HERRAMIENTAS DE LOGGING - NC AC FABEN")
    print("=" * 50)
    print()
    print("Herramientas disponibles:")
    print("1. 🧪 Probar sistema de logging")
    print("2. 📊 Gestionar archivos de log")
    print("3. 💬 Ver demostración de mensajes")
    print("4. ℹ️  Ver estado del logging")
    print("5. 🚪 Salir")
    
    while True:
        try:
            choice = input("\nSeleccione una opción (1-5): ").strip()
            
            if choice == '1':
                print("\n🧪 Ejecutando pruebas de logging...")
                import test_logging
                test_logging.main()
                
            elif choice == '2':
                print("\n📊 Abriendo gestor de logs...")
                import log_manager
                log_manager.main()
                
            elif choice == '3':
                print("\n💬 Mostrando demostración de mensajes...")
                import demo_mensajes
                demo_mensajes.main()
                
            elif choice == '4':
                print("\nℹ️ Estado del logging:")
                status_file = log_dir / 'LOGGING_STATUS.md'
                if status_file.exists():
                    with open(status_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Mostrar solo las primeras 1000 caracteres
                        print(content[:1000])
                        if len(content) > 1000:
                            print("\n... (contenido completo en log/LOGGING_STATUS.md)")
                else:
                    print("❌ No se encontró el archivo de estado")
                
            elif choice == '5':
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción no válida. Intente nuevamente.")
                
        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()