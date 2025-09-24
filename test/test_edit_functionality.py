#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de edición de registros
"""

import sqlite3
import sys
from pathlib import Path

def test_edit_functionality():
    """Prueba la funcionalidad de edición de registros"""
    
    DB_FILE = Path.cwd() / 'nc_ac_faben.db'
    
    if not DB_FILE.exists():
        print("❌ Error: Base de datos no encontrada")
        return False
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        
        # Verificar si hay registros
        cur.execute("SELECT COUNT(*) FROM nc")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("⚠️  La base de datos está vacía. Agregando registro de prueba...")
            
            # Insertar registro de prueba
            cur.execute('''INSERT INTO nc 
                          (nro_nc, fecha, resultado_matriz, op, cant_invol, cod_producto, 
                           desc_producto, cliente, cant_scrap, costo, cant_recuperada, 
                           observaciones, falla, ishikawa) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (9999, '2024-12-24', 5.0, 12345, 100.0, 'TEST001', 
                        'Producto de Prueba', 'Cliente Test', 10.0, 500.0, 90.0,
                        'Registro de prueba para testing', 'Falla de prueba', 'Ishikawa test'))
            conn.commit()
            print("✅ Registro de prueba agregado (NC 9999)")
        
        # Listar algunos registros disponibles
        print("\n📋 Registros disponibles para prueba:")
        cur.execute("SELECT nro_nc, desc_producto, cliente FROM nc LIMIT 5")
        registros = cur.fetchall()
        
        for nro_nc, desc, cliente in registros:
            print(f"   • NC {nro_nc}: {desc} - {cliente}")
        
        # Probar búsqueda de registro específico
        test_nc = registros[0][0] if registros else 9999
        
        print(f"\n🔍 Probando búsqueda de NC {test_nc}:")
        cur.execute("SELECT * FROM nc WHERE nro_nc=?", (test_nc,))
        row = cur.fetchone()
        
        if row:
            print("✅ Registro encontrado exitosamente")
            print("📊 Estructura de datos:")
            
            # Mapeo de índices a nombres de campos
            field_names = ['id', 'nro_nc', 'fecha', 'resultado_matriz', 'op', 'cant_invol', 
                          'cod_producto', 'desc_producto', 'cliente', 'cant_scrap', 'costo', 
                          'cant_recuperada', 'observaciones', 'falla', 'ishikawa']
            
            for i, (field_name, value) in enumerate(zip(field_names, row)):
                print(f"   [{i}] {field_name}: {value}")
            
            # Simular el mapeo que hace el código
            print("\n🔧 Simulando mapeo de campos para edición:")
            enable_chain_order = ['Nro NC','Resultado Matriz','OP','Cant. Invol.','Cod. Producto',
                                 'Desc. Producto','Cliente','Cant. Scrap','Costo','Cant. Recuperada','Falla']
            
            # El código hace: for idx, name in enumerate(self.enable_chain_order[1:], 1):
            # Y luego: w.setText(str(row[idx+2]))
            
            print("   Campos que se cargarían:")
            for idx, name in enumerate(enable_chain_order[1:], 1):  # Empieza en 1, salta 'Nro NC'
                db_index = idx + 1  # El código actual usa idx+2, pero debería ser idx+1
                if db_index < len(row):
                    print(f"   • {name}: row[{db_index}] = {row[db_index]}")
                else:
                    print(f"   ❌ {name}: ÍNDICE FUERA DE RANGO (row[{db_index}])")
            
            return True
        else:
            print("❌ No se encontró el registro")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False
    finally:
        conn.close()

def fix_edit_mapping():
    """Analiza el problema de mapeo en la función de edición"""
    print("\n🔧 ANÁLISIS DEL PROBLEMA DE EDICIÓN:")
    print("\n📋 Estructura de tabla NC:")
    print("   [0] id (PK)")
    print("   [1] nro_nc")
    print("   [2] fecha") 
    print("   [3] resultado_matriz")
    print("   [4] op")
    print("   [5] cant_invol")
    print("   [6] cod_producto")
    print("   [7] desc_producto")
    print("   [8] cliente")
    print("   [9] cant_scrap")
    print("   [10] costo")
    print("   [11] cant_recuperada")
    print("   [12] observaciones")
    print("   [13] falla")
    print("   [14] ishikawa")
    
    print("\n📋 Orden de campos en enable_chain_order:")
    enable_chain_order = ['Nro NC','Resultado Matriz','OP','Cant. Invol.','Cod. Producto',
                         'Desc. Producto','Cliente','Cant. Scrap','Costo','Cant. Recuperada','Falla']
    
    for i, field in enumerate(enable_chain_order):
        print(f"   [{i}] {field}")
    
    print("\n🔧 Mapeo CORRECTO que debería usarse:")
    print("   Campo en UI -> Índice DB correcto")
    
    # Mapeo correcto: enable_chain_order[1:] corresponde a row[2:]
    db_mapping = {
        'Resultado Matriz': 3,  # resultado_matriz  
        'OP': 4,               # op
        'Cant. Invol.': 5,     # cant_invol
        'Cod. Producto': 6,    # cod_producto
        'Desc. Producto': 7,   # desc_producto
        'Cliente': 8,          # cliente
        'Cant. Scrap': 9,      # cant_scrap
        'Costo': 10,           # costo
        'Cant. Recuperada': 11, # cant_recuperada
        'Falla': 13            # falla (salta observaciones e ishikawa)
    }
    
    for idx, name in enumerate(enable_chain_order[1:], 0):  # idx empieza en 0
        correct_db_idx = db_mapping.get(name, "NO MAPEADO")
        current_wrong_idx = idx + 3  # Lo que hace el código actual (idx+2 pero idx empieza en 1)
        should_be_idx = idx + 3 if idx < 9 else (13 if idx == 9 else "PROBLEMA")
        
        print(f"   • {name}:")
        print(f"     - Código actual: row[{current_wrong_idx}] ❌")  
        print(f"     - Debería ser: row[{correct_db_idx}] ✅")
    
    print(f"\n⚠️  PROBLEMA IDENTIFICADO:")
    print(f"   • El código actual usa 'row[idx+2]' donde idx empieza en 1")
    print(f"   • Esto genera índices incorrectos")  
    print(f"   • Solución: Usar mapeo directo por nombre de campo")

if __name__ == "__main__":
    print("🧪 PRUEBA DE FUNCIONALIDAD DE EDICIÓN DE REGISTROS\n")
    
    # Probar funcionalidad básica
    success = test_edit_functionality()
    
    # Analizar el problema de mapeo
    fix_edit_mapping()
    
    if success:
        print("\n✅ La funcionalidad básica de búsqueda funciona")
        print("⚠️  Sin embargo, hay un problema en el mapeo de campos")
        print("📝 Se requiere corrección en las funciones edit_record() y edit_record_by_number()")
    else:
        print("\n❌ Hay problemas con la funcionalidad básica")
    
    print("\n" + "="*60)
    print("RECOMENDACIONES:")
    print("1. Corregir el mapeo de índices en funciones de edición")  
    print("2. Usar mapeo directo por nombre de campo en lugar de índices")
    print("3. Agregar manejo de campos faltantes (observaciones, ishikawa)")
    print("4. Probar con registros reales después de las correcciones")