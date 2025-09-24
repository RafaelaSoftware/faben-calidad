# NC AC Registrador FABEN

## Descripción

Sistema de registro y gestión de No Conformidades (NC) y Acciones Correctivas para FABEN. Esta aplicación permite el registro completo de no conformidades, análisis causa-raíz mediante diagramas de Ishikawa y metodología "5 Por qué", gestión de acciones correctivas, y exportación de datos.

## Características Principales

### 📋 Gestión de No Conformidades

- **Registro completo**: Número de NC, fecha, datos del producto, cliente, costos
- **Control de calidad**: Resultado de matriz, cantidad involucrada, scrap y recuperada
- **Seguimiento**: Observaciones detalladas y clasificación de fallas

### 🔍 Análisis Causa-Raíz

- **Diagrama de Ishikawa**: Análisis de 6M (Máquina, Método, Material, Mano de obra, Medio ambiente, Medición)
- **Metodología 5 Por qué**: Análisis profundo de causas mediante preguntas iterativas
- **Integración**: Ambas herramientas se integran automáticamente en el registro

### ⚡ Acciones Correctivas

- **Gestión de tareas**: Descripción, tiempo estimado, responsable
- **Fechas**: Control de fechas de realización
- **Estados**: Seguimiento del progreso (Pendiente, En Proceso, Completada)
- **Adjuntos**: Soporte para archivos relacionados

### 💾 Gestión de Datos

- **Base de datos SQLite**: Almacenamiento local seguro y eficiente
- **Edición**: Modificación de registros existentes
- **Exportación Excel**: Generación de reportes en formato .xlsx
- **Adjuntos**: Sistema de archivos adjuntos organizados

## Estructura del Proyecto

```
NC_AC_FABEN/
├── NC_AC_Registrador_Faben.py    # Aplicación principal
├── logging_tools.py              # Herramientas de logging (punto de entrada)
├── verificar_sistema.py          # Script de verificación completa
├── requirements.txt              # Dependencias Python
├── nc_ac_faben.db               # Base de datos SQLite (se crea automáticamente)
├── export_nc.xlsx               # Archivo de exportación (se genera al exportar)
├── attachments/                 # Carpeta de archivos adjuntos (se crea automáticamente)
├── log/                         # 📁 Paquete de logging
│   ├── __init__.py              #     Inicialización del paquete
│   ├── logging_config.py        #     Sistema de logging avanzado
│   ├── test_logging.py          #     Pruebas del sistema de logging
│   ├── log_manager.py           #     Utilidad de gestión de logs
│   ├── demo_mensajes.py         #     Demostración de mensajes mejorados
│   ├── LOGGING_STATUS.md        #     Estado y documentación del logging
│   ├── nc_ac_faben.log         #     Log principal (se crea automáticamente)
│   ├── nc_ac_faben_debug.log   #     Log de debug (se crea automáticamente)
│   └── log_archives/           #     Carpeta de logs archivados (se crea automáticamente)
└── README.md                    # Este archivo
```

│ ├── log_manager.py # Gestor de archivos de log
│ └── demo_mensajes.py # Demo de mensajes mejorados
├── attachments/ # Carpeta de archivos adjuntos (se crea automáticamente)
├── log_archives/ # Carpeta de logs archivados (se crea automáticamente)
└── README.md # Este archivo

````

## Funciones Principales

### Clase `MainWindow`

- **Interfaz principal**: Gestiona toda la UI y lógica de la aplicación
- **Validación en tiempo real**: Control de campos obligatorios y formato
- **Navegación secuencial**: Los campos se habilitan progresivamente

### Funciones de Base de Datos

- `init_db()`: Inicialización de base de datos y estructura de tablas
- Gestión automática de conexiones SQLite
- Tablas: `nc` (no conformidades) y `acciones` (acciones correctivas)

### Diálogos Especializados

