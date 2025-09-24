#!/usr/bin/env python3
"""
Script para pruebas interactivas del ejecutable compilado
"""

import subprocess
import time
from pathlib import Path

def run_interactive_test():
    exe_path = Path(r"C:\Datos\Trabajo\FABEN\NC_AC_FABEN\dist\NC_AC_Registrador_Faben.exe")
    
    if not exe_path.exists():
        print("❌ Ejecutable no encontrado")
        return False
    
    print("🧪 PRUEBA INTERACTIVA DEL EJECUTABLE")
    print("="*50)
    print("📝 FUNCIONALIDADES A PROBAR:")
    print("   1. ✅ Apertura de la aplicación")
    print("   2. ✅ Ingreso de nuevo registro")
    print("   3. ✅ Edición de registro existente (NC 2000 o 2001)")
    print("   4. ✅ Ishikawa y 5 Por Qué")
    print("   5. ✅ Acciones correctivas")
    print("   6. ✅ Guardar registro")
    print("   7. ✅ Exportar a Excel")
    print("   8. ✅ Verificar logs")
    
    print("\n🚀 Iniciando ejecutable...")
    print("📋 Registros de prueba disponibles: NC 2000, NC 2001")
    print("🔧 Para cerrar: Cierre la ventana de la aplicación")
    
    try:
        subprocess.run([str(exe_path)], cwd=exe_path.parent)
        print("\n✅ Ejecutable cerrado correctamente")
        return True
    except Exception as e:
        print(f"\n❌ Error ejecutando: {e}")
        return False

if __name__ == "__main__":
    success = run_interactive_test()
    
    if success:
        print("\n🎉 Prueba completada")
        print("📊 Verifique que todas las funcionalidades trabajaron correctamente")
        print("📚 Revise logs en log/nc_ac_faben.log si hay problemas")
    else:
        print("\n❌ Hubo problemas en la prueba")
