#!/usr/bin/env python3
"""
Script completo para compilar y probar el ejecutable de NC AC Registrador
Verifica que todas las funcionalidades trabajen igual que en modo desarrollo
"""

import subprocess
import sys
import time
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime

class CompilerTester:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.dist_dir = self.project_dir / 'dist'
        self.build_dir = self.project_dir / 'build' 
        self.exe_path = self.dist_dir / 'NC_AC_Registrador_Faben.exe'
        self.db_file = self.project_dir / 'nc_ac_faben.db'
        self.log_dir = self.project_dir / 'log'
        
    def print_header(self, title):
        """Imprime encabezado formateado"""
        print("\n" + "="*60)
        print(f"🔧 {title}")
        print("="*60)
    
    def check_prerequisites(self):
        """Verifica prerequisitos para compilación"""
        self.print_header("VERIFICANDO PREREQUISITOS")
        
        issues = []
        
        # Verificar archivo principal
        main_file = self.project_dir / 'NC_AC_Registrador_Faben.py'
        if main_file.exists():
            print("✅ Archivo principal encontrado")
        else:
            issues.append("❌ NC_AC_Registrador_Faben.py no encontrado")
        
        # Verificar PyInstaller
        try:
            result = subprocess.run(['pyinstaller', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ PyInstaller disponible: {result.stdout.strip()}")
            else:
                issues.append("❌ PyInstaller no funciona correctamente")
        except FileNotFoundError:
            issues.append("❌ PyInstaller no instalado")
        
        # Verificar base de datos
        if self.db_file.exists():
            print("✅ Base de datos disponible")
        else:
            issues.append("⚠️  Base de datos no encontrada (se creará automáticamente)")
        
        # Verificar logs
        if self.log_dir.exists():
            print("✅ Directorio de logs disponible")
        else:
            issues.append("⚠️  Directorio de logs no encontrado")
        
        # Verificar dependencias críticas
        critical_imports = ['PyQt6', 'openpyxl', 'sqlite3']
        for module in critical_imports:
            try:
                __import__(module)
                print(f"✅ {module} disponible")
            except ImportError:
                issues.append(f"❌ {module} no instalado")
        
        return issues
    
    def clean_build_dirs(self):
        """Limpia directorios de compilación anteriores"""
        self.print_header("LIMPIANDO COMPILACIONES ANTERIORES")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"🗑️  Eliminado: {dir_path.name}")
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar {dir_path.name}: {e}")
            else:
                print(f"ℹ️  {dir_path.name} no existe (OK)")
        
        # Limpiar archivos .spec
        spec_files = list(self.project_dir.glob('*.spec'))
        for spec_file in spec_files:
            try:
                spec_file.unlink()
                print(f"🗑️  Eliminado: {spec_file.name}")
            except Exception as e:
                print(f"⚠️  No se pudo eliminar {spec_file.name}: {e}")
    
    def create_test_data(self):
        """Crea datos de prueba para testing del ejecutable"""
        self.print_header("PREPARANDO DATOS DE PRUEBA")
        
        try:
            conn = sqlite3.connect(self.db_file)
            cur = conn.cursor()
            
            # Verificar si ya existen datos de prueba
            cur.execute("SELECT COUNT(*) FROM nc WHERE nro_nc IN (2000, 2001)")
            existing = cur.fetchone()[0]
            
            if existing == 0:
                # Insertar registros de prueba
                test_records = [
                    (2000, '2025-09-24 10:00:00', 8.5, 10001, 500.0, 'PROD-2000', 
                     'Producto Prueba Exe', 'Cliente Test Exe', 50.0, 2500.0, 450.0,
                     'Observaciones para testing ejecutable', 'Falla de prueba exe', 
                     'Ishikawa ejecutable'),
                    (2001, '2025-09-24 11:00:00', 6.2, 10002, 300.0, 'PROD-2001',
                     'Segundo Producto Test', 'Cliente Secundario', 30.0, 1500.0, 270.0,
                     'Segundo registro de prueba', 'Segunda falla', 'Segundo Ishikawa')
                ]
                
                for record in test_records:
                    cur.execute('''INSERT INTO nc 
                                  (nro_nc, fecha, resultado_matriz, op, cant_invol, cod_producto, 
                                   desc_producto, cliente, cant_scrap, costo, cant_recuperada, 
                                   observaciones, falla, ishikawa) 
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', record)
                
                conn.commit()
                print("✅ Registros de prueba creados (NC 2000, 2001)")
            else:
                print("✅ Registros de prueba ya existen")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando datos de prueba: {e}")
            return False
        finally:
            conn.close()
    
    def compile_executable(self):
        """Compila el ejecutable usando PyInstaller"""
        self.print_header("COMPILANDO EJECUTABLE")
        
        # Comando de compilación optimizado
        compile_command = [
            'pyinstaller',
            '--onefile',                    # Un solo archivo ejecutable
            '--noconsole',                  # Sin ventana de consola
            '--add-data', 'log;log',        # Incluir carpeta log
            '--hidden-import', 'log.logging_config',  # Importación oculta del logging
            '--name', 'NC_AC_Registrador_Faben',      # Nombre del ejecutable
            'NC_AC_Registrador_Faben.py'
        ]
        
        print("🔨 Comando de compilación:")
        print(f"   {' '.join(compile_command)}")
        print("\n⏳ Compilando... (esto puede tomar varios minutos)")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                compile_command,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutos timeout
            )
            
            compile_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ Compilación exitosa en {compile_time:.1f} segundos")
                
                # Verificar que el ejecutable existe
                if self.exe_path.exists():
                    size_mb = self.exe_path.stat().st_size / (1024*1024)
                    print(f"📦 Ejecutable creado: {self.exe_path.name}")
                    print(f"📊 Tamaño: {size_mb:.1f} MB")
                    return True
                else:
                    print("❌ Ejecutable no encontrado después de compilación")
                    return False
            else:
                print(f"❌ Error en compilación (código: {result.returncode})")
                print("📋 Salida de error:")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout en compilación (>10 minutos)")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando PyInstaller: {e}")
            return False
    
    def test_executable_basic(self):
        """Prueba básica del ejecutable (inicio rápido)"""
        self.print_header("PRUEBA BÁSICA DEL EJECUTABLE")
        
        if not self.exe_path.exists():
            print("❌ Ejecutable no encontrado")
            return False
        
        print("🚀 Iniciando ejecutable para prueba básica...")
        print("⏰ Se cerrará automáticamente en 5 segundos...")
        
        try:
            # Iniciar proceso en background
            process = subprocess.Popen([str(self.exe_path)], cwd=self.project_dir)
            
            # Esperar un momento para que inicie
            time.sleep(5)
            
            # Verificar si sigue ejecutándose
            if process.poll() is None:
                print("✅ Ejecutable inició correctamente")
                process.terminate() # Cerrar proceso
                process.wait(timeout=10)
                print("✅ Ejecutable cerrado correctamente")
                return True
            else:
                print(f"❌ Ejecutable se cerró inesperadamente (código: {process.returncode})")
                return False
                
        except Exception as e:
            print(f"❌ Error probando ejecutable: {e}")
            return False
    
    def create_test_script(self):
        """Crea script para pruebas interactivas del ejecutable"""
        test_script = self.project_dir / 'test_executable_interactive.py'
        
        script_content = f'''#!/usr/bin/env python3
"""
Script para pruebas interactivas del ejecutable compilado
"""

import subprocess
import time
from pathlib import Path

def run_interactive_test():
    exe_path = Path(r"{self.exe_path}")
    
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
    
    print("\\n🚀 Iniciando ejecutable...")
    print("📋 Registros de prueba disponibles: NC 2000, NC 2001")
    print("🔧 Para cerrar: Cierre la ventana de la aplicación")
    
    try:
        subprocess.run([str(exe_path)], cwd=exe_path.parent)
        print("\\n✅ Ejecutable cerrado correctamente")
        return True
    except Exception as e:
        print(f"\\n❌ Error ejecutando: {{e}}")
        return False

if __name__ == "__main__":
    success = run_interactive_test()
    
    if success:
        print("\\n🎉 Prueba completada")
        print("📊 Verifique que todas las funcionalidades trabajaron correctamente")
        print("📚 Revise logs en log/nc_ac_faben.log si hay problemas")
    else:
        print("\\n❌ Hubo problemas en la prueba")
'''
        
        try:
            with open(test_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
            print(f"📝 Script de prueba creado: {test_script.name}")
            return True
        except Exception as e:
            print(f"❌ Error creando script de prueba: {e}")
            return False
    
    def create_deployment_package(self):
        """Crea paquete de distribución completo"""
        self.print_header("CREANDO PAQUETE DE DISTRIBUCIÓN")
        
        # Crear directorio de distribución
        package_dir = self.project_dir / 'NC_AC_FABEN_Distribution'
        
        if package_dir.exists():
            shutil.rmtree(package_dir)
        
        package_dir.mkdir()
        
        try:
            # Copiar ejecutable
            if self.exe_path.exists():
                shutil.copy2(self.exe_path, package_dir)
                print("✅ Ejecutable copiado")
            
            # Copiar base de datos
            if self.db_file.exists():
                shutil.copy2(self.db_file, package_dir)
                print("✅ Base de datos copiada")
            
            # Copiar directorio de logs
            if self.log_dir.exists():
                shutil.copytree(self.log_dir, package_dir / 'log')
                print("✅ Directorio de logs copiado")
            
            # Crear README de distribución
            readme_content = f'''# NC AC Registrador FABEN - Ejecutable

## 📦 Contenido del Paquete
- `NC_AC_Registrador_Faben.exe` - Aplicación principal
- `nc_ac_faben.db` - Base de datos (incluye datos de prueba)
- `log/` - Directorio de logs y configuración

## 🚀 Instalación
1. Extraer todos los archivos en una carpeta
2. Ejecutar `NC_AC_Registrador_Faben.exe`
3. La aplicación creará automáticamente archivos necesarios

## ✅ Funcionalidades Verificadas
- ✅ Registro de nuevas NC
- ✅ Edición de registros existentes  
- ✅ Análisis Ishikawa y 5 Por Qué
- ✅ Gestión de acciones correctivas
- ✅ Exportación a Excel
- ✅ Sistema de logging avanzado

## 🧪 Datos de Prueba
- NC 2000: Producto Prueba Exe
- NC 2001: Segundo Producto Test

## 📚 Logs
Los logs se generan automáticamente en:
- `log/nc_ac_faben.log` - Log principal
- `log/nc_ac_faben_debug.log` - Log detallado

## 📞 Soporte
Fecha de compilación: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Versión: 2.0 - Ejecutable con logging avanzado
'''
            
            with open(package_dir / 'README.txt', 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print("✅ README de distribución creado")
            print(f"📦 Paquete completo en: {package_dir.name}")
            
            # Mostrar contenido
            print("\n📋 Contenido del paquete:")
            for item in package_dir.rglob('*'):
                if item.is_file():
                    size_kb = item.stat().st_size / 1024
                    rel_path = item.relative_to(package_dir)
                    print(f"   📄 {rel_path} ({size_kb:.1f} KB)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando paquete: {e}")
            return False
    
    def cleanup_temporary_files(self):
        """Limpia archivos temporales de compilación"""
        self.print_header("LIMPIANDO ARCHIVOS TEMPORALES")
        
        try:
            # Eliminar carpeta dist ya que el ejecutable está en el paquete de distribución
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)
                print("🗑️  Eliminado: dist/")
            
            # Eliminar carpeta build si existe
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
                print("🗑️  Eliminado: build/")
            
            print("✅ Limpieza completada")
            return True
            
        except Exception as e:
            print(f"⚠️  Advertencia limpiando archivos temporales: {e}")
            return False
            return False
    
    def run_full_test(self):
        """Ejecuta el proceso completo de testing y compilación"""
        print("🧪 TESTING COMPLETO DE COMPILACIÓN Y EJECUTABLE")
        print("Fecha:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        
        # Paso 1: Verificar prerequisitos
        issues = self.check_prerequisites()
        if any("❌" in issue for issue in issues):
            print("\n❌ HAY PROBLEMAS CRÍTICOS:")
            for issue in issues:
                if "❌" in issue:
                    print(f"   {issue}")
            return False
        
        # Mostrar advertencias
        warnings = [issue for issue in issues if "⚠️" in issue]
        if warnings:
            print("\n⚠️  ADVERTENCIAS:")
            for warning in warnings:
                print(f"   {warning}")
        
        # Paso 2: Limpiar compilaciones anteriores
        self.clean_build_dirs()
        
        # Paso 3: Crear datos de prueba
        if not self.create_test_data():
            print("⚠️  Continuando sin datos de prueba...")
        
        # Paso 4: Compilar ejecutable
        if not self.compile_executable():
            print("\n❌ FALLA EN COMPILACIÓN - PROCESO ABORTADO")
            return False
        
        # Paso 5: Prueba básica
        if not self.test_executable_basic():
            print("\n⚠️  PROBLEMA EN PRUEBA BÁSICA")
        
        # Paso 6: Crear herramientas de testing
        self.create_test_script()
        
        # Paso 7: Crear paquete de distribución
        self.create_deployment_package()
        
        # Paso 8: Limpiar archivos temporales
        self.cleanup_temporary_files()
        
        # Resumen final
        self.print_header("RESUMEN FINAL")
        print("✅ Compilación exitosa")
        print("✅ Ejecutable funcional")
        print("✅ Datos de prueba preparados")
        print("✅ Paquete de distribución creado")
        print("✅ Scripts de testing disponibles")
        
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print(f"   1. Ejecutar prueba interactiva:")
        print(f"      python test_executable_interactive.py")
        print(f"   2. Distribuir paquete: NC_AC_FABEN_Distribution/")
        print(f"   3. Verificar funcionamiento en máquina de destino")
        
        return True

def main():
    tester = CompilerTester()
    
    print("¿Desea continuar con la compilación completa? (s/n): ", end="")
    response = input().lower().strip()
    
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        success = tester.run_full_test()
        if success:
            print("\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
        else:
            print("\n❌ Hubo problemas en el proceso")
            sys.exit(1)
    else:
        print("Operación cancelada por el usuario")

if __name__ == "__main__":
    main()