- `IshikawaDialog`: Interfaz para análisis de diagrama de Ishikawa
- `FiveWhysDialog`: Implementación de metodología 5 Por qué
- `ActionDialog`: Gestión de acciones correctivas individuales

## Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- Windows 10/11 (recomendado)

### 1. Crear Entorno Virtual

```powershell
# Navegar al directorio del proyecto
cd "c:\Datos\Trabajo\FABEN\NC_AC_FABEN"

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay problemas de ejecución de políticas, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
````

### 2. Instalar Dependencias

```powershell
# Instalar dependencias desde requirements.txt
pip install -r requirements.txt
```

### 3. Ejecutar en Modo Desarrollo

```powershell
# Con el entorno virtual activado
python NC_AC_Registrador_Faben.py
```

## Compilación y Generación de Ejecutable

### Método 1: PyInstaller Básico

```powershell
# Con el entorno virtual activado
pyinstaller --onefile --windowed NC_AC_Registrador_Faben.py
```

### Método 2: PyInstaller Avanzado (Recomendado)

```powershell
# Crear ejecutable con icono y opciones optimizadas
pyinstaller --onefile --windowed --name="NC_AC_FABEN" --add-data="requirements.txt;." NC_AC_Registrador_Faben.py

# Para debugging (mantiene consola)
pyinstaller --onefile --name="NC_AC_FABEN_Debug" NC_AC_Registrador_Faben.py
```

### Método 3: Con archivo .spec personalizado

```powershell
# Generar archivo spec
pyi-makespec --onefile --windowed NC_AC_Registrador_Faben.py

