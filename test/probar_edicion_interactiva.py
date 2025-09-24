#!/usr/bin/env python3
"""
Prueba interactiva de la funcionalidad de edición
Ejecuta el programa y verifica que la edición funcione correctamente
"""

import subprocess
import time
import sqlite3
from pathlib import Path

def show_available_records():
    """Muestra registros disponibles para probar la edición"""
    DB_FILE = Path.cwd() / 'nc_ac_faben.db'
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        
        cur.execute("SELECT nro_nc, desc_producto, cliente FROM nc ORDER BY nro_nc LIMIT 10")
        records = cur.fetchall()
        
        print("📋 REGISTROS DISPONIBLES PARA EDICIÓN:")
        print("="*50)
        
        if not records:
            print("   ⚠️  No hay registros en la base de datos")
            return []
        
        for nro_nc, desc, cliente in records:
            print(f"   • NC {nro_nc}: {desc} - {cliente}")
        
        print(f"\n💡 INSTRUCCIONES PARA PROBAR EDICIÓN:")
        print(f"   1. El programa se abrirá automáticamente")
        print(f"   2. Presionar botón 'Editar Registro Existente'")
        print(f"   3. Ingresar cualquiera de los números NC mostrados arriba")
        print(f"   4. Verificar que los campos se llenen correctamente")
        print(f"   5. Modificar algunos valores y guardar")
        
        return [record[0] for record in records]
        
    except Exception as e:
        print(f"❌ Error mostrando registros: {e}")
        return []
    finally:
        conn.close()

def launch_test():
    """Lanza el programa para prueba interactiva"""
    print("\n🚀 LANZANDO PROGRAMA PARA PRUEBA DE EDICIÓN")
    print("="*50)
    
    # Mostrar registros disponibles
    available_ncs = show_available_records()
    
    if not available_ncs:
        print("❌ No hay registros para probar. Creando uno...")
        # El script anterior ya creó NC 1000
        available_ncs = [1000]
    
    print(f"\n⏰ Iniciando programa en 3 segundos...")
    time.sleep(3)
    
    try:
        print(f"▶️  Ejecutando NC_AC_Registrador_Faben.py...")
        print(f"📝 RECUERDE: Probar con NC: {', '.join(map(str, available_ncs))}")
        print(f"🔧 Para cerrar el programa, cierre la ventana\n")
        
        # Ejecutar el programa
        subprocess.run([
            "python", 
            "NC_AC_Registrador_Faben.py"
        ], cwd=Path.cwd())
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Programa interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando programa: {e}")

if __name__ == "__main__":
    print("🧪 PRUEBA INTERACTIVA DE FUNCIONALIDAD DE EDICIÓN")
    print("="*60)
    
    launch_test()
    
    print(f"\n✅ Prueba completada")
    print(f"📊 Si la edición funcionó correctamente:")
    print(f"   • Los campos se llenaron con datos del registro")
    print(f"   • Pudo modificar valores")
    print(f"   • El guardado funcionó sin errores")
    print(f"📚 Revise los logs en log/nc_ac_faben.log para detalles")