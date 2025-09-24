# 📁 Directorio de Tests y Verificación

Este directorio contiene todos los scripts de testing y verificación para el proyecto NC_AC_Registrador_Faben.

## 📋 Contenido

### 🔧 Scripts de Compilación y Testing

- **`compile_and_test.py`**: Script principal para compilar el ejecutable usando PyInstaller y ejecutar tests básicos
- **`verify_executable.py`**: Verificación completa del ejecutable compilado (existencia, base de datos, logging, etc.)

### 🧪 Scripts de Testing de Funcionalidad

- **`test_edit_functionality.py`**: Prueba específica de la funcionalidad de edición de registros
- **`test_edit_executable.py`**: Prueba de la funcionalidad de edición en el ejecutable compilado
- **`test_executable_interactive.py`**: Test interactivo del ejecutable con interfaz gráfica
- **`test_logging.py`**: Pruebas del sistema de logging avanzado
- **`probar_edicion_interactiva.py`**: Prueba interactiva específica de edición
- **`verificar_edicion_completa.py`**: Verificación completa del sistema de edición
- **`verificar_sistema.py`**: Verificación general del sistema completo

### 📝 Documentación de Testing

- **`CHECKLIST_EJECUTABLE.md`**: Lista de verificación completa para validar el ejecutable

### 🛠️ Herramientas de Soporte

- **`logging_tools.py`**: Script de conveniencia para ejecutar herramientas de logging

## 🚀 Uso de los Scripts

### Compilar y Probar

```bash
# Compilar ejecutable y ejecutar tests básicos
python test/compile_and_test.py

# Verificar ejecutable completo
python test/verify_executable.py
```

### Probar Funcionalidades Específicas

```bash
# Probar funcionalidad de edición (desarrollo)
python test/test_edit_functionality.py

# Probar funcionalidad de edición (ejecutable)
python test/test_edit_executable.py

# Test interactivo del ejecutable
python test/test_executable_interactive.py

# Probar sistema de logging
python test/test_logging.py

# Pruebas interactivas adicionales
python test/probar_edicion_interactiva.py
python test/verificar_edicion_completa.py
python test/verificar_sistema.py

# Herramientas de logging
python test/logging_tools.py
```

### Checklist Manual

- Revisar `CHECKLIST_EJECUTABLE.md` para verificación manual completa

## 📁 Estructura Recomendada de Ejecución

1. **Durante Desarrollo**: Usar scripts de test individuales para validar cambios
2. **Pre-Compilación**: Ejecutar `test_edit_functionality.py` y `test_logging.py`
3. **Compilación**: Ejecutar `compile_and_test.py`
4. **Post-Compilación**: Ejecutar `verify_executable.py` y revisar `CHECKLIST_EJECUTABLE.md`
5. **Testing Final**: Ejecutar `test_executable_interactive.py` para validación manual

## 📊 Cobertura de Testing

- ✅ **Funcionalidad de Edición**: Validada en desarrollo y ejecutable
- ✅ **Sistema de Logging**: Configuración y funcionamiento
- ✅ **Base de Datos**: Conectividad y operaciones
- ✅ **Interfaz Gráfica**: Lanzamiento y operación básica
- ✅ **Compilación**: Proceso completo y validación
- ✅ **Ejecutable**: Funcionamiento idéntico al desarrollo

---

_Carpeta organizada el 24 de septiembre de 2025_
