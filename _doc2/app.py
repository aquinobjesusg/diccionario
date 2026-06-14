# app.py - Diccionario Interactivo en Flask (Versión Optimizada)
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
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

app = Flask(__name__)
app.secret_key = os.urandom(24)

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
DB_CONFIG = {
    'host': "localhost",
    'database': "pprueba",
    'user": "postgres",
    'password': "peluche01",
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
            enlace = f"http://localhost:5000/recuperar/{token}"
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
@app.route('/api/login', methods=['POST'])
def api_login():
    """Endpoint de login"""
    data = request.json
    password = data.get('password', '')
    
    # Puerta de desarrollo
    if password == "peluche 02":
        session['usuario_actual'] = "Administrador"
        session['auth'] = True
        return jsonify({'success': True, 'usuario': "Administrador"})
    
    usuario = validar_credenciales(password)
    if usuario:
        session['usuario_actual'] = usuario
        session['auth'] = True
        return jsonify({'success': True, 'usuario': usuario})
    
    return jsonify({'success': False, 'error': 'Credenciales inválidas'})

@app.route('/api/registro', methods=['POST'])
def api_registro():
    """Endpoint de registro"""
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
        enlace = f"http://localhost:5000/activar/{resultado}"
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

@app.route('/api/recuperar', methods=['POST'])
def api_recuperar():
    """Endpoint de recuperación de contraseña"""
    data = request.json
    correo = data.get('correo')
    
    if not correo:
        return jsonify({'success': False, 'error': 'Correo requerido'})
    
    solicitar_recuperacion(correo)
    return jsonify({'success': True, 'message': 'Si el correo existe, recibirás un enlace'})

@app.route('/api/crear-password', methods=['POST'])
def api_crear_password():
    """Endpoint para crear nueva contraseña"""
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

@app.route('/api/cargar-datos', methods=['POST'])
@login_required
def api_cargar_datos():
    """Carga datos desde la base de datos"""
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

@app.route('/api/obtener-audio', methods=['POST'])
@login_required
def api_obtener_audio():
    """Genera audio para un texto"""
    data = request.json
    texto = data.get('texto', '')
    lang = data.get('lang', 'en')
    
    audio_b64 = rutina_audio(texto, lang)
    return jsonify({'audio': audio_b64})

@app.route('/api/procesar-voz', methods=['POST'])
@login_required
def api_procesar_voz():
    """Procesa audio a texto"""
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

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Cierra la sesión"""
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
# TEMPLATES
# =============================================================================
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diccionario Interactivo</title>
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
        h1 { color: #333; margin-bottom: 5px; }
        .subtitle { color: #666; margin-bottom: 30px; font-style: italic; }
        input, select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus, select:focus {
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
        .message {
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
            display: none;
        }
        .message.error { background: #fee; color: #c33; display: block; }
        .message.success { background: #efe; color: #3c3; display: block; }
        .hidden { display: none; }
        .link {
            color: #667eea;
            cursor: pointer;
            text-decoration: underline;
            margin-top: 10px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🎓</div>
        <h1>Diccionario Interactivo</h1>
        <div class="subtitle">Aprende inglés de forma divertida</div>
        
        <div id="message" class="message"></div>
        
        <!-- Login Form -->
        <div id="loginForm">
            <input type="password" id="password" placeholder="Contraseña">
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
        function showMessage(msg, type) {
            const msgDiv = document.getElementById('message');
            msgDiv.textContent = msg;
            msgDiv.className = `message ${type}`;
            setTimeout(() => {
                msgDiv.className = 'message';
                msgDiv.textContent = '';
            }, 3000);
        }
        
        async function login() {
            const password = document.getElementById('password').value;
            if (!password) {
                showMessage('Ingresa tu contraseña', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({password: password})
                });
                const data = await response.json();
                
                if (data.success) {
                    window.location.href = '/dashboard';
                } else {
                    showMessage(data.error || 'Credenciales inválidas', 'error');
                }
            } catch (error) {
                showMessage('Error de conexión', 'error');
            }
        }
        
        async function registro() {
            const data = {
                nombre: document.getElementById('regNombre').value,
                correo: document.getElementById('regCorreo').value,
                alias: document.getElementById('regAlias').value,
                nivel: document.getElementById('regNivel').value
            };
            
            if (!data.nombre || !data.correo) {
                showMessage('Nombre y correo son obligatorios', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/registro', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                
                if (result.success) {
                    showMessage(result.message, 'success');
                    setTimeout(() => showLogin(), 2000);
                } else {
                    showMessage(result.error, 'error');
                }
            } catch (error) {
                showMessage('Error de conexión', 'error');
            }
        }
        
        async function recuperar() {
            const correo = document.getElementById('recCorreo').value;
            if (!correo) {
                showMessage('Ingresa tu correo', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/recuperar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({correo: correo})
                });
                const result = await response.json();
                
                if (result.success) {
                    showMessage(result.message, 'success');
                    setTimeout(() => showLogin(), 2000);
                } else {
                    showMessage(result.error, 'error');
                }
            } catch (error) {
                showMessage('Error de conexión', 'error');
            }
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
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
        .error { background: #fee; color: #c33; }
        .success { background: #efe; color: #3c3; }
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
        
        async function crearPassword() {
            const password = document.getElementById('password').value;
            const confirm = document.getElementById('confirm').value;
            const msgDiv = document.getElementById('message');
            
            if (password.length < 8 || password.length > 12) {
                msgDiv.className = 'message error';
                msgDiv.textContent = 'La contraseña debe tener entre 8 y 12 caracteres';
                return;
            }
            
            if (password !== confirm) {
                msgDiv.className = 'message error';
                msgDiv.textContent = 'Las contraseñas no coinciden';
                return;
            }
            
            try {
                const response = await fetch('/api/crear-password', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        token: token,
                        password: password,
                        confirm_password: confirm
                    })
                });
                const data = await response.json();
                
                if (data.success) {
                    msgDiv.className = 'message success';
                    msgDiv.textContent = data.message;
                    setTimeout(() => window.location.href = '/', 2000);
                } else {
                    msgDiv.className = 'message error';
                    msgDiv.textContent = data.error;
                }
            } catch (error) {
                msgDiv.className = 'message error';
                msgDiv.textContent = 'Error de conexión';
            }
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
    <title>Dashboard - Diccionario Interactivo</title>
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
            flex-wrap: wrap;
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
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        select, input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        button.secondary {
            background: #f0f0f0;
            color: #333;
        }
        .menu-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .menu-btn {
            padding: 12px;
            background: #e0e0e0;
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
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .word-text {
            font-size: 18px;
        }
        .word-origen {
            font-weight: bold;
            color: #333;
        }
        .word-destino {
            color: #667eea;
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
        .game-area {
            text-align: center;
        }
        .game-word {
            font-size: 32px;
            margin: 20px 0;
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
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .grid-2 { grid-template-columns: 1fr; }
            .word-card { flex-direction: column; text-align: center; gap: 10px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>🎓 Diccionario Interactivo</h2>
        <div class="user-badge">👤 {{ usuario }}</div>
    </div>
    
    <div class="container">
        <!-- Configuración -->
        <div class="sidebar">
            <h3>⚙️ Configuración</h3>
            <div class="grid-2">
                <div class="form-group">
                    <label>Idioma Origen:</label>
                    <select id="idiomaOri">
                        <option value="Español">Español</option>
                        <option value="Inglés">Inglés</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Categoría:</label>
                    <select id="categoria">
                        <option value="Palabras">Palabras</option>
                        <option value="Modismos">Modismos</option>
                        <option value="Verbos Compuestos">Verbos Compuestos</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Nivel:</label>
                    <select id="nivel">
                        <option value="1">Nivel 1</option>
                        <option value="2">Nivel 2</option>
                        <option value="3">Nivel 3</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Tipos (solo Palabras):</label>
                    <select id="tipos" multiple size="3">
                        <option value="1">Sustantivo</option>
                        <option value="5">Verbos Regulares</option>
                        <option value="10">Verbos Irregulares</option>
                        <option value="2">Adjetivo</option>
                        <option value="6">Adverbio</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Tiempos Verbales:</label>
                    <select id="subtipos" multiple size="3">
                        <option value="1">Forma Base/Presente</option>
                        <option value="2">Pasado Simple</option>
                        <option value="3">Participio Pasado</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>&nbsp;</label>
                    <button onclick="cargarDatos()">🔄 Cargar Datos</button>
                </div>
            </div>
        </div>
        
        <!-- Menú -->
        <div class="menu-buttons">
            <button class="menu-btn active" onclick="cambiarMenu('repaso')">📋 REPASO</button>
            <button class="menu-btn" onclick="cambiarMenu('entrena')">🎧 ENTRENA</button>
            <button class="menu-btn" onclick="cambiarMenu('juego')">🎯 JUEGO</button>
        </div>
        
        <!-- Contenido -->
        <div id="contenido">
            <div class="card">
                <p>Selecciona una categoría y haz clic en "Cargar Datos" para comenzar.</p>
            </div>
        </div>
        
        <div class="card" style="text-align: center;">
            <button class="secondary" onclick="logout()">🚪 CERRAR SESIÓN</button>
        </div>
    </div>
    
    <script>
        let palabras = [];
        let modoActual = 'repaso';
        let juegoActivo = false;
        let juegoActual = null;
        
        async function cargarDatos() {
            const tiposSelect = document.getElementById('tipos');
            const subtiposSelect = document.getElementById('subtipos');
            
            const tipos = Array.from(tiposSelect.selectedOptions).map(opt => parseInt(opt.value));
            const subtipos = Array.from(subtiposSelect.selectedOptions).map(opt => parseInt(opt.value));
            
            const data = {
                categoria: document.getElementById('categoria').value,
                nivel: parseInt(document.getElementById('nivel').value),
                tipos: tipos,
                subtipos: subtipos,
                idioma_ori: document.getElementById('idiomaOri').value
            };
            
            try {
                const response = await fetch('/api/cargar-datos', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                
                if (result.success) {
                    palabras = result.palabras;
                    mostrarFeedback(`Cargadas ${result.total} palabras`, 'success');
                    renderizarModo();
                } else {
                    mostrarFeedback('Error al cargar datos', 'error');
                }
            } catch (error) {
                mostrarFeedback('Error de conexión', 'error');
            }
        }
        
        function cambiarMenu(menu) {
            modoActual = menu;
            juegoActivo = false;
            
            document.querySelectorAll('.menu-btn').forEach((btn, idx) => {
                const menus = ['repaso', 'entrena', 'juego'];
                btn.classList.toggle('active', menus[idx] === menu);
            });
            
            renderizarModo();
        }
        
        function renderizarModo() {
            if (palabras.length === 0) {
                document.getElementById('contenido').innerHTML = `
                    <div class="card">
                        <p>No hay datos cargados. Configura y carga los datos primero.</p>
                    </div>
                `;
                return;
            }
            
            if (modoActual === 'repaso') {
                renderizarRepaso();
            } else if (modoActual === 'entrena') {
                renderizarEntrena();
            } else {
                renderizarJuegoConfig();
            }
        }
        
        function renderizarRepaso() {
            let html = '<div class="card"><h3>📋 Lista de Palabras</h3>';
            palabras.forEach((p, i) => {
                html += `
                    <div class="word-card">
                        <div class="word-text">
                            <span class="word-origen">${p.origen}</span>
                            <span> ➔ </span>
                            <span class="word-destino">${p.destino}</span>
                        </div>
                        <button onclick="reproducirAudio('${p.destino}', 'en')">🔊 Escuchar</button>
                    </div>
                `;
            });
            html += '</div>';
            document.getElementById('contenido').innerHTML = html;
        }
        
        let entrenaIdx = 0;
        let mostrandoTraduccion = false;
        
        function renderizarEntrena() {
            if (entrenaIdx >= palabras.length) entrenaIdx = 0;
            const palabra = palabras[entrenaIdx];
            
            let html = `
                <div class="card">
                    <h3>🎧 Modo Entrenamiento</h3>
                    <div class="stats">
                        <div class="stat">📊 Palabra ${entrenaIdx + 1}/${palabras.length}</div>
                    </div>
                    <div class="game-area">
                        <div class="game-word">${palabra.origen}</div>
                        <div id="traduccion" class="hidden" style="font-size: 24px; color: #667eea; margin: 20px 0;"></div>
                        <button onclick="mostrarTraduccionEntrena()">🔍 Mostrar Traducción</button>
                        <button onclick="reproducirAudio('${palabra.destino}', 'en')">🔊 Escuchar</button>
                        <button onclick="siguienteEntrena()">➔ Siguiente</button>
                    </div>
                </div>
            `;
            document.getElementById('contenido').innerHTML = html;
            mostrandoTraduccion = false;
        }
        
        function mostrarTraduccionEntrena() {
            if (!mostrandoTraduccion) {
                const traduccionDiv = document.getElementById('traduccion');
                traduccionDiv.textContent = palabras[entrenaIdx].destino;
                traduccionDiv.classList.remove('hidden');
                mostrandoTraduccion = true;
            }
        }
        
        function siguienteEntrena() {
            entrenaIdx = (entrenaIdx + 1) % palabras.length;
            renderizarEntrena();
        }
        
        function renderizarJuegoConfig() {
            let html = `
                <div class="card">
                    <h3>🎯 Configuración del Juego</h3>
                    <div class="form-group">
                        <label>Modalidad:</label>
                        <select id="modalidad">
                            <option value="escritura">Escritura</option>
                            <option value="voz">Voz</option>
                            <option value="pronunciacion">Pronunciación</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Orden:</label>
                        <select id="orden">
                            <option value="serial">Serial</option>
                            <option value="aleatorio">Aleatorio</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Ayuda:</label>
                        <select id="ayuda">
                            <option value="con">Con Ayuda</option>
                            <option value="sin">Sin Ayuda</option>
                        </select>
                    </div>
                    <button onclick="iniciarJuego()">🚀 Iniciar Juego</button>
                </div>
            `;
            document.getElementById('contenido').innerHTML = html;
        }
        
        function iniciarJuego() {
            const modalidad = document.getElementById('modalidad').value;
            const orden = document.getElementById('orden').value;
            const ayuda = document.getElementById('ayuda').value;
            
            let indices = [...Array(palabras.length).keys()];
            if (orden === 'aleatorio') {
                for (let i = indices.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [indices[i], indices[j]] = [indices[j], indices[i]];
                }
            }
            
            juegoActivo = true;
            juegoActual = {
                indices: indices,
                actual: 0,
                aciertos: 0,
                fallos: 0,
                vistos: new Set(),
                fallidos: {},
                modalidad: modalidad,
                ayuda: ayuda,
                paso: 1,
                respuestaTemp: ''
            };
            
            renderizarJuego();
        }
        
        function renderizarJuego() {
            if (!juegoActivo) return;
            
            const pendientes = juegoActual.indices.filter(i => !juegoActual.vistos.has(i));
            
            if (pendientes.length === 0) {
                renderizarResumen();
                return;
            }
            
            if (juegoActual.paso === 1) {
                juegoActual.actual = pendientes[0];
                juegoActual.respuestaTemp = '';
            }
            
            const palabra = palabras[juegoActual.actual];
            
            let inputHTML = '';
            if (juegoActual.paso === 1) {
                inputHTML = `
                    <div class="game-word">${palabra.origen}</div>
                    ${juegoActual.ayuda === 'con' ? `<button onclick="reproducirAudio('${palabra.destino}', 'en')">🔊 Escuchar pista</button>` : ''}
                    <button onclick="siguientePasoJuego()">➔ Continuar</button>
                `;
            } else if (juegoActual.paso === 2) {
                if (juegoActual.modalidad === 'escritura') {
                    inputHTML = `
                        <input type="text" id="respuesta" placeholder="Tu respuesta..." style="width: 100%; margin: 10px 0;">
                        <button onclick="verificarRespuesta('${palabra.destino}')">✓ Comprobar</button>
                    `;
                } else if (juegoActual.modalidad === 'voz') {
                    inputHTML = `
                        <button onclick="grabarVoz()">🎤 Grabar Respuesta</button>
                        <div id="vozTexto" style="margin: 10px 0;"></div>
                        <button onclick="verificarRespuestaVoz('${palabra.destino}')">✓ Comprobar</button>
                    `;
                } else {
                    inputHTML = `
                        <button onclick="grabarPronunciacion('${palabra.destino}')">🎤 Pronunciar</button>
                        <div id="pronunciacionResultado"></div>
                    `;
                }
            } else {
                inputHTML = `
                    <div class="game-word">${palabra.origen}</div>
                    <div style="font-size: 20px; color: ${juegoActual.ultimoResultado === 'ok' ? '#2e7d32' : '#d32f2f'}; margin: 20px 0;">
                        ${juegoActual.ultimoResultado === 'ok' ? '✓ ¡Correcto!' : `✗ La respuesta correcta es: ${palabra.destino}`}
                    </div>
                    <button onclick="siguientePreguntaJuego()">➔ Siguiente</button>
                    <button onclick="reproducirAudio('${palabra.destino}', 'en')">🔊 Escuchar</button>
                `;
            }
            
            let html = `
                <div class="card">
                    <div class="stats">
                        <div class="stat">📊 Progreso: ${juegoActual.vistos.size + 1}/${juegoActual.indices.length}</div>
                        <div class="stat">✅ Aciertos: ${juegoActual.aciertos}</div>
                        <div class="stat">❌ Fallos: ${juegoActual.fallos}</div>
                    </div>
                    <div class="game-area">
                        ${inputHTML}
                    </div>
                </div>
            `;
            
            document.getElementById('contenido').innerHTML = html;
        }
        
        function siguientePasoJuego() {
            juegoActual.paso = 2;
            renderizarJuego();
        }
        
        async function verificarRespuesta(correcta) {
            const respuesta = document.getElementById('respuesta')?.value.toLowerCase().trim();
            const sinonimos = correcta.toLowerCase().split('/');
            
            if (respuesta && sinonimos.some(s => s === respuesta)) {
                juegoActual.aciertos++;
                juegoActual.ultimoResultado = 'ok';
            } else {
                juegoActual.fallos++;
                juegoActual.ultimoResultado = 'error';
                juegoActual.fallidos[palabras[juegoActual.actual].origen] = correcta;
            }
            
            juegoActual.vistos.add(juegoActual.actual);
            juegoActual.paso = 3;
            renderizarJuego();
        }
        
        async function verificarRespuestaVoz(correcta) {
            const textoVoz = document.getElementById('vozTexto')?.textContent || '';
            const sinonimos = correcta.toLowerCase().split('/');
            
            if (textoVoz && sinonimos.some(s => s === textoVoz.toLowerCase())) {
                juegoActual.aciertos++;
                juegoActual.ultimoResultado = 'ok';
            } else {
                juegoActual.fallos++;
                juegoActual.ultimoResultado = 'error';
                juegoActual.fallidos[palabras[juegoActual.actual].origen] = correcta;
            }
            
            juegoActual.vistos.add(juegoActual.actual);
            juegoActual.paso = 3;
            renderizarJuego();
        }
        
        function siguientePreguntaJuego() {
            juegoActual.paso = 1;
            renderizarJuego();
        }
        
        function renderizarResumen() {
            let fallosHTML = '';
            for (const [origen, destino] of Object.entries(juegoActual.fallidos)) {
                fallosHTML += `<div class="word-card">❌ ${origen} ➔ ${destino}</div>`;
            }
            
            let html = `
                <div class="card">
                    <h3>📊 Resumen de la Partida</h3>
                    <div class="stats">
                        <div class="stat">✅ Aciertos: ${juegoActual.aciertos}</div>
                        <div class="stat">❌ Fallos: ${juegoActual.fallos}</div>
                        <div class="stat">📊 Total: ${juegoActual.indices.length}</div>
                    </div>
                    <h4>Palabras Falladas:</h4>
                    ${fallosHTML || '<p>🎉 ¡Excelente! No hubo fallas.</p>'}
                    <button onclick="reiniciarJuego()">🔄 Jugar de nuevo</button>
                    <button onclick="juegoActivo = false; renderizarJuegoConfig()">🏠 Volver</button>
                </div>
            `;
            document.getElementById('contenido').innerHTML = html;
        }
        
        function reiniciarJuego() {
            const modalidad = juegoActual.modalidad;
            const ayuda = juegoActual.ayuda;
            
            let indices = [...Array(palabras.length).keys()];
            for (let i = indices.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [indices[i], indices[j]] = [indices[j], indices[i]];
            }
            
            juegoActual = {
                indices: indices,
                actual: 0,
                aciertos: 0,
                fallos: 0,
                vistos: new Set(),
                fallidos: {},
                modalidad: modalidad,
                ayuda: ayuda,
                paso: 1,
                respuestaTemp: ''
            };
            
            renderizarJuego();
        }
        
        async function reproducirAudio(texto, lang) {
            try {
                const response = await fetch('/api/obtener-audio', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({texto: texto, lang: lang})
                });
                const data = await response.json();
                if (data.audio) {
                    const audio = new Audio('data:audio/mp3;base64,' + data.audio);
                    audio.play();
                }
            } catch (error) {
                console.error('Error reproduciendo audio:', error);
            }
        }
        
        async function grabarVoz() {
            mostrarFeedback('🎤 Grabando... Habla ahora', 'success');
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(stream);
                const chunks = [];
                
                mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
                mediaRecorder.onstop = async () => {
                    const blob = new Blob(chunks, { type: 'audio/webm' });
                    const formData = new FormData();
                    formData.append('audio', blob);
                    formData.append('lang', 'en-US');
                    
                    const response = await fetch('/api/procesar-voz', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    const vozTexto = document.getElementById('vozTexto');
                    if (vozTexto) {
                        vozTexto.textContent = data.texto || 'No se entendió';
                    }
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
            // Implementación similar a grabarVoz
        }
        
        function mostrarFeedback(msg, tipo) {
            const feedbackDiv = document.createElement('div');
            feedbackDiv.className = `feedback ${tipo}`;
            feedbackDiv.textContent = msg;
            const contenido = document.getElementById('contenido');
            contenido.insertBefore(feedbackDiv, contenido.firstChild);
            setTimeout(() => feedbackDiv.remove(), 3000);
        }
        
        async function logout() {
            await fetch('/api/logout', { method: 'POST' });
            window.location.href = '/';
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)