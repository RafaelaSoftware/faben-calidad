#!/usr/bin/env python3
"""
Script de demostración de mejoras en mensajes de error
Muestra los mensajes amigables para diferentes escenarios de error
"""

import sys
from pathlib import Path
import sqlite3

# Añadir el directorio actual al path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def demo_mensajes_error():
    """Demostrar los diferentes tipos de mensajes de error mejorados"""
    
    print("=== DEMOSTRACIÓN DE MENSAJES DE ERROR MEJORADOS ===")
    print("Los siguientes son ejemplos de los mensajes que verá el usuario:\n")
    
    # 1. Error de NC duplicada
    print("1. 📋 ERROR DE NC DUPLICADA:")
    print("   Título: 'NC Duplicada'")
    print("   Mensaje:")
    print("   ❌ Error al guardar:")
    print("   ")
    print("   El número de NC '12345' ya existe en el sistema.")
    print("   ")
    print("   Por favor:")
    print("   • Verifique el número de NC")
    print("   • Use un número diferente")
    print("   • O edite el registro existente")
    print()
    
    # 2. Error de formato de datos
    print("2. 🔢 ERROR DE FORMATO DE DATOS:")
    print("   Título: 'Datos Incorrectos'")
    print("   Mensaje:")
    print("   ❌ Error en los datos ingresados:")
    print("   ")
    print("   Algunos campos contienen valores incorrectos.")
    print("   ")
    print("   Por favor verifique que:")
    print("   • Los números estén en formato correcto")
    print("   • No haya campos vacíos requeridos")
    print("   • Los decimales usen punto (.) no coma (,)")
    print()
    
    # 3. Error general del sistema
    print("3. ⚠️ ERROR GENERAL DEL SISTEMA:")
    print("   Título: 'Error del Sistema'")
    print("   Mensaje:")
    print("   ❌ Error inesperado al guardar:")
    print("   ")
    print("   No se pudo completar la operación.")
    print("   ")
    print("   Por favor:")
    print("   • Verifique todos los campos")
    print("   • Intente nuevamente")
    print("   • Contacte soporte si persiste")
    print("   ")
    print("   Detalle técnico: [Primeros 100 caracteres del error]...")
    print()

def demo_validaciones_previas():
    """Demostrar las validaciones previas implementadas"""
    
    print("=== VALIDACIONES PREVIAS IMPLEMENTADAS ===\n")
    
    print("1. 🆔 VALIDACIÓN DE NÚMERO DE NC:")
    print("   ✅ Verificación de campo vacío")
    print("   ✅ Validación de formato numérico")
    print("   ✅ Detección de duplicados antes del guardado")
    print()
    
    print("2. 🔄 MANEJO DE DUPLICADOS:")
    print("   ✅ Pregunta al usuario qué hacer")
    print("   ✅ Opción de cancelar")
    print("   ✅ Opción de continuar (modo edición)")
    print("   ✅ Conversión automática INSERT → UPDATE")
    print()
    
    print("3. 📝 GESTIÓN DE ACCIONES CORRECTIVAS:")
    print("   ✅ Eliminación de acciones existentes en actualizaciones")
    print("   ✅ Inserción de nuevas acciones")
    print("   ✅ Logging detallado del proceso")
    print()

def demo_mensajes_exito():
    """Demostrar los mensajes de éxito mejorados"""
    
    print("=== MENSAJES DE ÉXITO MEJORADOS ===\n")
    
    print("1. 💾 GUARDADO DE NUEVO REGISTRO:")
    print("   Título: 'Registro Guardado'")
    print("   Mensaje:")
    print("   ✅ NC 12345 guardada correctamente.")
    print("   ")
    print("   El nuevo registro ha sido creado en la base de datos.")
    print()
    
    print("2. ✏️ ACTUALIZACIÓN DE REGISTRO EXISTENTE:")
    print("   Título: 'Registro Actualizado'")
    print("   Mensaje:")
    print("   ✅ NC 12345 actualizada correctamente.")
    print("   ")
    print("   Los cambios han sido guardados en la base de datos.")
    print()

def verificar_base_datos():
    """Verificar que la base de datos tenga datos para demostrar duplicados"""
    
    db_file = Path('nc_ac_faben.db')
    if not db_file.exists():
        print("⚠️ No se encontró la base de datos.")
        print("   Ejecute la aplicación principal primero para crear datos de prueba.")
        return False
    
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM nc")
        count = cur.fetchone()[0]
        
        if count > 0:
            cur.execute("SELECT nro_nc FROM nc LIMIT 3")
            ncs = cur.fetchall()
            print(f"📊 Base de datos contiene {count} registros NC:")
            for nc in ncs:
                print(f"   • NC {nc[0]}")
            print("   (Use uno de estos números para probar el error de duplicado)")
        else:
            print("📊 Base de datos vacía - cree algunos registros primero")
        
        conn.close()
        return count > 0
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def mostrar_comandos_prueba():
    """Mostrar comandos para probar las mejoras"""
    
    print("\n" + "="*60)
    print("CÓMO PROBAR LAS MEJORAS")
    print("="*60)
    
    print("\n🧪 PASOS PARA PROBAR:")
    print("1. Ejecutar: python NC_AC_Registrador_Faben.py")
    print("2. Llenar todos los campos")
    print("3. Usar un número de NC existente (ver lista arriba)")
    print("4. Hacer clic en 'Guardar'")
    print("5. Observar el mensaje amigable de error")
    
    print("\n📝 PRUEBAS ADICIONALES:")
    print("• Dejar campo NC vacío → Ver validación de campo requerido")
    print("• Ingresar texto en NC → Ver validación de formato")
    print("• Ingresar decimales con coma → Ver error de formato")
    print("• Completar guardado exitoso → Ver mensaje de confirmación")
    
    print("\n📊 MONITOREO:")
    print("• Ver logs: Get-Content nc_ac_faben.log -Tail 10")
    print("• Gestionar logs: python log_manager.py")

def main():
    """Ejecutar demostración completa"""
    
    print("DEMOSTRACIÓN DE MEJORAS EN MENSAJES DE ERROR")
    print("=" * 60)
    print(f"Fecha: {Path(__file__).stat().st_mtime}")
    
    # Mostrar ejemplos de mensajes
    demo_mensajes_error()
    demo_validaciones_previas()
    demo_mensajes_exito()
    
    # Verificar base de datos
    print("=== VERIFICACIÓN DE BASE DE DATOS ===")
    verificar_base_datos()
    
    # Instrucciones de prueba
    mostrar_comandos_prueba()
    
    print("\n🎉 MEJORAS IMPLEMENTADAS:")
    print("✅ Mensajes de error más amigables y descriptivos")
    print("✅ Validaciones previas para prevenir errores")
    print("✅ Manejo inteligente de duplicados (INSERT/UPDATE)")
    print("✅ Mensajes de éxito diferenciados")
    print("✅ Logging detallado para debugging")
    
    print("\n💡 Los usuarios ahora ven mensajes claros y útiles")
    print("   en lugar de errores técnicos confusos.")

if __name__ == '__main__':
    main()