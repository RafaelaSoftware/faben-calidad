#!/usr/bin/env python3
"""
Configuración de logging para NC AC FABEN
Módulo independiente para manejo de logs con diferentes niveles y formatos
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime

class LoggingConfig:
    """Configurador de sistema de logging para la aplicación"""
    
    def __init__(self, 
                 log_level=logging.INFO,
                 console_output=True,
                 file_output=True,
                 max_file_size_mb=10,
                 backup_count=5):
        
        self.log_level = log_level
        self.console_output = console_output
        self.file_output = file_output
        self.max_file_size_mb = max_file_size_mb
        self.backup_count = backup_count
        
        # Determinar el directorio de logs
        if Path.cwd().name == 'log':
            # Si estamos ejecutando desde la carpeta log
            self.log_file = Path.cwd() / 'nc_ac_faben.log'
            self.debug_file = Path.cwd() / 'nc_ac_faben_debug.log'
        else:
            # Si estamos ejecutando desde la carpeta raíz
            log_dir = Path.cwd() / 'log'
            log_dir.mkdir(exist_ok=True)
            self.log_file = log_dir / 'nc_ac_faben.log'
            self.debug_file = log_dir / 'nc_ac_faben_debug.log'
        
    def setup_logging(self):
        """Configurar el sistema de logging"""
        # Configuración del logger principal
        logger = logging.getLogger()
        logger.setLevel(self.log_level)
        
        # Limpiar handlers existentes
        logger.handlers.clear()
        
        # Formato para logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        
        # Formato simplificado para consola
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # Handler para archivo principal con rotación
        if self.file_output:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_file_size_mb * 1024 * 1024,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # Handler separado para debug (solo errores y debug)
            debug_handler = logging.handlers.RotatingFileHandler(
                self.debug_file,
                maxBytes=self.max_file_size_mb * 1024 * 1024,
                backupCount=self.backup_count,
                encoding='utf-8'
            )
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(formatter)
            
            # Filtro para capturar solo DEBUG, WARNING, ERROR y CRITICAL
            class DebugFilter(logging.Filter):
                def filter(self, record):
                    return record.levelno in [logging.DEBUG, logging.WARNING, 
                                            logging.ERROR, logging.CRITICAL]
            
            debug_handler.addFilter(DebugFilter())
            logger.addHandler(debug_handler)
        
        # Handler para consola
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.WARNING)  # Solo warnings y errores en consola
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # Log inicial
        logger.info("=== SISTEMA DE LOGGING INICIALIZADO ===")
        logger.info(f"Nivel de log: {logging.getLevelName(self.log_level)}")
        logger.info(f"Archivo principal: {self.log_file}")
        logger.info(f"Archivo debug: {self.debug_file}")
        
        return logger

def setup_production_logging():
    """Configuración optimizada para producción"""
    config = LoggingConfig(
        log_level=logging.INFO,
        console_output=False,
        file_output=True,
        max_file_size_mb=5,
        backup_count=3
    )
    return config.setup_logging()

def setup_development_logging():
    """Configuración optimizada para desarrollo"""
    config = LoggingConfig(
        log_level=logging.DEBUG,
        console_output=True,
        file_output=True,
        max_file_size_mb=10,
        backup_count=5
    )
    return config.setup_logging()

def setup_debug_logging():
    """Configuración para debugging intensivo"""
    config = LoggingConfig(
        log_level=logging.DEBUG,
        console_output=True,
        file_output=True,
        max_file_size_mb=20,
        backup_count=10
    )
    return config.setup_logging()

# Función de utilidad para logging de performance
def log_performance(func):
    """Decorador para medir tiempo de ejecución de funciones y métodos"""
    import functools
    import time
    import inspect
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Determinar si es un método de clase o una función
        is_method = len(args) > 0 and hasattr(args[0].__class__, func.__name__)
        if is_method:
            logger = logging.getLogger(args[0].__class__.__module__)
            func_name = f"{args[0].__class__.__name__}.{func.__name__}"
        else:
            logger = logging.getLogger(func.__module__)
            func_name = func.__name__
            
        start_time = time.time()
        
        try:
            logger.debug(f"Iniciando ejecución de {func_name}")
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"{func_name} ejecutada en {execution_time:.3f}s")
            return result
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"Error en {func_name} después de {execution_time:.3f}s: {e}")
            raise
            
    return wrapper

# Configuración de logging específica por módulos
def get_module_logger(module_name, level=None):
    """Obtener logger específico para un módulo"""
    logger = logging.getLogger(module_name)
    if level:
        logger.setLevel(level)
    return logger

# Utilidad para logging de datos sensibles (enmascaramiento)
def mask_sensitive_data(data_dict, sensitive_keys=['password', 'token', 'key']):
    """Enmascarar datos sensibles para logging seguro"""
    masked = data_dict.copy()
    for key in sensitive_keys:
        if key in masked:
            masked[key] = '*' * 8
    return masked

if __name__ == '__main__':
    # Ejemplo de uso
    print("Probando configuraciones de logging...")
    
    # Desarrollo
    logger = setup_development_logging()
    logger.info("Test de logging en modo desarrollo")
    logger.warning("Test de warning")
    logger.error("Test de error")
    
    # Limpiar para siguiente test
    logging.shutdown()
    
    print("Configuraciones de logging disponibles:")
    print("- setup_production_logging(): Para producción")
    print("- setup_development_logging(): Para desarrollo") 
    print("- setup_debug_logging(): Para debugging intensivo")