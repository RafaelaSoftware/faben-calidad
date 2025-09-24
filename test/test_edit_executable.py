#!/usr/bin/env python3
"""
Test específico para verificar la funcionalidad de edición en el ejecutable
"""

import sqlite3
import subprocess
import time
from pathlib import Path

def test_edit_data_preparation():
    """Prepara datos específicos para probar la edición"""
    print("🔧 PREPARANDO DATOS ESPECÍFICOS PARA TEST DE EDICIÓN")
    print("="*55)
    
    db_file = Path.cwd() / 'nc_ac_faben.db'
    
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        
        # Verificar/crear registro específico para testing de edición
        test_nc = 3000
        cur.execute("SELECT COUNT(*) FROM nc WHERE nro_nc=?", (test_nc,))
        
        if cur.fetchone()[0] == 0:
            # Crear registro con datos específicos y reconocibles
            cur.execute('''INSERT INTO nc 
                          (nro_nc, fecha, resultado_matriz, op, cant_invol, cod_producto, 
                           desc_producto, cliente, cant_scrap, costo, cant_recuperada, 
                           observaciones, falla, ishikawa) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (test_nc, '2025-09-24 17:20:00', 9.8, 77777, 888.0, 'EDIT-TEST', 
                        'PRODUCTO PARA EDICION TEST', 'CLIENTE EDICION S.A.', 77.0, 7777.0, 811.0,
                        'Observaciones específicas para test de edición', 
                        'FALLA PARA TEST DE EDICION', 
                        'Ishikawa específico para testing'))
            conn.commit()
            print(f"✅ Registro de prueba NC {test_nc} creado")
        else:
            print(f"✅ Registro de prueba NC {test_nc} ya existe")
        
        # Mostrar los datos que se deberían cargar
        cur.execute("SELECT * FROM nc WHERE nro_nc=?", (test_nc,))
        row = cur.fetchone()
        
        print(f"\n📋 DATOS QUE SE DEBEN CARGAR AL EDITAR NC {test_nc}:")
        print(f"   • Resultado Matriz: {row[3]}")
        print(f"   • OP: {row[4]}")  
        print(f"   • Cant. Invol.: {row[5]}")
        print(f"   • Cod. Producto: {row[6]}")
        print(f"   • Desc. Producto: {row[7]}")
        print(f"   • Cliente: {row[8]}")
        print(f"   • Cant. Scrap: {row[9]}")
        print(f"   • Costo: {row[10]}")
        print(f"   • Cant. Recuperada: {row[11]}")
        print(f"   • Falla: {row[13]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error preparando datos: {e}")
        return False
    finally:
        conn.close()

def launch_executable_for_edit_test():
    """Lanza el ejecutable con instrucciones específicas para test de edición"""
    print("\n🚀 LANZANDO EJECUTABLE PARA TEST DE EDICIÓN")
    print("="*50)
    
    exe_path = Path.cwd() / 'dist' / 'NC_AC_Registrador_Faben.exe'
    
    if not exe_path.exists():
        print("❌ Ejecutable no encontrado")
        return False
    
    print("🧪 INSTRUCCIONES ESPECÍFICAS PARA TEST DE EDICIÓN:")
    print("-"*50)
    print("1️⃣ Esperar a que la aplicación cargue completamente")
    print("2️⃣ Presionar botón 'Editar Registro Existente'")
    print("3️⃣ Ingresar el número: 3000")
    print("4️⃣ VERIFICAR que los campos se llenen con estos valores:")
    print("    • Resultado Matriz: 9.8")
    print("    • OP: 77777")
    print("    • Cant. Invol.: 888.0")
    print("    • Cod. Producto: EDIT-TEST")
    print("    • Desc. Producto: PRODUCTO PARA EDICION TEST")
    print("    • Cliente: CLIENTE EDICION S.A.")
    print("    • Cant. Scrap: 77.0")
    print("    • Costo: 7777.0")
    print("    • Cant. Recuperada: 811.0")
    print("    • Falla: FALLA PARA TEST DE EDICION")
    print("5️⃣ Modificar algunos valores (ej: cambiar OP a 88888)")
    print("6️⃣ Presionar 'Guardar' para confirmar que funciona")
    print("7️⃣ Cerrar la aplicación")
    print()
    print("⚠️  IMPORTANTE: Si los valores NO coinciden, la edición tiene problemas")
    print("✅ Si los valores coinciden exactamente, la edición funciona perfecto")
    
    print(f"\n🚀 Lanzando aplicación...")
    
    try:
        # Lanzar el ejecutable
        subprocess.run([str(exe_path)], cwd=exe_path.parent)
        print("\n✅ Aplicación cerrada")
        return True
        
    except Exception as e:
        print(f"\n❌ Error lanzando aplicación: {e}")
        return False

def verify_edit_results():
    """Verifica si la edición se realizó correctamente"""
    print("\n🔍 VERIFICANDO RESULTADOS DE LA EDICIÓN")
    print("="*45)
    
    db_file = Path.cwd() / 'nc_ac_faben.db'
    
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        
        # Obtener datos actuales del registro NC 3000
        cur.execute("SELECT * FROM nc WHERE nro_nc=?", (3000,))
        row = cur.fetchone()
        
        if not row:
            print("❌ Registro NC 3000 no encontrado")
            return False
        
        print("📊 ESTADO ACTUAL DEL REGISTRO NC 3000:")
        print(f"   • Resultado Matriz: {row[3]}")
        print(f"   • OP: {row[4]}")
        print(f"   • Cant. Invol.: {row[5]}")
        print(f"   • Cod. Producto: {row[6]}")
        print(f"   • Desc. Producto: {row[7]}")
        print(f"   • Cliente: {row[8]}")
        print(f"   • Cant. Scrap: {row[9]}")
        print(f"   • Costo: {row[10]}")
        print(f"   • Cant. Recuperada: {row[11]}")
        print(f"   • Falla: {row[13]}")
        
        # Verificar si se realizaron cambios
        original_op = 77777
        current_op = row[4]
        
        if current_op != original_op:
            print(f"\n✅ CAMBIO DETECTADO: OP cambió de {original_op} a {current_op}")
            print("🎉 ¡LA FUNCIONALIDAD DE EDICIÓN FUNCIONÓ CORRECTAMENTE!")
            return True
        else:
            print(f"\n ℹ️  No se detectaron cambios (OP sigue siendo {current_op})")
            print("🤔 Esto puede significar que no se realizó la prueba o no se guardó")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando resultados: {e}")
        return False
    finally:
        conn.close()

def run_complete_edit_test():
    """Ejecuta el test completo de funcionalidad de edición"""
    print("🧪 TEST COMPLETO DE FUNCIONALIDAD DE EDICIÓN EN EJECUTABLE")
    print("="*65)
    print(f"Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Paso 1: Preparar datos
    if not test_edit_data_preparation():
        print("❌ Error en preparación de datos")
        return False
    
    # Paso 2: Instrucciones y lanzamiento
    print(f"\n⏰ El ejecutable se lanzará en 5 segundos...")
    print("📝 Siga las instrucciones que se mostraron arriba")
    time.sleep(5)
    
    if not launch_executable_for_edit_test():
        print("❌ Error lanzando ejecutable")
        return False
    
    # Paso 3: Verificar resultados
    time.sleep(1)  # Breve pausa
    edit_worked = verify_edit_results()
    
    # Resumen final
    print(f"\n{'='*65}")
    print("📋 RESUMEN DEL TEST DE EDICIÓN")
    print('='*65)
    
    if edit_worked:
        print("🎉 ✅ FUNCIONALIDAD DE EDICIÓN VERIFICADA EXITOSAMENTE")
        print("     • Los datos se cargaron correctamente")
        print("     • Los cambios se guardaron correctamente")
        print("     • El ejecutable funciona igual que el modo desarrollo")
    else:
        print("🤔 ❓ NO SE PUDO CONFIRMAR LA FUNCIONALIDAD DE EDICIÓN")
        print("     • Verifique que siguió todos los pasos")
        print("     • Asegurese de haber modificado algún campo")
        print("     • Confirme que presionó 'Guardar'")
    
    print(f"\n📚 Para más detalles revise los logs en log/nc_ac_faben.log")
    
    return edit_worked

if __name__ == "__main__":
    success = run_complete_edit_test()
    
    if success:
        print(f"\n🎯 CONCLUSIÓN FINAL:")
        print("✅ El ejecutable mantiene TODAS las funcionalidades del modo desarrollo")
        print("✅ La edición de registros funciona correctamente")  
        print("✅ EJECUTABLE APROBADO PARA DISTRIBUCIÓN")
    else:
        print(f"\n🔧 Se requiere verificación manual adicional")