# Editar NC_AC_Registrador_Faben.spec según necesidades
# Compilar con spec
pyinstaller NC_AC_Registrador_Faben.spec
```

### Ubicación del Ejecutable

El ejecutable se generará en:

```
dist/
├── NC_AC_FABEN.exe    # Ejecutable final
└── ...
```

## Uso de la Aplicación

### Flujo de Trabajo Típico

1. **Inicio**: Ejecutar la aplicación
2. **Nuevo Registro**: Los campos se habilitan secuencialmente
3. **Datos Básicos**: Completar información de la NC
4. **Análisis**:
   - Usar botón "Ishikawa" para análisis de causas
   - Aplicar "5 Por qué" en cada categoría relevante
5. **Acciones**: Definir acciones correctivas con el botón "Acciones"
6. **Adjuntos**: Añadir archivos de soporte si es necesario
7. **Guardar**: Confirmar el registro en la base de datos

### Funciones Avanzadas

#### Edición de Registros

- Usar botón "Editar" e ingresar número de NC
- Modificar campos necesarios y guardar

#### Exportación

- Botón "Exportar" genera archivo Excel con todos los registros
- Archivo se guarda como `export_nc.xlsx`

#### Gestión de Adjuntos

- Los archivos se copian a carpeta `attachments/`
- Se mantiene organización por NC
- Formatos soportados: Todos los tipos de archivo

## Dependencias

### Librerías Python

- **PyQt6**: Interfaz gráfica de usuario
- **pandas**: Manipulación de datos (si es necesaria para futuras funciones)
- **openpyxl**: Generación de archivos Excel
- **sqlite3**: Base de datos (incluida en Python)
- **pathlib**: Manejo de rutas (incluida en Python)

### Para Compilación

- **pyinstaller**: Generación de ejecutables

## Estructura de Base de Datos

### Tabla `nc` (No Conformidades)

```sql
CREATE TABLE nc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nro_nc INTEGER UNIQUE,
    fecha TEXT,
    resultado_matriz REAL,
    op INTEGER,
    cant_invol REAL,
    cod_producto TEXT,
    desc_producto TEXT,
    cliente TEXT,
    cant_scrap REAL,
    costo REAL,
    cant_recuperada REAL,
    observaciones TEXT,
    falla TEXT,
    ishikawa TEXT
);
```

### Tabla `acciones` (Acciones Correctivas)

```sql
CREATE TABLE acciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nc_id INTEGER,
    tarea TEXT,
    tiempo_estimado TEXT,
    responsable TEXT,
    fecha_realizacion TEXT,
    estado TEXT,
    adjuntos TEXT,
    FOREIGN KEY(nc_id) REFERENCES nc(id)
);
```

## Solución de Problemas

### Problemas Comunes

#### Error de Ejecución de Políticas (Windows)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Problemas con PyQt6

```powershell
# Reinstalar PyQt6
pip uninstall pyqt6
pip install pyqt6
```

#### Base de Datos Bloqueada

- Cerrar todas las instancias de la aplicación
- Verificar que no hay procesos Python corriendo
- En casos extremos, eliminar `nc_ac_faben.db` (se perderán datos)

#### Ejecutable no Funciona

- Compilar sin `--windowed` para ver errores
- Verificar que todas las dependencias están incluidas
- Probar en máquina limpia para verificar dependencias del sistema

### Logs y Debugging

Para activar modo debug, modificar el código para incluir:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Desarrollo y Contribución

### Estructura del Código

- **Separación de responsabilidades**: UI, lógica de negocio, y acceso a datos
- **Patrones**: Uso de señales PyQt6 para comunicación entre componentes
- **Validación**: Controles de entrada en tiempo real

### Futuras Mejoras

- [ ] Reportes avanzados con gráficos
- [ ] Integración con sistemas ERP
- [ ] Notificaciones de vencimiento de acciones
- [ ] Firma digital de registros
- [ ] Backup automático de base de datos

## Sistema de Logging

### 📊 Características del Logging

La aplicación incluye un **sistema de logging avanzado** que registra todas las operaciones importantes:

#### Archivos de Log Generados:

- **`nc_ac_faben.log`**: Log principal con operaciones normales (INFO y superior)
- **`nc_ac_faben_debug.log`**: Log de debug con errores y warnings
- **Rotación automática**: Archivos se rotan cuando superan 10MB (hasta 5 respaldos)

#### Eventos Registrados:

- ✅ Inicialización de base de datos y conexiones
- ✅ Guardado y edición de registros NC
- ✅ Exportación a Excel y gestión de archivos
- ✅ Diálogos de Ishikawa y acciones correctivas
- ✅ Adjuntos y operaciones de archivos
- ✅ Tiempo de ejecución de operaciones críticas
- ✅ Errores y excepciones detalladas

### 🔧 Herramientas de Logging

#### Acceso Principal a Herramientas:

```powershell
# Menú unificado de herramientas de logging
python logging_tools.py
```

#### Herramientas Individuales:

```powershell
# Probar sistema de logging
python log/test_logging.py

# Gestionar archivos de log
python log/log_manager.py

# Demo de mensajes mejorados
python log/demo_mensajes.py
```

#### Ver Logs en Tiempo Real:

```powershell
# PowerShell - Log principal (nueva ubicación)
Get-Content log/nc_ac_faben.log -Tail 20 -Wait

# PowerShell - Log de debug (nueva ubicación)
Get-Content log/nc_ac_faben_debug.log -Tail 20 -Wait
Get-Content nc_ac_faben_debug.log -Tail 20 -Wait
```

#### Configuraciones Disponibles:

- **Desarrollo**: Logging completo con consola y archivos
- **Producción**: Solo archivos, sin salida de consola
- **Debug**: Logging intensivo para resolución de problemas

### 📈 Monitoreo y Análisis

El sistema permite:

- **Seguimiento de rendimiento** con medición automática de tiempos
- **Detección de errores** con stack traces completos
- **Auditoría de operaciones** con registro detallado de acciones
- **Análisis de uso** mediante estadísticas de log

## Licencia

Uso interno FABEN - Todos los derechos reservados

## Contacto y Soporte

Para soporte técnico o consultas sobre el sistema, contactar al área de IT de FABEN.

---

**Versión**: 1.0  
**Última actualización**: Septiembre 2025  
**Compatibilidad**: Windows 10/11, Python 3.8+
