# region Imports

from flask import Flask, request, redirect, render_template
import json
import os
import sys
from datetime import datetime, timedelta

# endregion

# region Variables globales

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TAREAS_FILE = os.path.join(SCRIPT_DIR, 'tareas.json')

app = Flask(__name__)


tareas = []
categorias = []
siguiente_id = 1



# endregion


# region Funciones auxiliares

def cargar_tareas():
    try:
        if os.path.exists(TAREAS_FILE):
            with open(TAREAS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('tareas', []), data.get('siguiente_id', 1), data.get('categorias', [])
        else:
            data_inicial = {
                'tareas': [],
                'siguiente_id': 1,
                'categorias': []
            }
            with open(TAREAS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_inicial, f, indent=2, ensure_ascii=False)
            return [], 1, []
    except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
        print(f"Error al cargar tareas: {e}")
        return [], 1, []

tareas, siguiente_id, categorias = cargar_tareas()

# Variable para fecha simulada (solo en modo debug)
fecha_simulada = datetime.now().strftime('%Y-%m-%d')

def obtener_fecha_actual():
    """Retorna la fecha actual (real o simulada según el modo)"""
    global fecha_simulada
    return fecha_simulada

def agregar_tarea(titulo, descripcion, categoria=''):
    global siguiente_id
    tarea = {
        'id': siguiente_id,
        'titulo': titulo,
        'descripcion': descripcion,
        'completada': False,
        'categoria': categoria,
        'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'fecha_completado': None
    }
    siguiente_id += 1
    tareas.append(tarea)
    guardar_tareas()

def completar_tarea(id):
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['completada'] = not tarea['completada']
            if tarea['completada']:
                tarea['fecha_completado'] = obtener_fecha_actual()
            else:
                tarea['fecha_completado'] = None
            guardar_tareas()
            return True
    return False



def obtener_tareas():
    return tareas

def obtener_tarea_por_id(id):
    for tarea in tareas:
        if tarea['id'] == id:
            return tarea

def limpiar_tareas_antiguas():
    """Elimina tareas completadas hace más de 2 días"""
    global tareas
    fecha_actual = obtener_fecha_actual()
    fecha_limite = (datetime.strptime(fecha_actual, '%Y-%m-%d') - timedelta(days=2)).strftime('%Y-%m-%d')
    
    tareas_originales = len(tareas)
    
    tareas = [tarea for tarea in tareas if not (
        tarea['completada'] and 
        tarea['fecha_completado'] and 
        tarea['fecha_completado'] <= fecha_limite
    )]
    
    if len(tareas) < tareas_originales:
        guardar_tareas()
        return tareas_originales - len(tareas)
    return 0

def organizar_tareas_por_fecha():
    """Organiza las tareas según su estado y fecha de completado"""
    fecha_actual = obtener_fecha_actual()
    fecha_ayer = (datetime.strptime(fecha_actual, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Mantener el orden original de las tareas
    tareas_activas = []  # Tareas que se muestran en la lista principal
    tareas_completadas_ayer = []  # Tareas que van a la sección "completadas ayer"
    tareas_antiguas = []  # Tareas que se eliminan
    
    for tarea in tareas:
        if not tarea['completada']:
            # Tarea pendiente - va a la lista principal
            tareas_activas.append(tarea)
        elif tarea['fecha_completado'] == fecha_actual:
            # Tarea completada hoy - mantiene su posición en la lista principal
            tareas_activas.append(tarea)
        elif tarea['fecha_completado'] == fecha_ayer:
            # Tarea completada ayer - va a la sección especial
            tareas_completadas_ayer.append(tarea)
        elif tarea['fecha_completado'] and tarea['fecha_completado'] < fecha_ayer:
            # Tarea muy antigua - se elimina
            tareas_antiguas.append(tarea)
    
    return {
        'pendientes': tareas_activas,  # Ya no separamos pendientes y completadas_hoy
        'completadas_hoy': [],  # Vacío porque van en pendientes
        'completadas_ayer': tareas_completadas_ayer,
        'eliminadas': len(tareas_antiguas)
    }

def agregar_categoria(nombre_categoria):
    global categorias
    if nombre_categoria and nombre_categoria not in categorias:
        categorias.append(nombre_categoria)
        guardar_tareas()
        return True
    return False

    
def guardar_tareas():
    data = {
        'tareas': tareas,
        'siguiente_id': siguiente_id,
        'categorias': categorias
    }
    try:
        with open(TAREAS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar tareas: {e}")
        print(f"Intentando guardar en: {TAREAS_FILE}")
    



# endregion



# region Rutas

@app.route('/')
def index():

    tareas_eliminadas = limpiar_tareas_antiguas()
    
    organizacion = organizar_tareas_por_fecha()
    
    return render_template('index.html', 
                         tareas=organizacion['pendientes'],  # Ya incluye pendientes y completadas hoy
                         tareas_completadas_ayer=organizacion['completadas_ayer'],
                         categorias=categorias,
                         tareas_eliminadas=tareas_eliminadas,
                         fecha_simulada=fecha_simulada,
                         debug_mode=app.debug)


@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    categoria = request.form.get('categoria', '')

    if titulo and descripcion:
        agregar_tarea(titulo, descripcion, categoria)
        return redirect('/')
    else:
        return render_template('index.html', tareas=tareas, categorias=categorias, error='Título y descripción son requeridos')
    

@app.route('/completar/<int:id>')
def completar(id):
    completar_tarea(id)
    return redirect('/')

def eliminar_tarea_func(id):
    global tareas
    tareas = [tarea for tarea in tareas if tarea['id'] != id]
    guardar_tareas()  

@app.route('/eliminar/<int:id>')
def eliminar_tarea(id):
    eliminar_tarea_func(id)
    return redirect('/')

@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria_route():
    nombre_categoria = request.form.get('nombre_categoria', '').strip()
    if agregar_categoria(nombre_categoria):
        return redirect('/')
    else:
        return render_template('index.html', tareas=tareas, categorias=categorias, error='Categoría ya existe o es inválida')

# Rutas para debugging de fecha simulada
@app.route('/debug/avanzar_dia')
def avanzar_dia():
    if not app.debug:
        return "Acceso denegado", 403
    global fecha_simulada
    fecha_actual = datetime.strptime(fecha_simulada, '%Y-%m-%d')
    fecha_simulada = (fecha_actual + timedelta(days=1)).strftime('%Y-%m-%d')
    return redirect('/')

@app.route('/debug/retroceder_dia')
def retroceder_dia():
    if not app.debug:
        return "Acceso denegado", 403
    global fecha_simulada
    fecha_actual = datetime.strptime(fecha_simulada, '%Y-%m-%d')
    fecha_simulada = (fecha_actual - timedelta(days=1)).strftime('%Y-%m-%d')
    return redirect('/')

@app.route('/debug/resetear_fecha')
def resetear_fecha():
    if not app.debug:
        return "Acceso denegado", 403
    global fecha_simulada
    fecha_simulada = datetime.now().strftime('%Y-%m-%d')
    return redirect('/')

# endregion


if __name__ == '__main__':
    # Evitar múltiples instancias usando archivo de bloqueo
    lock_file = os.path.join(SCRIPT_DIR, 'app.lock')
    
    try:
        # Intentar crear archivo de bloqueo
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        
        # Configurar para eliminar el archivo al salir
        import atexit
        atexit.register(lambda: os.remove(lock_file) if os.path.exists(lock_file) else None)
        
        print("Iniciando aplicación Flask...")
        # Detectar si se está ejecutando desde app_webview.py
        if 'app_webview.py' in sys.argv[0] or any('webview' in arg for arg in sys.argv):
            app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)
        else:
            app.run(debug=True, host='127.0.0.1', port=5000)
        
    except FileExistsError:
        print("Ya hay una instancia de la aplicación ejecutándose")
        sys.exit(1)
    except Exception as e:
        print(f"Error al iniciar: {e}")
        if os.path.exists(lock_file):
            os.remove(lock_file)
        sys.exit(1)
