#!/usr/bin/env python3
"""
Utilidad para gestión de archivos de log de NC AC FABEN
Permite limpiar, archivar y rotar logs manualmente
"""

import os
import shutil
import gzip
from datetime import datetime
from pathlib import Path

class LogManager:
    """Gestor de archivos de log"""
    
    def __init__(self):
        # Determinar el directorio de logs
        if Path.cwd().name == 'log':
            # Si estamos ejecutando desde la carpeta log
            self.log_dir = Path.cwd()
        else:
            # Si estamos ejecutando desde la carpeta raíz
            self.log_dir = Path.cwd() / 'log'
            
        self.main_log = self.log_dir / 'nc_ac_faben.log'
        self.debug_log = self.log_dir / 'nc_ac_faben_debug.log'
        self.archive_dir = self.log_dir / 'log_archives'
        
    def list_log_files(self):
        """Listar todos los archivos de log"""
        print("=== ARCHIVOS DE LOG EXISTENTES ===")
        
        log_files = list(self.log_dir.glob('*.log*'))
        
        if not log_files:
            print("No se encontraron archivos de log")
            return []
            
        total_size = 0
        for log_file in sorted(log_files):
            if log_file.exists():
                size = log_file.stat().st_size
                size_mb = size / (1024 * 1024)
                modified = datetime.fromtimestamp(log_file.stat().st_mtime)
                print(f"📄 {log_file.name}: {size_mb:.2f} MB (modificado: {modified.strftime('%Y-%m-%d %H:%M:%S')})")
                total_size += size
        
        total_mb = total_size / (1024 * 1024)
        print(f"\nTamaño total: {total_mb:.2f} MB")
        return log_files
    
    def clean_logs(self, confirm=True):
        """Limpiar todos los archivos de log"""
        if confirm:
            response = input("¿Está seguro de que desea eliminar TODOS los archivos de log? (s/N): ")
            if response.lower() not in ['s', 'si', 'sí', 'yes', 'y']:
                print("Operación cancelada")
                return False
        
        print("Eliminando archivos de log...")
        deleted_count = 0
        
        log_files = list(self.log_dir.glob('*.log*'))
        for log_file in log_files:
            try:
                log_file.unlink()
                print(f"✅ Eliminado: {log_file.name}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Error eliminando {log_file.name}: {e}")
        
        print(f"Se eliminaron {deleted_count} archivos de log")
        return deleted_count > 0
    
    def archive_logs(self):
        """Archivar logs actuales con compresión"""
        self.archive_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archived_count = 0
        
        log_files = [self.main_log, self.debug_log]
        
        for log_file in log_files:
            if log_file.exists():
                # Crear archivo comprimido
                archive_name = f"{log_file.stem}_{timestamp}.log.gz"
                archive_path = self.archive_dir / archive_name
                
                try:
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(archive_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    # Limpiar archivo original
                    log_file.unlink()
                    
                    print(f"✅ Archivado: {log_file.name} -> {archive_name}")
                    archived_count += 1
                    
                except Exception as e:
                    print(f"❌ Error archivando {log_file.name}: {e}")
        
        print(f"Se archivaron {archived_count} archivos en {self.archive_dir}")
        return archived_count > 0
    
    def rotate_logs(self, max_size_mb=10):
        """Rotar logs si superan el tamaño máximo"""
        rotated_count = 0
        
        log_files = [self.main_log, self.debug_log]
        
        for log_file in log_files:
            if log_file.exists():
                size_mb = log_file.stat().st_size / (1024 * 1024)
                
                if size_mb > max_size_mb:
                    print(f"Rotando {log_file.name} ({size_mb:.2f} MB > {max_size_mb} MB)")
                    
                    # Crear backup numerado
                    backup_num = 1
                    while True:
                        backup_path = log_file.parent / f"{log_file.stem}.{backup_num}.log"
                        if not backup_path.exists():
                            break
                        backup_num += 1
                    
                    try:
                        shutil.move(str(log_file), str(backup_path))
                        print(f"✅ Rotado: {log_file.name} -> {backup_path.name}")
                        rotated_count += 1
                    except Exception as e:
                        print(f"❌ Error rotando {log_file.name}: {e}")
        
        if rotated_count == 0:
            print("No es necesario rotar ningún archivo")
        
        return rotated_count > 0
    
    def show_log_tail(self, log_type='main', lines=20):
        """Mostrar las últimas líneas de un log"""
        log_file = self.main_log if log_type == 'main' else self.debug_log
        
        if not log_file.exists():
            print(f"El archivo {log_file.name} no existe")
            return
        
        print(f"=== ÚLTIMAS {lines} LÍNEAS DE {log_file.name} ===")
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                tail_lines = all_lines[-lines:]
                
                for line in tail_lines:
                    print(line.rstrip())
                    
        except Exception as e:
            print(f"Error leyendo {log_file.name}: {e}")
    
    def get_log_stats(self):
        """Obtener estadísticas de los logs"""
        print("=== ESTADÍSTICAS DE LOGS ===")
        
        for log_file in [self.main_log, self.debug_log]:
            if log_file.exists():
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Contar por niveles
                    levels = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0, 'DEBUG': 0}
                    
                    for line in lines:
                        for level in levels:
                            if f' {level} ' in line:
                                levels[level] += 1
                                break
                    
                    print(f"\n📊 {log_file.name}:")
                    print(f"   Total líneas: {len(lines)}")
                    for level, count in levels.items():
                        if count > 0:
                            print(f"   {level}: {count}")
                    
                except Exception as e:
                    print(f"Error analizando {log_file.name}: {e}")

def main():
    """Interfaz de línea de comandos"""
    manager = LogManager()
    
    print("GESTOR DE LOGS - NC AC FABEN")
    print("=" * 40)
    
    while True:
        print("\nOpciones disponibles:")
        print("1. Listar archivos de log")
        print("2. Mostrar estadísticas")
        print("3. Ver últimas líneas (main)")
        print("4. Ver últimas líneas (debug)")
        print("5. Rotar logs grandes")
        print("6. Archivar logs actuales")
        print("7. Limpiar todos los logs")
        print("8. Salir")
        
        try:
            choice = input("\nSeleccione una opción (1-8): ").strip()
            
            if choice == '1':
                manager.list_log_files()
                
            elif choice == '2':
                manager.get_log_stats()
                
            elif choice == '3':
                lines = input("¿Cuántas líneas mostrar? (20): ") or "20"
                manager.show_log_tail('main', int(lines))
                
            elif choice == '4':
                lines = input("¿Cuántas líneas mostrar? (20): ") or "20"
                manager.show_log_tail('debug', int(lines))
                
            elif choice == '5':
                size = input("Tamaño máximo en MB (10): ") or "10"
                manager.rotate_logs(float(size))
                
            elif choice == '6':
                manager.archive_logs()
                
            elif choice == '7':
                manager.clean_logs()
                
            elif choice == '8':
                print("¡Hasta luego!")
                break
                
            else:
                print("Opción no válida")
                
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()