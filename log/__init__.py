#!/usr/bin/env python3
"""
Paquete de logging para NC AC FABEN
Contiene todas las utilidades relacionadas con logging y gestión de registros
"""

from .logging_config import (
    setup_development_logging,
    setup_production_logging,
    setup_debug_logging,
    log_performance,
    get_module_logger,
    mask_sensitive_data
)

__version__ = "1.0.0"
__author__ = "FABEN IT"

# Exportar funciones principales
__all__ = [
    'setup_development_logging',
    'setup_production_logging', 
    'setup_debug_logging',
    'log_performance',
    'get_module_logger',
    'mask_sensitive_data'
]