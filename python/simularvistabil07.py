import streamlit as st
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

# =============================================================================
# BLOQUE 0: CONFIGURACIÓN Y ESTILOS GLOBALES
# =============================================================================
def convertir_mic_a_texto(audio_streamlit):
    """Convierte el audio del widget de Streamlit en texto en inglés"""
    r = sr.Recognizer()
    try:
        # Convertimos el archivo de Streamlit para que speech_recognition lo entienda
        with sr.AudioFile(audio_streamlit) as source:
            audio_data = r.record(source)
        # Usamos la función de Google especificando que es inglés (en-US)
        texto = r.recognize_google(audio_data, language="en-US")
        return texto
    except Exception:
        # Si no entiende el audio o no hay internet, devuelve un texto vacío
        return ""
def aplicar_configuracion_estetica():
    """Configura el layout y los estilos CSS personalizados del aplicativo."""
    st.set_page_config(page_title="Diccionario Interactivo", layout="wide")
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { background-color: #000000 !important; }
        [data-testid="stSidebar"] label p { color: #FFFFFF !important; font-weight: 900 !important; }
        
        div[data-baseweb="select"] > div, div[data-baseweb="base-input"] > input,
        div[data-testid="stMultiSelect"] > div, div[data-testid="stNumberInput"] input {
            background-color: #FFFFFF !important; color: #000000 !important; font-weight: 900 !important;
        }

        .count-label { color: #FFEB3B; font-weight: 900; font-size: 18px; display: block; text-align: center; margin: 10px 0; }
        .modo-reforzando { background-color: #FFD600; color: #000; padding: 10px; border-radius: 5px; text-align: center; font-weight: 900; margin: 10px 0; border: 2px solid #000; }
        .modo-aviso { background-color: #D32F2F; color: #FFF; padding: 10px; border-radius: 5px; text-align: center; font-weight: 900; margin-bottom: 10px; border: 2px solid #FFF; }
        .main-header { background: #0044CC; color: white; padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #000; position: relative; margin-top: -20px; }
        .timer-box { position: absolute; top: 5px; right: 10px; background: #000; color: #FFEB3B; padding: 2px 8px; border-radius: 5px; font-family: monospace; font-weight: 900; }
        .stat-box { background: #f0f0f0; border: 1px solid #ccc; padding: 5px; border-radius: 5px; text-align: center; font-weight: 900; color: #000; }
        .word-box { background-color: #FDFDFD; padding: 25px; border-radius: 15px; border-left: 12px solid #FFD600; color: #000; box-shadow: 4px 4px 10px rgba(0,0,0,0.1); }
        
        .stApp { background-color: #E0E0E0 !important; }
        
        .auth-card {
            background-color: #F5F5F5;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
            text-align: center;
            border: 1px solid #CCC;
        }
        .logo-bg {
            background-color: white;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px auto;
            font-size: 70px;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
        }
        .app-title { color: #0044CC; font-weight: 900; margin-bottom: 5px; }
        .app-subtitle { color: #555; font-style: italic; margin-bottom: 30px; }
        </style>
        """, unsafe_allow_html=True)

# =============================================================================
# BLOQUE 1: UTILIDADES DE COMUNICACIÓN (EMAIL)
# =============================================================================

def ejecutar_envio_mail(remitente, password_app, destino, asunto, cuerpo):
    """Función de bajo nivel para envío de correos vía SMTP."""
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
        st.error(f"Error al enviar correo: {e}")
        return False

def enviar_correo_activacion(correo_destino, nombre_usuario, token):
    """Genera y envía el correo para activación de cuenta nueva."""
    remitente = "edwinreyes308@gmail.com" 
    password_app = "nlco hjxd wjzi srei" 
    enlace = f"http://localhost:8501/?token={token}"
    
    asunto = "🎓 Activa tu cuenta - Diccionario Interactivo"
    cuerpo = f"""Hola {nombre_usuario},
    
¡Gracias por registrarte! Para completar tu perfil y crear tu contraseña 
personal, por favor haz clic en el siguiente enlace:

{enlace}

Este enlace es de un solo uso."""
    
    return ejecutar_envio_mail(remitente, password_app, correo_destino, asunto, cuerpo)

def enviar_correo_recuperacion(correo_destino, nombre_usuario, token):
    """Genera y envía el correo para recuperación de contraseña."""
    remitente = "edwinreyes308@gmail.com" 
    password_app = "nlco hjxd wjzi srei" 
    enlace = f"http://localhost:8501/?token={token}"
    
    asunto = "🔑 Restablecer tu contraseña - Diccionario Interactivo"
    cuerpo = f"""Hola {nombre_usuario},
    
Hemos recibido una solicitud para restablecer tu contraseña en el Diccionario Interactivo.
Para crear una nueva clave, haz clic en el siguiente enlace:

{enlace}

Si no solicitaste este cambio, puedes ignorar este correo de forma segura."""
    
    return ejecutar_envio_mail(remitente, password_app, correo_destino, asunto, cuerpo)

# =============================================================================
# BLOQUE 2: GESTIÓN DE SEGURIDAD Y BASE DE DATOS
# =============================================================================

def proceso_solicitar_recuperacion(correo):
    """Maneja la lógica de validación de correo y envío de token a la BD."""
    try:
        token = secrets.token_urlsafe(16)
        conn = psycopg2.connect(host="localhost", database="pprueba", user="postgres", password="password2017", port="5432")
        cur = conn.cursor()
        
        cur.execute("SELECT nombre FROM usuarios WHERE correo = %s AND estado = 'ACTIVO'", (correo.strip(),))
        resultado = cur.fetchone()
        
        if resultado:
            nombre_usuario = resultado[0]
            cur.execute("UPDATE usuarios SET token_verificacion = %s WHERE correo = %s", (token, correo.strip()))
            conn.commit()
            
            if enviar_correo_recuperacion(correo.strip(), nombre_usuario, token):
                cur.close(); conn.close()
                return True
        
        cur.close(); conn.close()
        return False 
    except Exception as e:
        st.error(f"Error en BD: {e}")
        return False

# =============================================================================
# BLOQUE 3: COMPONENTES DE INTERFAZ (UI)
# =============================================================================

def mostrar_identidad_usuario():
    """Muestra el banner de sesión activa en la parte superior."""
    usuario = st.session_state.get('usuario_actual') or st.session_state.get('user_name') or "USUARIO"
    es_admin = str(usuario).upper() == "ADMINISTRADOR"
    color_borde = "#FFD700" if es_admin else "#11caa0"
    
    st.markdown(f"""
        <div class="banner-identidad-superior">
            <span style="color: {color_borde};">● SESIÓN ACTIVA</span>
            <span style="letter-spacing: 1.5px;">{usuario}</span>
        </div>
    """, unsafe_allow_html=True)

def pantalla_crear_password(token):
    """Pantalla para que el usuario defina su clave mediante un token de URL."""
    st.markdown('<h2 style="text-align: center;">🔑 Crear Nueva Contraseña</h2>', unsafe_allow_html=True)
    
    try:
        conn = psycopg2.connect(host="localhost", database="pprueba", user="postgres", password="password2017", port="5432")
        cur = conn.cursor()
        cur.execute("SELECT correo, nombre FROM usuarios WHERE token_verificacion = %s", (token,))
        usuario = cur.fetchone()
        
        if not usuario:
            st.error("❌ El enlace es inválido o ya fue usado.")
            if st.button("Volver al Inicio"):
                st.query_params.clear()
                st.rerun()
            return

        correo_user, nombre_user = usuario
        st.info(f"Hola **{nombre_user}**, define tu nueva clave de acceso.")

        with st.form("form_nueva_clave"):
            nueva_pass = st.text_input("Nueva Contraseña (8-12 caracteres):", type="password")
            confirm_pass = st.text_input("Confirma tu Contraseña:", type="password")
            btn_guardar = st.form_submit_button("GUARDAR CONTRASEÑA", use_container_width=True)

            if btn_guardar:
                if 8 <= len(nueva_pass) <= 12:
                    if nueva_pass == confirm_pass:
                        query_update = """
                            UPDATE usuarios SET clave = %s, estado = 'ACTIVO', token_verificacion = NULL 
                            WHERE token_verificacion = %s
                        """
                        cur.execute(query_update, (nueva_pass, token))
                        conn.commit()
                        st.success("✅ ¡Contraseña actualizada con éxito!")
                        st.balloons()
                        time.sleep(3)
                        st.query_params.clear()
                        st.session_state.auth_step = 'login'
                        st.rerun()
                    else:
                        st.warning("Las contraseñas no coinciden.")
                else:
                    st.warning("La contraseña debe tener entre 8 y 12 caracteres.")
        
        cur.close(); conn.close()
    except Exception as e:
        st.error(f"Error de conexión: {e}")
# =============================================================================
# BLOQUE 4: GESTIÓN DE ACCESO Y SEGURIDAD (EL PORTERO)
# =============================================================================

def registrar_usuario_inicial(nombre, alias, correo, nivel_texto):
    """Registra al usuario en estado PENDIENTE y genera el token de activación."""
    try:
        token = secrets.token_urlsafe(16)
        conn = psycopg2.connect(
            host="localhost", database="pprueba", user="postgres", password="password2017", port="5432"
        )
        cur = conn.cursor()
        
        # Lógica para Alias: si está vacío, usamos parte del nombre
        ali_final = alias.strip() if (alias and alias.strip()) else nombre.replace(" ", "")[:10]
        
        query = """
            INSERT INTO usuarios (nombre, alias, correo, nivel, token_verificacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'PENDIENTE')
        """
        cur.execute(query, (nombre.strip(), ali_final, correo.strip(), nivel_texto, token))
        
        conn.commit()
        cur.close(); conn.close()
        return True, token
    except Exception as e:
        return False, f"Error detallado: {e}"

def validar_credenciales_db(password_ingresada):
    """Valida la clave contra la base de datos para usuarios ACTIVOS."""
    try:
        conn = psycopg2.connect(
            host="localhost", database="pprueba", user="postgres", password="password2017", port="5432"
        )
        cur = conn.cursor()
        
        query = "SELECT nombre, alias FROM usuarios WHERE clave = %s AND estado = 'ACTIVO'"
        cur.execute(query, (password_ingresada.strip(),))
        registro = cur.fetchone()
        cur.close(); conn.close()
        
        if registro:
            # Guardamos el alias (o nombre) en la sesión
            st.session_state['usuario_actual'] = registro[1] if registro[1] else registro[0]
            return True
        return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# =============================================================================
# BLOQUE 5: INTERFAZ DE SEGURIDAD (PANTALLAS)
# =============================================================================

def pantalla_seguridad():
    """Maneja el flujo visual de Login, Registro y Recuperación."""
    if 'auth_step' not in st.session_state:
        st.session_state.auth_step = 'inicio'

    col_main_1, col_main_2, col_main_3 = st.columns([1, 2, 1])
    
    with col_main_2:
        st.markdown('<div style="font-size: 80px; text-align: center; margin-bottom: 10px;">🎓</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center;">❌ DICCIONARIO INTERACTIVO ❌ </h2>', unsafe_allow_html=True)
        st.markdown('---')

        # --- ESTADO: BOTONES PRINCIPALES ---
        if st.session_state.auth_step == 'inicio':
            if st.button("INICIAR SESIÓN", use_container_width=True, key="btn_init_login"):
                st.session_state.auth_step = 'login'
                st.rerun()
            if st.button("CREAR UNA CUENTA", use_container_width=True, key="btn_init_reg"):
                st.session_state.auth_step = 'registro'
                st.rerun()

        # --- ESTADO: LOGIN ---
        elif st.session_state.auth_step == 'login':
            st.write("### 🔐 Ingreso de Usuario")
            password = st.text_input("Contraseña:", type="password", key="login_pass_input")
            
            if st.button("ENTRAR", use_container_width=True, key="btn_login_submit"):
                if password == "peluche 02": # Puerta de desarrollo
                    st.session_state['usuario_actual'] = "Administrador"
                    st.session_state['auth'] = True
                    st.rerun()
                elif validar_credenciales_db(password):
                    st.session_state['auth'] = True
                    st.rerun()
                else:
                    st.error("Credenciales inválidas o cuenta pendiente de activación.")
            
            if st.button("¿Olvidaste tu contraseña?", key="btn_forgot_pass"):
                st.session_state.auth_step = 'recuperar'
                st.rerun()
            
            if st.button("VOLVER", key="btn_login_back"):
                st.session_state.auth_step = 'inicio'
                st.rerun()

        # --- ESTADO: RECUPERAR CONTRASEÑA ---
        elif st.session_state.auth_step == 'recuperar':
            st.write("### 🔑 Recuperar Acceso")
            correo_recu = st.text_input("Introduce tu correo registrado:", key="recovery_email_input")
            
            if st.button("ENVIAR ENLACE DE RECUPERACIÓN", use_container_width=True, key="btn_recovery_submit"):
                if not correo_recu:
                    st.warning("Escribe tu correo.")
                else:
                    if proceso_solicitar_recuperacion(correo_recu):
                        st.success("Si el correo existe, recibirás un enlace en breve.")
                        time.sleep(3)
                        st.session_state.auth_step = 'inicio'
                        st.rerun()

            if st.button("VOLVER AL LOGIN", key="btn_recovery_back"):
                st.session_state.auth_step = 'inicio'
                st.rerun()

        # --- ESTADO: REGISTRO ---
        elif st.session_state.auth_step == 'registro':
            st.write("### 📝 Registro de Nuevo Usuario")
            nom = st.text_input("Nombre Completo:", key="reg_nom")
            cor = st.text_input("Correo Electrónico:", key="reg_cor")
            ali = st.text_input("Alias (Nombre de usuario):", key="reg_ali")
            niv = st.selectbox("Nivel de Inglés:", ["Básico", "Intermedio", "Avanzado"], key="reg_niv")
            
            if st.button("REGISTRARSE", use_container_width=True, key="btn_reg_submit"):
                if not nom or not cor:
                    st.warning("El nombre y el correo son obligatorios.")
                else:
                    exito, resultado_token = registrar_usuario_inicial(nom, ali, cor, niv)
                    if exito:
                        if enviar_correo_activacion(cor, nom, resultado_token):
                            st.success(f"¡Registro exitoso! Revisa tu correo: {cor}")
                        else:
                            st.warning("Usuario registrado, pero hubo un problema enviando el correo.")
                        time.sleep(4)
                        st.session_state.auth_step = 'inicio'
                        st.rerun()
                    else:
                        st.error(resultado_token)
            
            if st.button("CANCELAR", key="btn_reg_cancel"):
                st.session_state.auth_step = 'inicio'
                st.rerun()
                
def procesar_voz_laboratorio(idioma_code):
    """
    Captura el audio del micrófono y lo convierte a texto.
    idioma_code: 'en-US' para inglés o 'es-ES' para español.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Ajuste para el ruido ambiental
        r.adjust_for_ambient_noise(source, duration=0.5)
        st.toast("🎤 Escuchando... ¡Habla ahora!", icon="👂")
        
        try:
            # Captura el audio con un límite de tiempo para que no se quede colgado
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            st.text("⌛ Procesando voz...")
            texto = r.recognize_google(audio, language=idioma_code)
            return texto
        except sr.WaitTimeoutError:
            st.warning("⚠️ No se detectó voz. Intenta de nuevo.")
            return None
        except sr.UnknownValueError:
            st.error("❌ No logré entender el audio. ¿Podrías repetir?")
            return None
        except Exception as e:
            st.error(f"Error técnico con el micrófono: {e}")
            return None
#===================================================================
# BLOQUE 3: EL MOTOR DEL APLICATIVO (LOGICA DE MENÚS Y AUTO-ENTRENA)
# =============================================================================

# ==========================================
# BLOQUE 2: EL APLICATIVO (CAJA NEGRA) - ORGANIZADO
# ==========================================
def ejecutar_aplicativo_principal():
    # --- 1. Inicialización de Estado ---
    if 'data' not in st.session_state:
        st.session_state.update({
            'data': [], 'total_p': 0, 'jugando': False, 'menu_actual': "REPASO",
            'idx_entrena': 0, 'ent_step': 0, 'j_paso': 1, 'j_vistos': set(), 
            'j_fallidos_dict': {}, 'cat_activa': "PALABRAS", 'niv_activo': 1, 'idioma_ori': "Español",
            'r_ini': 1, 'r_fin': 20, 'modo_falla_activo': False, 'subset_fallas': [], 't_inicio': 0,
            'viendo_resumen': False, 'ayuda_juego': "Con Ayuda", 'input_voz': "", 'mod_j': "Escritura",
            'auto_entrena': False
        })

    # --- 2. Sub-rutinas Internas (Cargadas una sola vez) ---
    def rutina_audio(texto, lang):
        if not texto: return
        try:
            tts = gTTS(text=texto, lang=lang); fp = io.BytesIO(); tts.write_to_fp(fp)
            b64 = base64.b64encode(fp.getvalue()).decode()
            st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
        except: pass

    def obtener_par(idx, lista, col, ori):
        if not lista or idx+1 >= len(lista): return "---", "---", 'en', ""
        p1, p2 = lista[idx][col], lista[idx+1][col]
        return (p2, p1, 'en', "") if ori == "Español" else (p1, p2, 'es', "")

    def rutina_cargar_db(categoria, nivel, tipos_sel):
        try:
            conn = psycopg2.connect(host="localhost", database="pprueba", user="postgres", password="password2017", port="5432")
            cur = conn.cursor()
            mapeo = {"Palabras": ("palabras", "id_palabra", 4, "id_tipo_palabra"),
                     "Modismos": ("modismos", "id_modismo", 3, None),
                     "Verbos Compuestos": ("verbos_compuestos", "id_verbo", 3, None)}
            if categoria not in mapeo: return [], 0
            tabla, id_col, col_idx, col_tipo = mapeo[categoria]
            query = f"SELECT * FROM {tabla} WHERE id_nivel = %s "
            params = [int(nivel)]
            if col_tipo and tipos_sel:
                query += f"AND {col_tipo} IN ({','.join(['%s']*len(tipos_sel))}) "
                params.extend(tipos_sel)
            query += f"ORDER BY {id_col}"
            cur.execute(query, tuple(params))
            datos = cur.fetchall()
            cur.close(); conn.close()
            return datos, col_idx
        except Exception as e:
            st.error(f"Error DB: {e}"); return [], 0

    # --- 3. Panel Lateral (Sidebar) ---
    with st.sidebar:
        #st.subheader("⚙️ PANEL DE CONTROL")
        st.markdown('<h2 style="text-align: center;">⚙️ PANEL DE CONTROL</h2>', unsafe_allow_html=True)

        if not st.session_state.jugando:
            habla = st.selectbox("Idioma Origen:", ["Español", "Inglés"], key="sb_idioma_origen")
            cat = st.selectbox("Categoría:", ["Palabras", "Modismos", "Verbos Compuestos"])
            t_sel = []
            if cat == "Palabras":
                opciones = {"Sustantivo (1)": 1, "Adjetivo (2)": 2, "Determinante (3)": 3, "Pronombre (4)": 4, "Verbo (5)": 5, "Adverbio (6)": 6, "Preposición (7)": 7, "Conjunción (8)": 8, "Interjección (9)": 9}
                t_sel = [opciones[s] for s in st.multiselect("Tipos:", list(opciones.keys()), default=["Sustantivo (1)"])]
            niv_sel = st.radio("NIVEL:", ["NIVEL 1", "NIVEL 2", "NIVEL 3"], horizontal=True)
            nivel_num = int(niv_sel.split()[-1])
            
            if st.button("🔄 CARGAR / ACTUALIZAR NUEVA DATA"):
                res, col = rutina_cargar_db(cat, nivel_num, t_sel)
                st.session_state.update({
                    'data': res, 'col_idx': col, 'idioma_ori': habla, 'total_p': len(res)//2, 
                    'cat_activa': cat, 'niv_activo': nivel_num, 'menu_actual': "REPASO", 
                    'r_fin': min(20, len(res)//2), 'modo_falla_activo': False, 'idx_entrena': 0,
                    'subset_fallas': [], 'auto_entrena': False
                })
                st.rerun()
                
            if st.session_state.total_p > 0:
                if st.session_state.modo_falla_activo:
                    st.markdown('<div class="modo-reforzando">⚠️ MODO: REFORZANDO FALLAS</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="count-label">Total en DB: {st.session_state.total_p}</div>', unsafe_allow_html=True)
                    st.session_state.r_ini = st.number_input("Desde:", 1, st.session_state.total_p, value=st.session_state.r_ini)
                    st.session_state.r_fin = st.number_input("Hasta:", 1, st.session_state.total_p, value=st.session_state.r_fin)
            
            st.markdown("---")
            if st.button("🚪 CERRAR SESIÓN"):
                st.session_state['auth'] = False
                st.rerun()
        else:
            # st.markdown(f"<div class='modo-aviso'>{st.session_state.mod_j.upper()}</div>", unsafe_allow_html=True)
            info_partida = f"""
            <div style='background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 5px solid #2196f3; color: #0d47a1;'>
                <small>ESTÁS JUGANDO EN:</small><br>
                <strong>🎯 {st.session_state.mod_j.upper()}</strong><br>
             <strong>💡 {st.session_state.ayuda_juego.upper()}</strong>
            </div>
            """
            st.markdown(info_partida, unsafe_allow_html=True)
    
            st.write("###") # Espacio
    

            if st.button("📊 VER FALLAS + PENDIENTES"): st.session_state.viendo_resumen = True; st.rerun()
            if st.button("❌ ABORTAR JUEGO"): st.session_state.jugando = False; st.rerun()

    # --- 4. Lógica de Navegación y Pantallas ---
    if st.session_state.data or st.session_state.modo_falla_activo:
        current_subset = st.session_state.subset_fallas if st.session_state.modo_falla_activo else st.session_state.data[(st.session_state.r_ini-1)*2 : st.session_state.r_fin*2]
        total_int = len(current_subset)//2

        # Menú de botones (Solo si no estamos jugando ni en resumen)
        if not st.session_state.jugando and not st.session_state.viendo_resumen:
            c1, c2, c3 = st.columns(3)
            with c1: st.button("📋 REPASO", key="btn_m1", on_click=lambda: st.session_state.update({'menu_actual': "REPASO"}), use_container_width=True)
            with c2: st.button("🎧 ENTRENA", key="btn_m2", on_click=lambda: st.session_state.update({'menu_actual': "ENTRENA"}), use_container_width=True)
            with c3: st.button("🎯 JUEGO", key="btn_m3", on_click=lambda: st.session_state.update({'menu_actual': "JUEGO"}), use_container_width=True)
            
            st.markdown(f"<div class='main-header'><h3>{st.session_state.cat_activa.upper()} - NIVEL {st.session_state.niv_activo}</h3></div>", unsafe_allow_html=True)

        # --- SECCIONES EXCLUYENTES (Aquí mueren los fantasmas) ---
        
        if st.session_state.viendo_resumen:
            # PANTALLA: RESUMEN DE FALLAS
            st.subheader("📝 REFUERZO DE FALLAS Y PENDIENTES")
            if st.session_state.j_fallidos_dict:
                st.write("❌ **Registros fallados:**")
                for p, info in st.session_state.j_fallidos_dict.items():
                    st.error(f"{p} ➔ {info['traduccion']}")
            
            pends_idx = [i for i in st.session_state.j_indices if i not in st.session_state.j_vistos]
            if pends_idx:
                st.write("⏳ **Registros no mostrados:**")
                for pi in pends_idx:
                    vp, vd, _, _ = obtener_par(pi, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
                    st.warning(f"{vp} ➔ {vd}")

            if st.button("🏠 REFORZAR ESTO (IR A REPASO)", use_container_width=True):
                # Lógica para crear el subset de fallas y pendientes
                nueva_data = []
                for p, info in st.session_state.j_fallidos_dict.items():
                    f1, f2 = [None]*10, [None]*10
                    f1[st.session_state.col_idx], f2[st.session_state.col_idx] = p, info['traduccion']
                    if st.session_state.idioma_ori == "Español": nueva_data.extend([f2, f1])
                    else: nueva_data.extend([f1, f2])
                for pi in pends_idx:
                    nueva_data.extend([current_subset[pi], current_subset[pi+1]])
                st.session_state.update({'subset_fallas': nueva_data, 'modo_falla_activo': True, 'menu_actual': "REPASO", 'jugando': False, 'viendo_resumen': False})
                st.rerun()

        elif st.session_state.menu_actual == "JUEGO":
            # --- 1. PANTALLA DE CONFIGURACIÓN ---
            if not st.session_state.jugando:
                st.markdown("### 🎯 CONFIGURACIÓN DE LA PARTIDA")
                c_a, c_b, c_c = st.columns(3)
                st.session_state.mod_j = c_a.selectbox("Modalidad:", ["Escritura", "Voz", "Pronunciación"], key="sel_mod_j")
                st.session_state.ord_j = c_b.selectbox("Orden:", ["Serial", "Aleatorio"], key="sel_ord_j")
                st.session_state.ayuda_juego = c_c.selectbox("Ayuda:", ["Con Ayuda", "Sin Ayuda"], key="sel_ayu_j")
                
                if st.button("🚀 INICIAR JUEGO", use_container_width=True):
                    ind = list(range(0, len(current_subset), 2))
                    if st.session_state.ord_j == "Aleatorio":
                        #import random
                        random.shuffle(ind)
                    
                    st.session_state.update({
                        'j_indices': ind, 'aciertos': 0, 'fallos': 0, 'jugando': True, 
                        'j_paso': 1, 'j_vistos': set(), 'j_fallidos_dict': {}, 't_inicio': time.time(),
                        'temp_ans': "" # Limpiamos la respuesta temporal de voz
                    })
                    st.rerun()

            # --- 2. LÓGICA DE LA PARTIDA ACTIVA ---
            else:
                pends = [i for i in st.session_state.j_indices if i not in st.session_state.j_vistos]
                
                if pends:
                    if st.session_state.j_paso == 1: 
                        st.session_state.c_idx = pends[0]
                        # Al iniciar una palabra nueva, limpiamos el texto del micrófono anterior
                        st.session_state.temp_ans = "" 
                        
                    v_p, v_s, v_l, _ = obtener_par(st.session_state.c_idx, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
                    
                    # --- MARCADORES SUPERIORES ---
                    m1, m2, m3 = st.columns(3)
                    m1.markdown(f"<div class='stat-box'>Progreso: {len(st.session_state.j_vistos)+1}/{len(st.session_state.j_indices)}</div>", unsafe_allow_html=True)
                    m2.markdown(f"<div class='stat-box' style='color:green;'>✅ Aciertos: {st.session_state.aciertos}</div>", unsafe_allow_html=True)
                    m3.markdown(f"<div class='stat-box' style='color:red;'>❌ Fallos: {st.session_state.fallos}</div>", unsafe_allow_html=True)

                    col_iz, col_de = st.columns([7, 3])

                    with col_iz:
                        # PASO 1: MOSTRAR PREGUNTA (Ocultando la respuesta en inglés)
                        if st.session_state.j_paso == 1:
                            if st.session_state.mod_j == "Voz":
                                st.markdown('<div class="word-box"><h3>TRADUCE EL AUDIO:</h3><h1>🔊 Escucha atentamente...</h1></div>', unsafe_allow_html=True)
                                rutina_audio(v_s, v_l) # En modalidad voz siempre se escucha
                            else:
                                # Muestra la palabra origen (Español o Inglés según configuración)
                                st.markdown(f'<div class="word-box"><h3>TRADUCE:</h3><h1>{v_p}</h1></div>', unsafe_allow_html=True)
                                
                                # REGLA DE AYUDA: Si está "Con Ayuda", le permitimos escuchar el inglés antes de responder
                                if st.session_state.ayuda_juego == "Con Ayuda":
                                    st.caption("💡 Modo Con Ayuda: Escucha la pronunciación antes de responder.")
                                    # Forzamos que suene la guía en inglés (v_s suele ser el destino)
                                    rutina_audio(v_s, v_l) 

                        # PASO 2: ENTRADA DE DATOS (Micrófono o Teclado)
                        elif st.session_state.j_paso == 2:
                            st.markdown(f'<div class="word-box"><h3>EXPRESIÓN: {v_p}</h3></div>', unsafe_allow_html=True)
                            
                            if st.session_state.mod_j == "Pronunciación":
                                audio_usuario = st.audio_input("🎤 Haz clic, habla y espera que procese:", key=f"mic_{st.session_state.c_idx}")
                                
                                if audio_usuario is not None:
                                    with st.spinner("Interpretando tu voz..."):
                                        texto_interpretado = convertir_mic_a_texto(audio_usuario) 
                                    
                                    if texto_interpretado:
                                        st.session_state.temp_ans = texto_interpretado
                                        st.info(f"🗣️ El sistema escuchó: **{texto_interpretado}**")
                                    else:
                                        st.warning("No se entendió el audio. ¡Intenta de nuevo!")
                                        st.session_state.temp_ans = ""
                            else:
                                st.text_input("TU RESPUESTA:", key=f"ins_{st.session_state.c_idx}")

                        # PASO 3: REVELACIÓN FINAL (Ambas palabras se muestran aquí)
                        elif st.session_state.j_paso == 3:
                            color_borde = "#2E7D32" if st.session_state.j_status == "OK" else "#D32F2F"
                            st.markdown(f"""
                                <div class="word-box" style="border-left-color:{color_borde};">
                                    <h3>ORIGEN:</h3><h1>{v_p}</h1>
                                    <hr style="margin:10px 0;">
                                    <h3>TRADUCCIÓN CORRECTA:</h3><h1 style="color:{color_borde};">{v_s}</h1>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            if st.session_state.j_status == "OK": st.balloons()
                            else: st.snow()

                    with col_de:
                        st.write("###")
                        if st.session_state.j_paso == 1:
                            if st.button("CONTINUAR ➔", key="btn_next_1", use_container_width=True):
                                st.session_state.j_paso = 2; st.rerun()
                        
                        elif st.session_state.j_paso == 2:
                            if st.button("COMPROBAR", key="btn_comp", use_container_width=True):
                                sinonimos = [s.strip().lower() for s in v_s.split('/')]
                                es_correcto = False
                                
                                # REGLA DE COMPARACIÓN REAL PARA PRONUNCIACIÓN
                                if st.session_state.mod_j == "Pronunciación":
                                    texto_voz = st.session_state.get("temp_ans", "").strip().lower()
                                    # Comparamos estrictamente lo que dictó el micrófono contra la solución
                                    es_correcto = texto_voz in sinonimos
                                else:
                                    # Escritura y Voz comparan el cuadro de texto
                                    user_ans = st.session_state.get(f"ins_{st.session_state.c_idx}", "").strip().lower()
                                    es_correcto = user_ans in sinonimos

                                # Procesar marcadores
                                if es_correcto:
                                    st.session_state.aciertos += 1
                                    st.session_state.j_status = "OK"
                                    if st.session_state.aciertos % 20 == 0: st.success("¡FELICITACIONES! 20 ACIERTOS")
                                else:
                                    st.session_state.fallos += 1
                                    st.session_state.j_status = "ERR"
                                    st.session_state.j_fallidos_dict[v_p] = {'traduccion': v_s}
                                
                                st.session_state.j_vistos.add(st.session_state.c_idx)
                                st.session_state.j_paso = 3; st.rerun()
                        
                        elif st.session_state.j_paso == 3:
                            # En ambos casos se puede oír la palabra correcta al final
                            st.button("🔊 OÍR PRONUNCIACIÓN", on_click=rutina_audio, args=(v_s, v_l), key="btn_audio_final")
                            if st.button("SIGUIENTE ➔", key="btn_next_3", use_container_width=True):
                                st.session_state.j_paso = 1; st.rerun()

                else:
                    # --- RESUMEN DE FALLAS (Ya estable) ---
                    st.markdown("## 📊 RESUMEN DE LA PARTIDA")
                    with st.container(height=300):
                        st.subheader("❌ Registros Fallados")
                        if st.session_state.j_fallidos_dict:
                            for p, info in st.session_state.j_fallidos_dict.items():
                                traduccion_final = info.get('traduccion', 'Sin traducción') if isinstance(info, dict) else info
                                st.error(f"**{p}** ➔ {traduccion_final}")
                        else:
                            st.success("¡Excelente Edwin! No hubo fallas en esta sesión.")

                    st.markdown("---")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        if st.button("🏠 REFORZAR FALLAS", use_container_width=True):
                            st.session_state.modo_falla_activo = True
                            st.session_state.menu_actual = "REPASO"; st.session_state.jugando = False; st.rerun()
                    with c2:
                        if st.button("🎯 VOLVER AL JUEGO", use_container_width=True):
                            st.session_state.jugando = False; st.rerun()
                    with c3:
                        if st.button("🚪 SALIR AL INICIO", use_container_width=True):
                            st.session_state.menu_actual = "INICIO"; st.session_state.jugando = False; st.rerun()
        elif st.session_state.menu_actual == "REPASO":
            # PANTALLA: REPASO
            for i in range(0, len(current_subset), 2):
                v_i, v_d, v_l, _ = obtener_par(i, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
                c_txt, c_aud, c_go = st.columns([7.5, 1.2, 1.3])
                with c_txt: st.markdown(f"**{i//2 + 1}. {v_i} ➔ {v_d}**")
                with c_aud: st.button("🔊", key=f"ra_{i}", on_click=rutina_audio, args=(v_d, v_l))
                with c_go: 
                    if st.button("🎯", key=f"rg_{i}"): st.session_state.update({'menu_actual': "ENTRENA", 'idx_entrena': i, 'ent_step': 0, 'auto_entrena': False}); st.rerun()

        elif st.session_state.menu_actual == "ENTRENA":
            v_p, v_s, v_l, _ = obtener_par(st.session_state.idx_entrena, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
            
            if not st.session_state.auto_entrena:
                # --- MODO MANUAL ---
                st.markdown(f"<div class='stat-box'>{(st.session_state.idx_entrena//2)+1} / {total_int}</div>", unsafe_allow_html=True)
                c_iz, c_de = st.columns([7, 3])
                with c_iz:
                    st.markdown(f'<div class="word-box"><h3>TRADUCE:</h3><h1>{v_p}</h1></div>', unsafe_allow_html=True)
                    if st.session_state.ent_step == 1: 
                        st.markdown(f'<div class="word-box" style="border-left-color:green;"><h1>{v_s}</h1></div>', unsafe_allow_html=True)
                with c_de:
                    st.write("###")
                    if st.button("SIGUIENTE ➔", key="btn_sig_ent"):
                        if st.session_state.ent_step == 0: st.session_state.ent_step = 1
                        else: 
                            st.session_state.idx_entrena = (st.session_state.idx_entrena + 2) % len(current_subset)
                            st.session_state.ent_step = 0
                        st.rerun()
                    if st.button("🔊 OÍR", key="btn_aud_ent"): rutina_audio(v_s, v_l)
                    st.markdown("---")
                    if st.button("🚀 MODO AUTO", key="btn_auto_on"): st.session_state.auto_entrena = True; st.rerun()
            else:
                # --- MODO AUTOMÁTICO (Tu lógica de bucle) ---
                st.info("Modo Automático Activo: Relájate y escucha.")
                placeholder = st.empty()
                if st.button("🛑 DETENER", key="btn_auto_off"): st.session_state.auto_entrena = False; st.rerun()

                for i in range(st.session_state.idx_entrena, len(current_subset), 2):
                    if not st.session_state.auto_entrena: break
                    v_p, v_s, v_l, _ = obtener_par(i, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
                    progreso = (i//2) + 1
                    with placeholder.container():
                        st.markdown(f"<div class='stat-box'>{progreso} / {total_int}</div>", unsafe_allow_html=True)
                        st.markdown(f'<div class="word-box"><h3>ESPAÑOL:</h3><h1>{v_p}</h1></div>', unsafe_allow_html=True)
                        time.sleep(2)
                        st.markdown(f'<div class="word-box" style="border-left-color:green;"><h3>INGLÉS:</h3><h1>{v_s}</h1></div>', unsafe_allow_html=True)
                        rutina_audio(v_s, v_l)
                        time.sleep(3)
                st.session_state.auto_entrena = False
                st.rerun()
    else:
        st.warning("No hay datos cargados.")

# =============================================================================
# BLOQUE 2B: INICIALIZACIÓN DE SESIÓN
# =============================================================================

def inicializar_estado_aplicativo():
    """Asegura que todas las variables de control existan en la sesión."""
    if 'data' not in st.session_state:
        st.session_state.update({
            'data': [], 'total_p': 0, 'jugando': False, 'menu_actual': "REPASO",
            'idx_entrena': 0, 'ent_step': 0, 'j_paso': 1, 'j_vistos': set(), 
            'j_fallidos_dict': {}, 'cat_activa': "PALABRAS", 'niv_activo': 1, 'idioma_ori': "Español",
            'r_ini': 1, 'r_fin': 20, 'modo_falla_activo': False, 'subset_fallas': [], 't_inicio': 0,
            'viendo_resumen': False, 'ayuda_juego': "Con Ayuda", 'input_voz': "", 'mod_j': "Escritura",
            'auto_entrena': False
        })
# =============================================================================
# BLOQUE 6: PUNTO DE ENTRADA (CONTROLADOR PRINCIPAL)
# =============================================================================

def main():
    """Controlador de flujo principal del aplicativo."""
    aplicar_configuracion_estetica()
    
    # 1. Gestión de Tokens de URL
    parametros = st.query_params
    if "token" in parametros:
        pantalla_crear_password(parametros["token"])
        return 

    # 2. Control de Sesión
    if 'auth' not in st.session_state:
        st.session_state['auth'] = False
    
    if not st.session_state['auth']:
        pantalla_seguridad()
    else:
        mostrar_identidad_usuario()
        # Aquí se llama al núcleo del programa
        ejecutar_aplicativo_principal()

if __name__ == "__main__":
    main()
def procesar_voz_laboratorio(idioma_captura):
    """Captura audio del usuario y lo convierte a texto."""
    audio_input = st.audio_input("Pulsa para grabar tu pronunciación:", key="micro_lab")
    if audio_input:
        r = sr.Recognizer()
        try:
            with sr.AudioFile(audio_input) as source:
                audio_data = r.record(source)
                texto = r.recognize_google(audio_data, language=idioma_captura)
                return texto
        except:
            st.error("No se pudo entender el audio. Intenta de nuevo.")
    return ""
