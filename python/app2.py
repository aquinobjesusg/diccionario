# app.py - Diccionario Interactivo en Flask (Con CORS corregido)
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from functools import wraps
import psycopg2
from gtts import gTTS
import io
import base64
import secrets
import smtplib
import time
import random
import speech_recognition as sr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import timedelta

app = Flask(__name__)
application = app

# Configuración de sesión
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=24)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # Requerido para SameSite=None
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Configuración CORS completa
CORS(app, 
     resources={
         r"/*": {
             "origins": [
                 "http://localhost:5000",
                 "http://127.0.0.1:5000",
                 "http://localhost:8501",
                 "http://127.0.0.1:8501",
                 "https://systemsya.com",
                 "https://www.systemsya.com"
             ],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
             "expose_headers": ["Content-Type", "X-Total-Count"],
             "supports_credentials": True,
             "max_age": 3600
         }
     },
     supports_credentials=True)

# Middleware para asegurar CORS en todas las respuestas
@app.after_request
def after_request(response):
    """Agrega headers CORS a todas las respuestas"""
    origin = request.headers.get('Origin')
    allowed_origins = [
        'http://localhost:5000',
        'http://127.0.0.1:5000', 
        'http://localhost:8501',
        'http://127.0.0.1:8501',
        'https://systemsya.com',
        'https://www.systemsya.com'
    ]
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Expose-Headers'] = 'Content-Type, X-Total-Count'
    
    return response

# Manejo de peticiones OPTIONS (Preflight)
@app.route('/<path:path>', methods=['OPTIONS'])
@app.route('/', methods=['OPTIONS'])
def handle_options(path=None):
    """Maneja las peticiones OPTIONS para CORS preflight"""
    response = jsonify({'status': 'ok'})
    origin = request.headers.get('Origin')
    allowed_origins = [
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'http://localhost:8501', 
        'http://127.0.0.1:8501',
        'https://systemsya.com',
        'https://www.systemsya.com'
    ]
    
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Max-Age'] = '3600'
    
    return response

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================
DB_CONFIG = {
    'host': "localhost",
    'database': "systemsy_dicc1",
    'user': "systemsy_dicc",
    'password': "systemsy_dicc",
    'port': "5432"
}

EMAIL_CONFIG = {
    'remitente': "edwinreyes308@gmail.com",
    'password': "nlco hjxd wjzi srei"
}

# =============================================================================
# DECORADORES Y UTILIDADES
# =============================================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('auth'):
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    """Obtiene conexión a la base de datos"""
    return psycopg2.connect(**DB_CONFIG)

def rutina_audio(texto, lang='en'):
    """Genera audio en base64 para reproducción"""
    if not texto:
        return None
    try:
        tts = gTTS(text=texto, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return base64.b64encode(fp.getvalue()).decode()
    except Exception as e:
        print(f"Error generando audio: {e}")
        return None

def obtener_par(idx, lista, col_idx, idioma_ori):
    """Obtiene el par de palabras (origen-destino) según el idioma de origen"""
    if not lista or idx + 1 >= len(lista):
        return "---", "---", 'en'
    
    reg1, reg2 = lista[idx], lista[idx + 1]
    
    # Determinar cuál es inglés (id_lenguaje=1) y cuál español (id_lenguaje=2)
    palabra_ing = reg1[col_idx] if reg1[1] == 1 else reg2[col_idx]
    palabra_esp = reg1[col_idx] if reg1[1] == 2 else reg2[col_idx]
    
    if idioma_ori == "Español":
        return palabra_esp, palabra_ing, 'en'
    else:
        return palabra_ing, palabra_esp, 'es'

def ejecutar_envio_mail(destino, asunto, cuerpo):
    """Envía correo electrónico"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_CONFIG['remitente']
    msg['To'] = destino
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_CONFIG['remitente'], EMAIL_CONFIG['password'])
        server.sendmail(EMAIL_CONFIG['remitente'], destino, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

# =============================================================================
# FUNCIONES DE BASE DE DATOS
# =============================================================================
def registrar_usuario(nombre, alias, correo, nivel_texto):
    """Registra un nuevo usuario en estado PENDIENTE"""
    try:
        token = secrets.token_urlsafe(16)
        conn = get_db_connection()
        cur = conn.cursor()
        
        alias_final = alias.strip() if (alias and alias.strip()) else nombre.replace(" ", "")[:10]
        
        query = """
            INSERT INTO usuarios (nombre, alias, correo, nivel, token_verificacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'PENDIENTE')
        """
        cur.execute(query, (nombre.strip(), alias_final, correo.strip(), nivel_texto, token))
        conn.commit()
        cur.close()
        conn.close()
        return True, token
    except Exception as e:
        return False, str(e)

def validar_credenciales(password):
    """Valida las credenciales del usuario"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = "SELECT nombre, alias FROM usuarios WHERE clave = %s AND estado = 'ACTIVO'"
        cur.execute(query, (password.strip(),))
        registro = cur.fetchone()
        cur.close()
        conn.close()
        
        if registro:
            return registro[1] if registro[1] else registro[0]
        return None
    except Exception as e:
        print(f"Error validando credenciales: {e}")
        return None

def obtener_datos_db(categoria, nivel, tipos_sel=None, subtipos_sel=None):
    """Obtiene datos de la base de datos según filtros"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        mapeo = {
            "Palabras": ("palabras", "id_palabra", 4, "id_tipo_palabra"),
            "Modismos": ("modismos", "id_modismo", 3, None),
            "Verbos Compuestos": ("verbos_compuestos", "id_verbo", 3, None)
        }
        
        if categoria not in mapeo:
            return [], 0
        
        tabla, id_col, col_idx, col_tipo = mapeo[categoria]
        query = f"SELECT * FROM {tabla} WHERE id_nivel = %s "
        params = [int(nivel)]
        
        if col_tipo and tipos_sel:
            query += f"AND {col_tipo} IN ({','.join(['%s'] * len(tipos_sel))}) "
            params.extend(tipos_sel)
            
            # Filtro por subtipo para verbos
            if tabla == "palabras" and subtipos_sel:
                query += f"AND subtipo IN ({','.join(['%s'] * len(subtipos_sel))}) "
                params.extend(subtipos_sel)
        
        query += f"ORDER BY {id_col}"
        cur.execute(query, tuple(params))
        datos = cur.fetchall()
        cur.close()
        conn.close()
        return datos, col_idx
    except Exception as e:
        print(f"Error en BD: {e}")
        return [], 0

def actualizar_password(token, nueva_password):
    """Actualiza la contraseña del usuario"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT correo, nombre FROM usuarios WHERE token_verificacion = %s", (token,))
        usuario = cur.fetchone()
        
        if not usuario:
            return False, "El enlace es inválido o ya fue usado"
        
        query = """
            UPDATE usuarios SET clave = %s, estado = 'ACTIVO', token_verificacion = NULL 
            WHERE token_verificacion = %s
        """
        cur.execute(query, (nueva_password, token))
        conn.commit()
        cur.close()
        conn.close()
        return True, "Contraseña actualizada con éxito"
    except Exception as e:
        return False, str(e)

