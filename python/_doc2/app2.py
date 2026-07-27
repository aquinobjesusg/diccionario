# app.py - Diccionario Interactivo en Flask
#import streamlit as st
import psycopg2
from gtts import gTTS
import io
import base64
import random
import time
import speech_recognition as sr
import re
import secrets  
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================
DB_CONFIG = {
    'host': "localhost",
    'database': "pprueba",
    'user': "postgres",
    'password': "password2017",
    'port': "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# =============================================================================
# DECORADORES Y UTILIDADES
# =============================================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('auth'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def rutina_audio(texto, lang='en'):
    """Genera audio en base64 para reproducción"""
    if not texto:
        return None
    try:
        tts = gTTS(text=texto, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return base64.b64encode(fp.getvalue()).decode()
    except:
        return None

def convertir_mic_a_texto(audio_bytes):
    """Convierte audio a texto"""
    r = sr.Recognizer()
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=True, suffix='.wav') as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            with sr.AudioFile(tmp.name) as source:
                audio_data = r.record(source)
            return r.recognize_google(audio_data, language="en-US")
    except Exception:
        return ""

def obtener_par(idx, lista, col_idx, idioma_ori):
    """Obtiene par de palabras para traducción"""
    if not lista or idx+1 >= len(lista):
        return "---", "---", 'en', ""
    p1, p2 = lista[idx][col_idx], lista[idx+1][col_idx]
    if idioma_ori == "Español":
        return p2, p1, 'en', ""
    return p1, p2, 'es', ""

# =============================================================================
# FUNCIONES DE CORREO
# =============================================================================
def ejecutar_envio_mail(remitente, password_app, destino, asunto, cuerpo):
    """Envía correo vía SMTP"""
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destino
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password_app)
        server.sendmail(remitente, destino, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def enviar_correo_activacion(correo_destino, nombre_usuario, token):
    """Envía correo de activación"""
    remitente = "edwinreyes308@gmail.com"
    password_app = "nlco hjxd wjzi srei"
    enlace = f"http://localhost:5000/activar/{token}"
    
    asunto = "🎓 Activa tu cuenta - Diccionario Interactivo"
    cuerpo = f"""Hola {nombre_usuario},

¡Gracias por registrarte! Para completar tu perfil y crear tu contraseña 
personal, por favor haz clic en el siguiente enlace:

{enlace}

Este enlace es de un solo uso."""
    
    return ejecutar_envio_mail(remitente, password_app, correo_destino, asunto, cuerpo)

def enviar_correo_recuperacion(correo_destino, nombre_usuario, token):
    """Envía correo de recuperación"""
    remitente = "edwinreyes308@gmail.com"
    password_app = "nlco hjxd wjzi srei"
    enlace = f"http://localhost:5000/recuperar/{token}"
    
    asunto = "🔑 Restablecer tu contraseña - Diccionario Interactivo"
    cuerpo = f"""Hola {nombre_usuario},

Hemos recibido una solicitud para restablecer tu contraseña en el Diccionario Interactivo.
Para crear una nueva clave, haz clic en el siguiente enlace:

{enlace}

Si no solicitaste este cambio, puedes ignorar este correo de forma segura."""
    
    return ejecutar_envio_mail(remitente, password_app, correo_destino, asunto, cuerpo)

# =============================================================================
# FUNCIONES DE BASE DE DATOS
# =============================================================================
def registrar_usuario(nombre, alias, correo, nivel_texto):
    """Registra nuevo usuario"""
    try:
        token = secrets.token_urlsafe(16)
        conn = get_db_connection()
        cur = conn.cursor()
        
        ali_final = alias.strip() if (alias and alias.strip()) else nombre.replace(" ", "")[:10]
        
        query = """
            INSERT INTO usuarios (nombre, alias, correo, nivel, token_verificacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'PENDIENTE')
        """
        cur.execute(query, (nombre.strip(), ali_final, correo.strip(), nivel_texto, token))
        conn.commit()
        cur.close()
        conn.close()
        return True, token
    except Exception as e:
        return False, str(e)

def validar_credenciales(password_ingresada):
    """Valida credenciales de usuario"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = "SELECT nombre, alias FROM usuarios WHERE clave = %s AND estado = 'ACTIVO'"
        cur.execute(query, (password_ingresada.strip(),))
        registro = cur.fetchone()
        cur.close()
        conn.close()
        return registro if registro else False
    except Exception as e:
        print(f"Error: {e}")
        return False

def obtener_datos_db(categoria, nivel, tipos_sel=None):
    """Obtiene datos de la base de datos"""
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
            query += f"AND {col_tipo} IN ({','.join(['%s']*len(tipos_sel))}) "
            params.extend(tipos_sel)
        
        query += f"ORDER BY {id_col}"
        cur.execute(query, tuple(params))
        datos = cur.fetchall()
        cur.close()
        conn.close()
        return datos, col_idx
    except Exception as e:
        print(f"Error DB: {e}")
        return [], 0

# =============================================================================
# RUTAS DE AUTENTICACIÓN
# =============================================================================
@app.route('/')
def index():
    if session.get('auth'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        # Puerta de desarrollo
        if password == "peluche 02":
            session['usuario_actual'] = "Administrador"
            session['auth'] = True
            return jsonify({'success': True})
        
        credenciales = validar_credenciales(password)
        if credenciales:
            session['usuario_actual'] = credenciales[1] if credenciales[1] else credenciales[0]
            session['auth'] = True
            return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Credenciales inválidas'})
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/registro', methods=['POST'])
def registro():
    data = request.json
    nombre = data.get('nombre')
    correo = data.get('correo')
    alias = data.get('alias')
    nivel = data.get('nivel')
    
    if not nombre or not correo:
        return jsonify({'success': False, 'error': 'Nombre y correo son obligatorios'})
    
    exito, resultado = registrar_usuario(nombre, alias, correo, nivel)
    if exito:
        if enviar_correo_activacion(correo, nombre, resultado):
            return jsonify({'success': True, 'message': f'Registro exitoso. Revisa tu correo: {correo}'})
        return jsonify({'success': False, 'error': 'Usuario registrado pero error al enviar correo'})
    
    return jsonify({'success': False, 'error': resultado})

@app.route('/recuperar', methods=['POST'])
def recuperar():
    correo = request.json.get('correo')
    if not correo:
        return jsonify({'success': False, 'error': 'Correo requerido'})
    
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
            enviar_correo_recuperacion(correo.strip(), nombre_usuario, token)
        
        cur.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Si el correo existe, recibirás un enlace'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/activar/<token>')
def activar_cuenta(token):
    return render_template_string(CREAR_PASSWORD_TEMPLATE, token=token)

@app.route('/recuperar/<token>')
def recuperar_password(token):
    return render_template_string(CREAR_PASSWORD_TEMPLATE, token=token)

@app.route('/crear-password', methods=['POST'])
def crear_password():
    data = request.json
    token = data.get('token')
    nueva_pass = data.get('password')
    confirm_pass = data.get('confirm_password')
    
    if not 8 <= len(nueva_pass) <= 12:
        return jsonify({'success': False, 'error': 'La contraseña debe tener entre 8 y 12 caracteres'})
    
    if nueva_pass != confirm_pass:
        return jsonify({'success': False, 'error': 'Las contraseñas no coinciden'})
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT correo, nombre FROM usuarios WHERE token_verificacion = %s", (token,))
        usuario = cur.fetchone()
        
        if not usuario:
            return jsonify({'success': False, 'error': 'El enlace es inválido o ya fue usado'})
        
        query_update = """
            UPDATE usuarios SET clave = %s, estado = 'ACTIVO', token_verificacion = NULL 
            WHERE token_verificacion = %s
        """
        cur.execute(query_update, (nueva_pass, token))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Contraseña actualizada con éxito'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# =============================================================================
# RUTAS PRINCIPALES
# =============================================================================
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE, usuario=session.get('usuario_actual'))

@app.route('/cargar-datos', methods=['POST'])
@login_required
def cargar_datos():
    data = request.json
    categoria = data.get('categoria')
    nivel = data.get('nivel')
    tipos = data.get('tipos', [])
    idioma_ori = data.get('idioma_ori', 'Español')
    
    datos, col_idx = obtener_datos_db(categoria, int(nivel), tipos if tipos else None)
    total_p = len(datos) // 2
    
    session['data'] = datos
    session['col_idx'] = col_idx
    session['idioma_ori'] = idioma_ori
    session['total_p'] = total_p
    session['cat_activa'] = categoria
    session['niv_activo'] = nivel
    
    # Preparar datos para el frontend
    palabras = []
    for i in range(0, len(datos), 2):
        if i+1 < len(datos):
            p1, p2 = datos[i][col_idx], datos[i+1][col_idx]
            if idioma_ori == "Español":
                palabras.append({'origen': p2, 'destino': p1})
            else:
                palabras.append({'origen': p1, 'destino': p2})
    
    return jsonify({
        'success': True,
        'total': total_p,
        'palabras': palabras[:20]  # Primeras 20 palabras
    })

@app.route('/obtener-audio', methods=['POST'])
@login_required
def obtener_audio():
    data = request.json
    texto = data.get('texto', '')
    lang = data.get('lang', 'en')
    
    audio_b64 = rutina_audio(texto, lang)
    return jsonify({'audio': audio_b64})

@app.route('/procesar-voz', methods=['POST'])
@login_required
def procesar_voz():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'error': 'No se recibió audio'})
    
    audio_file = request.files['audio']
    audio_bytes = audio_file.read()
    
    texto = convertir_mic_a_texto(audio_bytes)
    return jsonify({'texto': texto})

# =============================================================================
# TEMPLATES HTML
# =============================================================================

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diccionario Interactivo - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            width: 90%;
            max-width: 400px;
            text-align: center;
        }
        .logo { font-size: 60px; margin-bottom: 10px; }
        h1 { color: #333; margin-bottom: 10px; }
        .subtitle { color: #666; margin-bottom: 30px; font-style: italic; }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            display: none;
        }
        .success {
            background: #efe;
            color: #3c3;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            display: none;
        }
        .hidden { display: none; }
        .form-group { margin: 20px 0; }
        .link { color: #667eea; cursor: pointer; text-decoration: underline; margin-top: 10px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🎓</div>
        <h1>Diccionario Interactivo</h1>
        <div class="subtitle">Aprende inglés de forma divertida</div>
        
        <div id="errorMsg" class="error"></div>
        <div id="successMsg" class="success"></div>
        
        <!-- Login Form -->
        <div id="loginForm">
            <input type="password" id="password" placeholder="Contraseña" autocomplete="off">
            <button onclick="login()">INICIAR SESIÓN</button>
            <button onclick="showRegistro()" class="btn-secondary">CREAR CUENTA</button>
            <div class="link" onclick="showRecuperar()">¿Olvidaste tu contraseña?</div>
        </div>
        
        <!-- Registro Form -->
        <div id="registroForm" class="hidden">
            <input type="text" id="regNombre" placeholder="Nombre Completo">
            <input type="email" id="regCorreo" placeholder="Correo Electrónico">
            <input type="text" id="regAlias" placeholder="Alias (opcional)">
            <select id="regNivel">
                <option value="Básico">Básico</option>
                <option value="Intermedio">Intermedio</option>
                <option value="Avanzado">Avanzado</option>
            </select>
            <button onclick="registro()">REGISTRARSE</button>
            <button onclick="showLogin()" class="btn-secondary">VOLVER</button>
        </div>
        
        <!-- Recuperar Form -->
        <div id="recuperarForm" class="hidden">
            <input type="email" id="recCorreo" placeholder="Tu correo electrónico">
            <button onclick="recuperar()">ENVIAR ENLACE</button>
            <button onclick="showLogin()" class="btn-secondary">VOLVER</button>
        </div>
    </div>
    
    <script>
        function showError(msg) {
            const errorDiv = document.getElementById('errorMsg');
            errorDiv.textContent = msg;
            errorDiv.style.display = 'block';
            setTimeout(() => errorDiv.style.display = 'none', 3000);
        }
        
        function showSuccess(msg) {
            const successDiv = document.getElementById('successMsg');
            successDiv.textContent = msg;
            successDiv.style.display = 'block';
            setTimeout(() => successDiv.style.display = 'none', 3000);
        }
        
        function login() {
            const password = document.getElementById('password').value;
            if (!password) {
                showError('Ingresa tu contraseña');
                return;
            }
            
            fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: 'password=' + encodeURIComponent(password)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/dashboard';
                } else {
                    showError(data.error || 'Credenciales inválidas');
                }
            });
        }
        
        function registro() {
            const data = {
                nombre: document.getElementById('regNombre').value,
                correo: document.getElementById('regCorreo').value,
                alias: document.getElementById('regAlias').value,
                nivel: document.getElementById('regNivel').value
            };
            
            if (!data.nombre || !data.correo) {
                showError('Nombre y correo son obligatorios');
                return;
            }
            
            fetch('/registro', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showSuccess(data.message);
                    setTimeout(() => showLogin(), 2000);
                } else {
                    showError(data.error);
                }
            });
        }
        
        function recuperar() {
            const correo = document.getElementById('recCorreo').value;
            if (!correo) {
                showError('Ingresa tu correo');
                return;
            }
            
            fetch('/recuperar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({correo: correo})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showSuccess(data.message);
                    setTimeout(() => showLogin(), 2000);
                } else {
                    showError(data.error);
                }
            });
        }
        
        function showRegistro() {
            document.getElementById('loginForm').classList.add('hidden');
            document.getElementById('recuperarForm').classList.add('hidden');
            document.getElementById('registroForm').classList.remove('hidden');
        }
        
        function showRecuperar() {
            document.getElementById('loginForm').classList.add('hidden');
            document.getElementById('registroForm').classList.add('hidden');
            document.getElementById('recuperarForm').classList.remove('hidden');
        }
        
        function showLogin() {
            document.getElementById('registroForm').classList.add('hidden');
            document.getElementById('recuperarForm').classList.add('hidden');
            document.getElementById('loginForm').classList.remove('hidden');
        }
    </script>
</body>
</html>
'''

CREAR_PASSWORD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear Contraseña</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            width: 90%;
            max-width: 400px;
            text-align: center;
        }
        h2 { color: #333; margin-bottom: 20px; }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        .error { color: #c33; margin: 10px 0; }
        .success { color: #3c3; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔑 Crear Nueva Contraseña</h2>
        <input type="password" id="password" placeholder="Nueva Contraseña (8-12 caracteres)">
        <input type="password" id="confirm" placeholder="Confirmar Contraseña">
        <button onclick="crearPassword()">GUARDAR CONTRASEÑA</button>
        <div id="message"></div>
    </div>
    
    <script>
        const token = '{{ token }}';
        
        function crearPassword() {
            const password = document.getElementById('password').value;
            const confirm = document.getElementById('confirm').value;
            const msgDiv = document.getElementById('message');
            
            if (password.length < 8 || password.length > 12) {
                msgDiv.className = 'error';
                msgDiv.textContent = 'La contraseña debe tener entre 8 y 12 caracteres';
                return;
            }
            
            if (password !== confirm) {
                msgDiv.className = 'error';
                msgDiv.textContent = 'Las contraseñas no coinciden';
                return;
            }
            
            fetch('/crear-password', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({token: token, password: password, confirm_password: confirm})
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    msgDiv.className = 'success';
                    msgDiv.textContent = data.message;
                    setTimeout(() => window.location.href = '/login', 2000);
                } else {
                    msgDiv.className = 'error';
                    msgDiv.textContent = data.error;
                }
            });
        }
    </script>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diccionario Interactivo - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .user-badge {
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 20px auto;
            padding: 0 20px;
        }
        .sidebar {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .menu-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .menu-btn {
            padding: 12px;
            background: #f0f0f0;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        .menu-btn.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .word-card {
            background: #fafafa;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .word-origen {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .word-destino {
            font-size: 20px;
            color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        button.secondary {
            background: #f0f0f0;
            color: #333;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .grid-2 { grid-template-columns: 1fr; }
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .stat {
            background: #f0f0f0;
            padding: 10px;
            text-align: center;
            border-radius: 8px;
            font-weight: bold;
        }
        .feedback {
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
            display: none;
        }
        .feedback.success {
            background: #d4edda;
            color: #155724;
            display: block;
        }
        .feedback.error {
            background: #f8d7da;
            color: #721c24;
            display: block;
        }
        .hidden { display: none; }
        select, input {
            padding: 8px;
            margin: 5px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>🎓 Diccionario Interactivo</h2>
        <div class="user-badge">👤 {{ usuario }}</div>
    </div>
    
    <div class="container">
        <!-- Sidebar de Configuración -->
        <div class="sidebar">
            <h3>⚙️ Configuración</h3>
            <div class="grid-2">
                <div>
                    <label>Idioma Origen:</label>
                    <select id="idiomaOri">
                        <option value="Español">Español</option>
                        <option value="Inglés">Inglés</option>
                    </select>
                </div>
                <div>
                    <label>Categoría:</label>
                    <select id="categoria">
                        <option value="Palabras">Palabras</option>
                        <option value="Modismos">Modismos</option>
                        <option value="Verbos Compuestos">Verbos Compuestos</option>
                    </select>
                </div>
                <div>
                    <label>Nivel:</label>
                    <select id="nivel">
                        <option value="1">Nivel 1</option>
                        <option value="2">Nivel 2</option>
                        <option value="3">Nivel 3</option>
                    </select>
                </div>
                <div>
                    <label>&nbsp;</label>
                    <button onclick="cargarDatos()">🔄 Cargar Datos</button>
                </div>
            </div>
        </div>
        
        <!-- Menú Principal -->
        <div class="menu-buttons">
            <button class="menu-btn active" onclick="cambiarMenu('repaso')">📋 REPASO</button>
            <button class="menu-btn" onclick="cambiarMenu('entrena')">🎧 ENTRENA</button>
            <button class="menu-btn" onclick="cambiarMenu('juego')">🎯 JUEGO</button>
        </div>
        
        <!-- Contenido Dinámico -->
        <div id="contenido"></div>
        
        <div class="card" style="text-align: center; margin-top: 20px;">
            <button class="secondary" onclick="logout()">🚪 CERRAR SESIÓN</button>
        </div>
    </div>
    
    <script>
        let palabrasData = [];
        let currentMenu = 'repaso';
        let gameState = {
            jugando: false,
            indices: [],
            actual: 0,
            aciertos: 0,
            fallos: 0,
            vistos: new Set(),
            fallidos: {}
        };
        
        function cambiarMenu(menu) {
            currentMenu = menu;
            document.querySelectorAll('.menu-btn').forEach((btn, idx) => {
                btn.classList.toggle('active', idx === ['repaso', 'entrena', 'juego'].indexOf(menu));
            });
            renderizarContenido();
        }
        
        async function cargarDatos() {
            const data = {
                categoria: document.getElementById('categoria').value,
                nivel: document.getElementById('nivel').value,
                idioma_ori: document.getElementById('idiomaOri').value
            };
            
            const response = await fetch('/cargar-datos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await response.json();
            
            if (result.success) {
                palabrasData = result.palabras;
                gameState = {
                    jugando: false,
                    indices: [...Array(palabrasData.length).keys()],
                    actual: 0,
                    aciertos: 0,
                    fallos: 0,
                    vistos: new Set(),
                    fallidos: {}
                };
                renderizarContenido();
                mostrarFeedback('Datos cargados correctamente', 'success');
            } else {
                mostrarFeedback('Error al cargar datos', 'error');
            }
        }
        
        function renderizarContenido() {
            const contenedor = document.getElementById('contenido');
            
            if (currentMenu === 'repaso') {
                contenedor.innerHTML = '<div class="card"><h3>📋 Repaso de Palabras</h3>' +
                    palabrasData.map((p, i) => `
                        <div class="word-card">
                            <div class="word-origen">${p.origen}</div>
                            <div class="word-destino">➔ ${p.destino}</div>
                            <button onclick="reproducirAudio('${p.destino}', 'en')">🔊 Escuchar</button>
                        </div>
                    `).join('') + '</div>';
            } 
            else if (currentMenu === 'entrena') {
                contenedor.innerHTML = `
                    <div class="card">
                        <h3>🎧 Modo Entrenamiento</h3>
                        <div id="entrenaCard">
                            <div class="word-card" style="text-align: center;">
                                <div class="word-origen" id="entrenaOrigen"></div>
                                <button onclick="mostrarTraduccion()">🔍 Mostrar Traducción</button>
                                <button onclick="reproducirAudioEntrena()">🔊 Escuchar</button>
                                <button onclick="siguienteEntrena()">➔ Siguiente</button>
                            </div>
                        </div>
                        <div id="entrenaDestino" style="display:none;" class="word-card">
                            <div class="word-destino" id="entrenaDestinoText"></div>
                        </div>
                    </div>
                `;
                if (palabrasData.length > 0) {
                    document.getElementById('entrenaOrigen').textContent = palabrasData[0].origen;
                }
                window.entrenaIdx = 0;
                window.mostrandoTraduccion = false;
            }
            else if (currentMenu === 'juego') {
                if (!gameState.jugando) {
                    contenedor.innerHTML = `
                        <div class="card">
                            <h3>🎯 Configuración del Juego</h3>
                            <select id="modalidad">
                                <option value="escritura">Escritura</option>
                                <option value="voz">Voz</option>
                                <option value="pronunciacion">Pronunciación</option>
                            </select>
                            <select id="orden">
                                <option value="serial">Serial</option>
                                <option value="aleatorio">Aleatorio</option>
                            </select>
                            <button onclick="iniciarJuego()">🚀 Iniciar Juego</button>
                        </div>
                    `;
                } else {
                    renderizarJuego();
                }
            }
        }
        
        function renderizarJuego() {
            const pendientes = gameState.indices.filter(i => !gameState.vistos.has(i));
            
            if (pendientes.length === 0) {
                // Resumen final
                const fallosList = Object.entries(gameState.fallidos)
                    .map(([p, info]) => `<div class="word-card">❌ ${p} ➔ ${info.traduccion}</div>`).join('');
                
                document.getElementById('contenido').innerHTML = `
                    <div class="card">
                        <h3>📊 Resumen de la Partida</h3>
                        <div class="stats">
                            <div class="stat">✅ Aciertos: ${gameState.aciertos}</div>
                            <div class="stat">❌ Fallos: ${gameState.fallos}</div>
                            <div class="stat">📊 Total: ${gameState.indices.length}</div>
                        </div>
                        <h4>Palabras Falladas:</h4>
                        ${fallosList || '<p>🎉 ¡Excelente! No hubo fallas.</p>'}
                        <button onclick="reiniciarJuego()">🔄 Jugar de nuevo</button>
                        <button onclick="gameState.jugando = false; renderizarContenido()">🏠 Volver</button>
                    </div>
                `;
                return;
            }
            
            const palabraActual = palabrasData[gameState.actual];
            const modalidad = document.getElementById('modalidad')?.value || 'escritura';
            
            let inputHTML = '';
            if (modalidad === 'escritura') {
                inputHTML = `<input type="text" id="respuesta" placeholder="Tu respuesta..." style="margin: 10px 0;">
                            <button onclick="verificarRespuesta('${palabraActual.destino}')">Comprobar</button>`;
            } else if (modalidad === 'voz') {
                inputHTML = `<button onclick="grabarVoz()">🎤 Grabar Respuesta</button>
                            <div id="vozTexto" style="margin: 10px 0;"></div>
                            <button onclick="verificarRespuestaVoz('${palabraActual.destino}')">Comprobar</button>`;
            } else {
                inputHTML = `<button onclick="grabarPronunciacion('${palabraActual.destino}')">🎤 Pronunciar</button>
                            <div id="pronunciacionResultado"></div>`;
            }
            
            document.getElementById('contenido').innerHTML = `
                <div class="card">
                    <div class="stats">
                        <div class="stat">📊 Progreso: ${gameState.vistos.size + 1}/${gameState.indices.length}</div>
                        <div class="stat">✅ Aciertos: ${gameState.aciertos}</div>
                        <div class="stat">❌ Fallos: ${gameState.fallos}</div>
                    </div>
                    <div class="word-card" style="text-align: center;">
                        <div class="word-origen">📖 ${palabraActual.origen}</div>
                        <button onclick="reproducirAudio('${palabraActual.destino}', 'en')">🔊 Escuchar pista</button>
                        ${inputHTML}
                    </div>
                </div>
            `;
        }
        
        function verificarRespuesta(correcta) {
            const respuesta = document.getElementById('respuesta')?.value.toLowerCase().trim();
            const sinonimos = correcta.toLowerCase().split('/');
            
            if (respuesta && sinonimos.some(s => s === respuesta)) {
                gameState.aciertos++;
                mostrarFeedback('✅ ¡Correcto!', 'success');
            } else {
                gameState.fallos++;
                gameState.fallidos[palabrasData[gameState.actual].origen] = {
                    traduccion: correcta
                };
                mostrarFeedback(`❌ Incorrecto. La respuesta correcta es: ${correcta}`, 'error');
            }
            
            gameState.vistos.add(gameState.actual);
            siguientePregunta();
        }
        
        function verificarRespuestaVoz(correcta) {
            const textoVoz = document.getElementById('vozTexto')?.textContent || '';
            const sinonimos = correcta.toLowerCase().split('/');
            
            if (textoVoz && sinonimos.some(s => s === textoVoz.toLowerCase())) {
                gameState.aciertos++;
                mostrarFeedback('✅ ¡Correcto!', 'success');
            } else {
                gameState.fallos++;
                gameState.fallidos[palabrasData[gameState.actual].origen] = {
                    traduccion: correcta
                };
                mostrarFeedback(`❌ Incorrecto. La respuesta correcta es: ${correcta}`, 'error');
            }
            
            gameState.vistos.add(gameState.actual);
            siguientePregunta();
        }
        
        function siguientePregunta() {
            const pendientes = gameState.indices.filter(i => !gameState.vistos.has(i));
            if (pendientes.length > 0) {
                gameState.actual = pendientes[0];
                renderizarJuego();
            } else {
                renderizarJuego(); // Muestra resumen
            }
        }
        
        function iniciarJuego() {
            const orden = document.getElementById('orden').value;
            let indices = [...Array(palabrasData.length).keys()];
            
            if (orden === 'aleatorio') {
                for (let i = indices.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [indices[i], indices[j]] = [indices[j], indices[i]];
                }
            }
            
            gameState = {
                jugando: true,
                indices: indices,
                actual: indices[0],
                aciertos: 0,
                fallos: 0,
                vistos: new Set(),
                fallidos: {}
            };
            renderizarContenido();
        }
        
        function reiniciarJuego() {
            gameState.jugando = false;
            iniciarJuego();
        }
        
        function siguienteEntrena() {
            window.entrenaIdx = (window.entrenaIdx + 1) % palabrasData.length;
            document.getElementById('entrenaOrigen').textContent = palabrasData[window.entrenaIdx].origen;
            const destDiv = document.getElementById('entrenaDestino');
            if (destDiv) destDiv.style.display = 'none';
            window.mostrandoTraduccion = false;
        }
        
        function mostrarTraduccion() {
            if (!window.mostrandoTraduccion) {
                const destDiv = document.getElementById('entrenaDestino');
                const destText = document.getElementById('entrenaDestinoText');
                if (destDiv && destText) {
                    destText.textContent = palabrasData[window.entrenaIdx].destino;
                    destDiv.style.display = 'block';
                    window.mostrandoTraduccion = true;
                }
            }
        }
        
        function reproducirAudioEntrena() {
            reproducirAudio(palabrasData[window.entrenaIdx].destino, 'en');
        }
        
        async function reproducirAudio(texto, lang) {
            const response = await fetch('/obtener-audio', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({texto: texto, lang: lang})
            });
            const data = await response.json();
            if (data.audio) {
                const audio = new Audio('data:audio/mp3;base64,' + data.audio);
                audio.play();
            }
        }
        
        async function grabarVoz() {
            mostrarFeedback('🎤 Grabando... Habla ahora', 'success');
            // Implementar grabación con MediaRecorder
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(stream);
                const chunks = [];
                
                mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
                mediaRecorder.onstop = async () => {
                    const blob = new Blob(chunks, { type: 'audio/webm' });
                    const formData = new FormData();
                    formData.append('audio', blob);
                    
                    const response = await fetch('/procesar-voz', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    document.getElementById('vozTexto').textContent = data.texto || 'No se entendió';
                };
                
                mediaRecorder.start();
                setTimeout(() => mediaRecorder.stop(), 3000);
                setTimeout(() => stream.getTracks().forEach(track => track.stop()), 4000);
            } catch (err) {
                mostrarFeedback('Error al acceder al micrófono', 'error');
            }
        }
        
        function grabarPronunciacion(correcta) {
            mostrarFeedback('🎤 Pronuncia la palabra...', 'success');
            // Implementación similar a grabarVoz pero comparando con la palabra correcta
        }
        
        function mostrarFeedback(msg, tipo) {
            const feedbackDiv = document.createElement('div');
            feedbackDiv.className = `feedback ${tipo}`;
            feedbackDiv.textContent = msg;
            document.getElementById('contenido').prepend(feedbackDiv);
            setTimeout(() => feedbackDiv.remove(), 3000);
        }
        
        function logout() {
            window.location.href = '/logout';
        }
        
        // Cargar datos iniciales
        cargarDatos();
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)