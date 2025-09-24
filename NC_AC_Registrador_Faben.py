#!/usr/bin/env python3
"""
NC y Acciones Correctivas - Aplicación completa y segura
Incluye:
- Ingreso de datos
- Ishikawa + 5 Por qué
- Acciones correctivas
- Adjuntos
- Guardar registros seguro
- Editar registros existentes
- Exportar a Excel
"""

import sys, os, sqlite3, shutil, logging
from datetime import datetime
from pathlib import Path
from typing import List
from PyQt6 import QtWidgets, QtCore
from openpyxl import Workbook

# Importar configuración de logging personalizada
LOG_DIR = Path.cwd() / 'log'
LOG_FILE = LOG_DIR / 'nc_ac_faben.log'
DEBUG_LOG_FILE = LOG_DIR / 'nc_ac_faben_debug.log'

try:
    from log import setup_development_logging, log_performance, get_module_logger
    logger = setup_development_logging()
    logger.info("Sistema de logging avanzado cargado exitosamente")
except ImportError:
    # Fallback a configuración básica si no está disponible el paquete log
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.warning("Usando configuración de logging básica (logging_config no disponible)")
    
    # Función dummy para compatibilidad
    def log_performance(func):
        return func

DB_FILE = Path.cwd() / 'nc_ac_faben.db'
ATTACH_DIR = Path.cwd() / 'attachments'

def _is_float(s):
    try:
        float(s)
        return True
    except:
        return False

@log_performance
def init_db():
    try:
        logger.info("Inicializando base de datos y directorios...")
        ATTACH_DIR.mkdir(exist_ok=True)
        logger.info(f"Directorio de adjuntos creado/verificado: {ATTACH_DIR}")
        
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        logger.info(f"Conexión establecida con base de datos: {DB_FILE}")
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS nc (
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
    )''')
        logger.info("Tabla 'nc' creada/verificada exitosamente")
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS acciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nc_id INTEGER,
            tarea TEXT,
            tiempo_estimado TEXT,
            responsable TEXT,
            fecha_realizacion TEXT,
            estado TEXT,
            adjuntos TEXT,
            FOREIGN KEY(nc_id) REFERENCES nc(id)
        )''')
        logger.info("Tabla 'acciones' creada/verificada exitosamente")
        
        conn.commit()
        conn.close()
        logger.info("Base de datos inicializada correctamente")
        
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise

# --- 5 Por qué Dialog ---
class FiveWhysDialog(QtWidgets.QDialog):
    def __init__(self, m_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"5 Por qué - {m_name}")
        self.resize(500,350)
        layout = QtWidgets.QVBoxLayout(self)
        self.edits=[]
        for i in range(5):
            lbl = QtWidgets.QLabel(f"¿Por qué {i+1}?")
            txt = QtWidgets.QTextEdit()
            txt.setFixedHeight(60)
            layout.addWidget(lbl)
            layout.addWidget(txt)
            self.edits.append(txt)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                         QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_answers(self) -> List[str]:
        return [e.toPlainText().strip() for e in self.edits]