def solicitar_recuperacion(correo):
    """Genera token y envía correo de recuperación"""
    try:
        token = secrets.token_urlsafe(16)
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT nombre FROM usuarios WHERE correo = %s AND estado = 'ACTIVO'", (correo.strip(),))
        resultado = cur.fetchone()
        
        if resultado:
            nombre_usuario = resultado[0]
            cur.execute("UPDATE usuarios SET token_verificacion = %s WHERE correo = %s", (token, correo.strip()))
            conn.commit()
            
            # Enviar correo
            enlace = f"https://systemsya.com/diccionario/recuperar/{token}"
            asunto = "🔑 Restablecer tu contraseña - Diccionario Interactivo"
            cuerpo = f"""Hola {nombre_usuario},

Hemos recibido una solicitud para restablecer tu contraseña.
Para crear una nueva clave, haz clic en el siguiente enlace:

{enlace}

Si no solicitaste este cambio, puedes ignorar este correo."""
            
            ejecutar_envio_mail(correo.strip(), asunto, cuerpo)
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en recuperación: {e}")
        return False

# =============================================================================
# RUTAS DE LA API
# =============================================================================
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def api_login():
    """Endpoint de login"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    data = request.json
    password = data.get('password', '')
    
    # Puerta de desarrollo
    if password == "peluche 02":
        session.permanent = True
        session['usuario_actual'] = "Administrador"
        session['auth'] = True
        return jsonify({'success': True, 'usuario': "Administrador"})
    
    usuario = validar_credenciales(password)
    if usuario:
        session.permanent = True
        session['usuario_actual'] = usuario
        session['auth'] = True
        return jsonify({'success': True, 'usuario': usuario})
    
    return jsonify({'success': False, 'error': 'Credenciales inválidas'})

@app.route('/api/registro', methods=['POST', 'OPTIONS'])
def api_registro():
    """Endpoint de registro"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    data = request.json
    nombre = data.get('nombre')
    correo = data.get('correo')
    alias = data.get('alias')
    nivel = data.get('nivel')
    
    if not nombre or not correo:
        return jsonify({'success': False, 'error': 'Nombre y correo son obligatorios'})
    
    exito, resultado = registrar_usuario(nombre, alias, correo, nivel)
    if exito:
        # Enviar correo de activación
        enlace = f"https://systemsya.com/diccionario/activar/{resultado}"
        asunto = "🎓 Activa tu cuenta - Diccionario Interactivo"
        cuerpo = f"""Hola {nombre},

¡Gracias por registrarte! Para completar tu perfil y crear tu contraseña, 
haz clic en el siguiente enlace:

{enlace}

Este enlace es de un solo uso."""
        
        if ejecutar_envio_mail(correo, asunto, cuerpo):
            return jsonify({'success': True, 'message': f'Registro exitoso. Revisa tu correo: {correo}'})
        return jsonify({'success': False, 'error': 'Usuario registrado pero error al enviar correo'})
    
    return jsonify({'success': False, 'error': resultado})