# --- Ishikawa Dialog ---
class IshikawaDialog(QtWidgets.QDialog):
    M_OPTIONS = ['Máquina','Método','Material','Mano de obra','Medio ambiente','Medición']
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Diagrama de Ishikawa")
        self.resize(600,400)
        self.selected = {}
        layout = QtWidgets.QVBoxLayout(self)
        lbl = QtWidgets.QLabel("Seleccione M(s) y complete 5 Por qué")
        layout.addWidget(lbl)
        self.checks = {}
        grid = QtWidgets.QGridLayout()
        for i,m in enumerate(self.M_OPTIONS):
            cb = QtWidgets.QCheckBox(m)
            grid.addWidget(cb,i//2,i%2)
            self.checks[m] = cb
        layout.addLayout(grid)
        btn = QtWidgets.QPushButton("Agregar 5 Por qué")
        btn.clicked.connect(self.collect_whys)
        layout.addWidget(btn)
        self.result_area = QtWidgets.QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                         QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def collect_whys(self):
        self.selected = {}
        for m, cb in self.checks.items():
            if cb.isChecked():
                dlg = FiveWhysDialog(m,self)
                if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    self.selected[m] = dlg.get_answers()
        out=[]
        for m,ans in self.selected.items():
            out.append(f"--- {m} ---")
            for i,a in enumerate(ans,1):
                out.append(f"{i}) {a}")
        self.result_area.setPlainText("\n".join(out))

    def get_result(self) -> str:
        parts=[]
        for m,ans in self.selected.items():
            parts.append(f"{m}:|"+"||".join(ans))
        return ";;".join(parts)

# --- Acción Dialog ---
class ActionDialog(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Acción Correctiva")
        self.resize(500,300)
        layout = QtWidgets.QFormLayout(self)
        self.tarea = QtWidgets.QLineEdit()
        self.tiempo = QtWidgets.QLineEdit()
        self.responsable = QtWidgets.QLineEdit()
        self.fecha_realizacion = QtWidgets.QDateEdit()
        self.fecha_realizacion.setCalendarPopup(True)
        self.fecha_realizacion.setDate(QtCore.QDate.currentDate())
        self.estado = QtWidgets.QComboBox()
        self.estado.addItems(['Abierta','En curso','Cerrada'])
        layout.addRow("Tarea",self.tarea)
        layout.addRow("Tiempo estimado",self.tiempo)
        layout.addRow("Responsable",self.responsable)
        layout.addRow("Fecha realización",self.fecha_realizacion)
        layout.addRow("Estado",self.estado)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                         QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_action(self):
        return {
            'tarea': self.tarea.text(),
            'tiempo': self.tiempo.text(),
            'responsable': self.responsable.text(),
            'fecha_realizacion': self.fecha_realizacion.date().toString('yyyy-MM-dd'),
            'estado': self.estado.currentText()
        }

# --- Main Window ---
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Iniciando aplicación principal...")
        
        try:
            self.conn = sqlite3.connect(DB_FILE)
            logger.info("Conexión a base de datos establecida")
        except Exception as e:
            logger.error(f"Error al conectar con la base de datos: {e}")
            raise
            
        self.attached_files=[]
        self.actions_temp=[]
        self.ishikawa_result=''
        self.fields={}
        self.enable_chain_order=['Nro NC','Resultado Matriz','OP','Cant. Invol.','Cod. Producto',
                                 'Desc. Producto','Cliente','Cant. Scrap','Costo','Cant. Recuperada','Falla']
        self.init_ui()
        logger.info("Interfaz de usuario inicializada")

    def init_ui(self):
        self.setWindowTitle("NC y Acciones Correctivas")
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)
        form_frame = QtWidgets.QGroupBox("Ingreso de datos")
        form_layout = QtWidgets.QFormLayout()
        form_frame.setLayout(form_layout)
        main_layout.addWidget(form_frame)

        # Campos
        campo_defs=[('Nro NC',lambda v:v.isdigit()),
                    ('Resultado Matriz',_is_float),
                    ('OP',lambda v:v.isdigit()),
                    ('Cant. Invol.',_is_float),
                    ('Cod. Producto',lambda v:len(v.strip())>0),
                    ('Desc. Producto',lambda v:len(v.strip())>0),
                    ('Cliente',lambda v:len(v.strip())>0),
                    ('Cant. Scrap',_is_float),
                    ('Costo',_is_float),
                    ('Cant. Recuperada',_is_float),
                    ('Falla',lambda v:len(v.strip())>0)]
        for name,val in campo_defs:
            le = QtWidgets.QLineEdit()
            self.add_field(name,le,val,form_layout)

        # Botones
        self.ishikawa_btn = QtWidgets.QPushButton("Abrir Ishikawa")
        self.ishikawa_btn.clicked.connect(self.open_ishikawa)
        self.action_btn = QtWidgets.QPushButton("Agregar Acción Correctiva")
        self.action_btn.clicked.connect(self.open_action)
        self.attach_btn = QtWidgets.QPushButton("Adjuntar archivos")
        self.attach_btn.clicked.connect(self.attach_files)
        self.save_btn = QtWidgets.QPushButton("Guardar registro")
        self.save_btn.clicked.connect(self.save_record)
        self.export_btn = QtWidgets.QPushButton("Exportar a Excel")
        self.export_btn.clicked.connect(self.export_to_excel)
        self.edit_btn = QtWidgets.QPushButton("Editar Registro Existente")
        self.edit_btn.clicked.connect(self.edit_record)

        for btn,label in [(self.ishikawa_btn,'Análisis causa'),(self.action_btn,'Acción Correctiva'),
                          (self.attach_btn,'Adjuntos')]:
            form_layout.addRow(label,btn)
        form_layout.addRow(self.save_btn)
        form_layout.addRow(self.export_btn)
        form_layout.addRow(self.edit_btn)

        self.enable_widgets_by_order()
        for name in self.fields:
            w,_ = self.fields[name]
            w.textChanged.connect(lambda _, n=name:self.validate_and_progress(n))

    def add_field(self,name,widget,validator,layout):
        widget.setEnabled(False)
        layout.addRow(name,widget)
        self.fields[name]=(widget,validator)

    def enable_widgets_by_order(self):
        first=self.enable_chain_order[0]
        self.fields[first][0].setEnabled(True)
        self.ishikawa_btn.setEnabled(False)
        self.action_btn.setEnabled(False)
        self.attach_btn.setEnabled(False)
        self.save_btn.setEnabled(False)

    def validate_and_progress(self,name):
        w,val=self.fields[name]
        value=w.text()
        ok = val(value) if val else True
        w.setStyleSheet('border:1px solid green;' if ok else 'border:1px solid red;')
        try: idx=self.enable_chain_order.index(name)
        except: idx=-1
        if ok and idx!=-1:
            if idx+1<len(self.enable_chain_order):
                self.fields[self.enable_chain_order[idx+1]][0].setEnabled(True)
            else:
                self.ishikawa_btn.setEnabled(True)
                self.action_btn.setEnabled(True)
                self.attach_btn.setEnabled(True)
                self.save_btn.setEnabled(True)

    def open_ishikawa(self):
        logger.info("Abriendo diálogo de análisis Ishikawa...")
        dlg = IshikawaDialog(self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.ishikawa_result = dlg.get_result()
            logger.info(f"Análisis Ishikawa completado: {len(self.ishikawa_result)} caracteres")
            QtWidgets.QMessageBox.information(self,'Ishikawa','Análisis guardado.')
        else:
            logger.info("Diálogo Ishikawa cancelado por usuario")

    def open_action(self):
        logger.info("Abriendo diálogo de acción correctiva...")
        dlg = ActionDialog(self)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            action = dlg.get_action()
            self.actions_temp.append(action)
            logger.info(f"Acción agregada: {action.get('tarea', 'Sin descripción')[:50]}...")
            logger.info(f"Total de acciones temporales: {len(self.actions_temp)}")
            QtWidgets.QMessageBox.information(self,'Acción','Acción agregada temporalmente.')
        else:
            logger.info("Diálogo de acción cancelado por usuario")

    def attach_files(self):
        logger.info("Iniciando selección de archivos adjuntos...")
        files,_ = QtWidgets.QFileDialog.getOpenFileNames(self,'Seleccionar archivos')
        
        if not files:
            logger.info("Selección de archivos cancelada por usuario")
            return
            
        logger.info(f"Seleccionados {len(files)} archivos para adjuntar")
        
        for f in files:
            dst = ATTACH_DIR / f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{Path(f).name}"
            try: 
                shutil.copy(f,dst)
                self.attached_files.append(str(dst.name))
                logger.info(f"Archivo copiado exitosamente: {Path(f).name}")
            except Exception as e: 
                logger.error(f"Error al copiar archivo {Path(f).name}: {e}")
                QtWidgets.QMessageBox.warning(self,'Adjuntar',f'Error: {e}')
                
        if files: 
            logger.info(f"Proceso de adjuntos completado: {len(files)} archivos")
            QtWidgets.QMessageBox.information(self,'Adjuntos',f'{len(files)} archivos adjuntados.')

    def check_nc_exists(self, nro_nc):
        """Verificar si un número de NC ya existe en la base de datos"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM nc WHERE nro_nc = ?", (nro_nc,))
            count = cur.fetchone()[0]
            return count > 0
        except Exception as e:
            logger.error(f"Error verificando NC existente: {e}")
            return False

    def edit_record_by_number(self, nro_nc):
        """Editar un registro específico por número de NC"""
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM nc WHERE nro_nc=?", (nro_nc,))
            row = cur.fetchone()
            if row:
                # Mapeo correcto de campos UI a índices de DB
                field_mapping = {
                    'Resultado Matriz': 3,   # resultado_matriz
                    'OP': 4,                 # op  
                    'Cant. Invol.': 5,       # cant_invol
                    'Cod. Producto': 6,      # cod_producto
                    'Desc. Producto': 7,     # desc_producto
                    'Cliente': 8,            # cliente
                    'Cant. Scrap': 9,        # cant_scrap
                    'Costo': 10,             # costo
                    'Cant. Recuperada': 11,  # cant_recuperada
                    'Falla': 13              # falla
                }
                
                # Rellenar campos excepto Nro NC usando mapeo correcto
                for name in self.enable_chain_order[1:]:
                    if name in field_mapping:
                        w, _ = self.fields[name]
                        db_index = field_mapping[name]
                        value = row[db_index] if row[db_index] is not None else ''
                        w.setText(str(value))
                        logger.debug(f"Campo '{name}' cargado: {value}")
                    else:
                        logger.warning(f"Campo '{name}' no tiene mapeo definido")
                        
                logger.info(f"Datos de NC {nro_nc} cargados para edición")
                QtWidgets.QMessageBox.information(self, "Editar", f"Datos de NC {nro_nc} cargados.\nModifique los campos y presione Guardar.")
            else:
                logger.warning(f"No se encontró NC {nro_nc} para edición")
                QtWidgets.QMessageBox.warning(self, "No encontrado", f"No existe NC {nro_nc}")
        except Exception as e:
            logger.error(f"Error cargando NC {nro_nc} para edición: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al cargar registro: {e}")

    def save_record(self):
        import time
        start_time = time.time()
        try:
            logger.info("Iniciando guardado de registro...")
            
            # Validación previa del número de NC
            nro_nc_text = self.fields['Nro NC'][0].text().strip()
            if not nro_nc_text:
                QtWidgets.QMessageBox.warning(self, 'Campo Requerido', 
                                            '⚠️ El número de NC es obligatorio.\n\nPor favor ingrese un número de NC válido.')
                return
                
            try:
                nro = int(nro_nc_text)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, 'Formato Incorrecto', 
                                            f'⚠️ El número de NC debe ser un número entero.\n\nValor ingresado: "{nro_nc_text}"\n\nPor favor corrija el formato.')
                return
            
            # Verificar si el NC ya existe (solo para nuevos registros)
            if self.check_nc_exists(nro):
                respuesta = QtWidgets.QMessageBox.question(
                    self, 'NC Duplicada', 
                    f'⚠️ El número de NC "{nro}" ya existe en el sistema.\n\n¿Qué desea hacer?',
                    QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Retry,
                    QtWidgets.QMessageBox.StandardButton.Cancel
                )
                
                if respuesta == QtWidgets.QMessageBox.StandardButton.Cancel:
                    logger.info(f"Usuario canceló guardado de NC duplicada: {nro}")
                    return
                else:
                    # Si elige Retry, continuar con el guardado (modo edición)
                    logger.info(f"Usuario eligió continuar con NC existente: {nro} (modo edición)")
            
            cur=self.conn.cursor()
            logger.info(f"Guardando NC número: {nro}")
            
            resultado=float(self.fields['Resultado Matriz'][0].text())
            op=int(self.fields['OP'][0].text())
            cant_invol=float(self.fields['Cant. Invol.'][0].text())
            cant_scrap=float(self.fields['Cant. Scrap'][0].text())
            costo=float(self.fields['Costo'][0].text())
            cant_recup=float(self.fields['Cant. Recuperada'][0].text())
            data={name:w.text() for name,(w,_) in self.fields.items()}
            fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Guardar o actualizar NC
            # Verificar si es una actualización
            is_update = self.check_nc_exists(nro)
            
            if is_update:
                # Actualizar registro existente
                cur.execute('''
                    UPDATE nc SET fecha=?,resultado_matriz=?,op=?,cant_invol=?,cod_producto=?,desc_producto=?,cliente=?,
                                  cant_scrap=?,costo=?,cant_recuperada=?,observaciones=?,falla=?,ishikawa=?
                    WHERE nro_nc=?''',
                                (fecha,resultado,op,cant_invol,data['Cod. Producto'],data['Desc. Producto'],
                                 data['Cliente'],cant_scrap,costo,cant_recup,'',data['Falla'],self.ishikawa_result,nro))
                logger.info(f"NC {nro} actualizada exitosamente")
                operacion = "actualizada"
                # Obtener ID del registro existente
                cur.execute("SELECT id FROM nc WHERE nro_nc=?", (nro,))
                nc_id = cur.fetchone()[0]
            else:
                # Insertar nuevo registro
                cur.execute('''
                    INSERT INTO nc (nro_nc,fecha,resultado_matriz,op,cant_invol,cod_producto,desc_producto,cliente,
                                    cant_scrap,costo,cant_recuperada,observaciones,falla,ishikawa)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                (nro,fecha,resultado,op,cant_invol,data['Cod. Producto'],data['Desc. Producto'],
                                 data['Cliente'],cant_scrap,costo,cant_recup,'',data['Falla'],self.ishikawa_result))
                logger.info(f"NC {nro} creada exitosamente")
                operacion = "guardada"
                nc_id = cur.lastrowid
            
            logger.info(f"NC procesada con ID: {nc_id}")

            # Guardar acciones
            if is_update:
                # Para actualizaciones, eliminar acciones existentes primero
                cur.execute("DELETE FROM acciones WHERE nc_id = ?", (nc_id,))
                logger.info(f"Acciones existentes eliminadas para NC {nro}")
            
            logger.info(f"Guardando {len(self.actions_temp)} acciones correctivas...")
            for i, a in enumerate(self.actions_temp, 1):
                cur.execute('''
                    INSERT INTO acciones (nc_id,tarea,tiempo_estimado,responsable,fecha_realizacion,estado,adjuntos)
                    VALUES (?,?,?,?,?,?,?)''',
                            (nc_id,a['tarea'],a['tiempo'],a['responsable'],a['fecha_realizacion'],a['estado'],
                             '||'.join(self.attached_files)))
                logger.info(f"Acción {i} guardada: {a['tarea'][:50]}...")
                
            self.conn.commit()
            logger.info(f"Registro NC {nro} {operacion} exitosamente")
            
            # Mensaje de éxito personalizado
            if operacion == "actualizada":
                mensaje_exito = f"✅ NC {nro} actualizada correctamente.\n\nLos cambios han sido guardados en la base de datos."
                titulo_exito = "Registro Actualizado"
            else:
                mensaje_exito = f"✅ NC {nro} guardada correctamente.\n\nEl nuevo registro ha sido creado en la base de datos."
                titulo_exito = "Registro Guardado"
            
            QtWidgets.QMessageBox.information(self, titulo_exito, mensaje_exito)
            self.reset_form()
            
            # Log de performance
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"save_record ejecutada en {execution_time:.3f}s")
            
        except sqlite3.IntegrityError as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Determinar el tipo de error de integridad y mostrar mensaje amigable
            error_str = str(e).lower()
            if 'unique constraint failed: nc.nro_nc' in error_str:
                nro = self.fields['Nro NC'][0].text()
                mensaje_usuario = f"❌ Error al guardar:\n\nEl número de NC '{nro}' ya existe en el sistema.\n\nPor favor:\n• Verifique el número de NC\n• Use un número diferente\n• O edite el registro existente"
                titulo = "NC Duplicada"
                logger.error(f"Intento de insertar NC duplicada después de {execution_time:.3f}s: NC {nro}")
            else:
                mensaje_usuario = f"❌ Error de base de datos:\n\nNo se pudo guardar el registro debido a un problema de integridad.\n\nDetalle técnico: {e}"
                titulo = "Error de Base de Datos"
                logger.error(f"Error de integridad en base de datos después de {execution_time:.3f}s: {e}")
            
            QtWidgets.QMessageBox.warning(self, titulo, mensaje_usuario)
        except ValueError as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Mensaje amigable para errores de formato
            mensaje_usuario = "❌ Error en los datos ingresados:\n\nAlgunos campos contienen valores incorrectos.\n\nPor favor verifique que:\n• Los números estén en formato correcto\n• No haya campos vacíos requeridos\n• Los decimales usen punto (.) no coma (,)"
            
            logger.error(f"Error en formato de datos después de {execution_time:.3f}s: {e}")
            QtWidgets.QMessageBox.warning(self,'Datos Incorrectos', mensaje_usuario)
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Mensaje amigable para errores generales
            mensaje_usuario = f"❌ Error inesperado al guardar:\n\nNo se pudo completar la operación.\n\nPor favor:\n• Verifique todos los campos\n• Intente nuevamente\n• Contacte soporte si persiste\n\nDetalle técnico: {str(e)[:100]}..."
            
            logger.error(f"Error inesperado al guardar después de {execution_time:.3f}s: {e}")
            QtWidgets.QMessageBox.critical(self,'Error del Sistema', mensaje_usuario)

    def export_to_excel(self):
        import time
        start_time = time.time()
        try:
            logger.info("Iniciando exportación a Excel...")
            cur=self.conn.cursor()
            cur.execute("SELECT * FROM nc")
            rows=cur.fetchall()
            logger.info(f"Obtenidos {len(rows)} registros para exportar")
            
            headers=[desc[0] for desc in cur.description]
            wb=Workbook()
            ws=wb.active
            ws.append(headers)
            for row in rows: ws.append(row)
            wb.save("export_nc.xlsx")
            
            logger.info("Exportación a Excel completada exitosamente")
            QtWidgets.QMessageBox.information(self,"Exportar","Datos exportados a export_nc.xlsx")
            
            # Log de performance
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"export_to_excel ejecutada en {execution_time:.3f}s")
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"Error al exportar a Excel después de {execution_time:.3f}s: {e}")
            QtWidgets.QMessageBox.warning(self,"Error",f"No se pudo exportar: {e}")

    def edit_record(self):
        nro,ok=QtWidgets.QInputDialog.getInt(self,"Editar","Ingrese Nro NC a editar:")
        if not ok: 
            logger.info("Edición cancelada por usuario")
            return
            
        logger.info(f"Iniciando edición de NC número: {nro}")
        cur=self.conn.cursor()
        cur.execute("SELECT * FROM nc WHERE nro_nc=?",(nro,))
        row=cur.fetchone()
        
        if not row:
            logger.warning(f"No se encontró NC {nro} para edición")
            QtWidgets.QMessageBox.warning(self,"No encontrado",f"No existe NC {nro}")
            return
            
        logger.info(f"NC {nro} encontrada, cargando datos para edición...")
        
        # Mapeo correcto de campos UI a índices de DB
        field_mapping = {
            'Resultado Matriz': 3,   # resultado_matriz
            'OP': 4,                 # op  
            'Cant. Invol.': 5,       # cant_invol
            'Cod. Producto': 6,      # cod_producto
            'Desc. Producto': 7,     # desc_producto
            'Cliente': 8,            # cliente
            'Cant. Scrap': 9,        # cant_scrap
            'Costo': 10,             # costo
            'Cant. Recuperada': 11,  # cant_recuperada
            'Falla': 13              # falla
        }
        
        # Rellenar campos excepto Nro NC usando mapeo correcto
        for name in self.enable_chain_order[1:]:
            if name in field_mapping:
                w, _ = self.fields[name]
                db_index = field_mapping[name]
                value = row[db_index] if row[db_index] is not None else ''
                w.setText(str(value))
                logger.debug(f"Campo '{name}' cargado: {value}")
            else:
                logger.warning(f"Campo '{name}' no tiene mapeo definido")
                
        logger.info(f"Datos de NC {nro} cargados para edición")
        QtWidgets.QMessageBox.information(self,"Editar","Modifique los campos y presione Guardar.")

    def reset_form(self):
        for w,_ in self.fields.values():
            w.clear()
            w.setEnabled(False)
            w.setStyleSheet('')
        self.attached_files=[]
        self.actions_temp=[]
        self.ishikawa_result=''
        self.enable_widgets_by_order()

if __name__=='__main__':
    logger.info("=== INICIANDO APLICACIÓN NC AC FABEN ===")
    logger.info(f"Versión Python: {sys.version}")
    logger.info(f"Directorio de trabajo: {Path.cwd()}")
    logger.info(f"Archivo de log principal: {LOG_FILE}")
    logger.info(f"Archivo de log debug: {DEBUG_LOG_FILE}")
    
    try:
        init_db()
        logger.info("Inicializando aplicación PyQt6...")
        app=QtWidgets.QApplication(sys.argv)
        
        win=MainWindow()
        win.show()
        logger.info("Aplicación iniciada exitosamente")
        
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"Error crítico al iniciar aplicación: {e}")
        import traceback
        logger.critical(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