@app.route('/api/recuperar', methods=['POST', 'OPTIONS'])
def api_recuperar():
    """Endpoint de recuperación de contraseña"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    data = request.json
    correo = data.get('correo')
    
    if not correo:
        return jsonify({'success': False, 'error': 'Correo requerido'})
    
    solicitar_recuperacion(correo)
    return jsonify({'success': True, 'message': 'Si el correo existe, recibirás un enlace'})

@app.route('/api/crear-password', methods=['POST', 'OPTIONS'])
def api_crear_password():
    """Endpoint para crear nueva contraseña"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    data = request.json
    token = data.get('token')
    password = data.get('password')
    confirm = data.get('confirm_password')
    
    if not 8 <= len(password) <= 12:
        return jsonify({'success': False, 'error': 'La contraseña debe tener entre 8 y 12 caracteres'})
    
    if password != confirm:
        return jsonify({'success': False, 'error': 'Las contraseñas no coinciden'})
    
    exito, mensaje = actualizar_password(token, password)
    return jsonify({'success': exito, 'message': mensaje})

@app.route('/api/cargar-datos', methods=['POST', 'OPTIONS'])
@login_required
def api_cargar_datos():
    """Carga datos desde la base de datos"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    data = request.json
    categoria = data.get('categoria', 'Palabras')
    nivel = data.get('nivel', 1)
    tipos = data.get('tipos', [])
    subtipos = data.get('subtipos', [])
    idioma_ori = data.get('idioma_ori', 'Español')
    
    datos, col_idx = obtener_datos_db(categoria, nivel, tipos, subtipos)
    total_p = len(datos) // 2
    
    # Preparar datos para el frontend
    palabras = []
    for i in range(0, len(datos), 2):
        if i + 1 < len(datos):
            origen, destino, _ = obtener_par(i, datos, col_idx, idioma_ori)
            palabras.append({
                'origen': origen,
                'destino': destino,
                'idx': i
            })
    
    # Guardar en sesión
    session['datos_actuales'] = {
        'data': [[list(row) for row in datos], col_idx] if datos else [[], 0],
        'categoria': categoria,
        'nivel': nivel,
        'idioma_ori': idioma_ori,
        'total': total_p
    }
    
    return jsonify({
        'success': True,
        'total': total_p,
        'palabras': palabras
    })

@app.route('/api/obtener-audio', methods=['POST', 'OPTIONS'])
@login_required
def api_obtener_audio():
    """Genera audio para un texto"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    data = request.json
    texto = data.get('texto', '')
    lang = data.get('lang', 'en')
    
    audio_b64 = rutina_audio(texto, lang)
    return jsonify({'audio': audio_b64})

@app.route('/api/procesar-voz', methods=['POST', 'OPTIONS'])
@login_required
def api_procesar_voz():
    """Procesa audio a texto"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    if 'audio' not in request.files:
        return jsonify({'success': False, 'error': 'No se recibió audio'})
    
    audio_file = request.files['audio']
    lang = request.form.get('lang', 'en-US')
    
    r = sr.Recognizer()
    try:
        # Guardar temporalmente
        import tempfile
        with tempfile.NamedTemporaryFile(delete=True, suffix='.wav') as tmp:
            audio_file.save(tmp.name)
            tmp.flush()
            with sr.AudioFile(tmp.name) as source:
                audio_data = r.record(source)
            texto = r.recognize_google(audio_data, language=lang)
            return jsonify({'success': True, 'texto': texto})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/verificar-sesion', methods=['GET', 'OPTIONS'])
def api_verificar_sesion():
    """Verifica si la sesión está activa"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    if session.get('auth'):
        return jsonify({'success': True, 'usuario': session.get('usuario_actual')})
    return jsonify({'success': False})

@app.route('/api/logout', methods=['POST', 'OPTIONS'])
def api_logout():
    """Cierra la sesión"""
    if request.method == 'OPTIONS':
        return handle_options(None)
    
    session.clear()
    return jsonify({'success': True})

# =============================================================================
# RUTAS DE PÁGINAS
# =============================================================================
@app.route('/')
def index():
    """Página principal"""
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    return render_template_string(DASHBOARD_TEMPLATE, usuario=session.get('usuario_actual'))

@app.route('/activar/<token>')
def activar_cuenta(token):
    """Página de activación de cuenta"""
    return render_template_string(CREAR_PASSWORD_TEMPLATE, token=token)

@app.route('/recuperar/<token>')
def recuperar_password(token):
    """Página de recuperación de contraseña"""
    return render_template_string(CREAR_PASSWORD_TEMPLATE, token=token)

# =============================================================================
# TEMPLATES (Mismos que antes, se incluirían aquí)
# =============================================================================
# [Los templates LOGIN_TEMPLATE, CREAR_PASSWORD_TEMPLATE y DASHBOARD_TEMPLATE 
# se mantienen igual que en tu código original]

# Nota: Por brevedad, los templates no se repiten aquí, pero mantén los que ya tienes

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)