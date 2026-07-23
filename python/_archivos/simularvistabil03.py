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

def enviar_correo_activacion(correo_destino, nombre_usuario, token):
    """Para nuevos usuarios."""
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
    """Para usuarios que olvidaron su clave."""
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

def ejecutar_envio_mail(remitente, password_app, destino, asunto, cuerpo):
    """Función interna para no repetir código de servidor SMTP."""
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
    """Para nuevos usuarios."""
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
    """Para usuarios que olvidaron su clave."""
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

def proceso_solicitar_recuperacion(correo):
    try:
        token = secrets.token_urlsafe(16)
        conn = psycopg2.connect(host="localhost", database="pprueba", user="postgres", password="peluche01", port="5432")
        cur = conn.cursor()
        
        # 1. Buscamos si el usuario existe y está activo
        cur.execute("SELECT nombre FROM usuarios WHERE correo = %s AND estado = 'ACTIVO'", (correo.strip(),))
        resultado = cur.fetchone()
        
        if resultado:
            nombre_usuario = resultado[0]
            # 2. Guardamos el nuevo token
            cur.execute("UPDATE usuarios SET token_verificacion = %s WHERE correo = %s", (token, correo.strip()))
            conn.commit()
            
            # 3. Enviamos el correo con el formato de RECUPERACIÓN
            if enviar_correo_recuperacion(correo.strip(), nombre_usuario, token):
                cur.close(); conn.close()
                return True
        
        cur.close(); conn.close()
        return False 
    except Exception as e:
        st.error(f"Error en BD: {e}")
        return False
# ==========================================
# Función: mostrar_identidad_usuario
# ==========================================
def mostrar_identidad_usuario():
    """
    Muestra una barra de identidad fija en el tope superior.
    Ajustada para máximo contraste y visibilidad garantizada.
    """
    # 1. Intentamos obtener el usuario de varias posibles llaves por seguridad
    usuario = st.session_state.get('usuario_actual') or st.session_state.get('user_name') or "USUARIO"
    
    # 2. Definimos el color según el tipo de usuario
    es_admin = str(usuario).upper() == "ADMINISTRADOR"
    color_borde = "#FFD700" if es_admin else "#11caa0"
    
    # 3. Inyectamos el diseño (CSS y HTML)
    st.markdown(f"""
        <style>
            /* Contenedor fijo en la parte superior del navegador */
            .banner-identidad-superior {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 35px;
                background-color: #000000; /* Fondo negro puro para máximo contraste */
                color: #FFFFFF;
                z-index: 999999; /* Por encima de cualquier menú de Streamlit */
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0 25px;
                border-bottom: 2px solid {color_borde};
                box-shadow: 0px 2px 10px rgba(0,0,0,0.5);
            }}
            
            .banner-identidad-superior span {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 13px;
                font-weight: bold;
                text-transform: uppercase;
            }}

            /* Forzamos al cuerpo de la página a bajar para que el banner no tape nada */
            [data-testid="stHeader"] {{
                top: 35px !important;
            }}
            .main .block-container {{
                padding-top: 60px !important;
            }}
        </style>
        
        <div class="banner-identidad-superior">
            <span style="color: {color_borde};">● SESIÓN ACTIVA</span>
            <span style="letter-spacing: 1.5px;">{usuario}</span>
        </div>
    """, unsafe_allow_html=True)
# ==========================================
# Función: pantalla_crear_password (NUEVA)
# ==========================================
def pantalla_crear_password(token):
    st.markdown('<h2 style="text-align: center;">🔑 Crear Nueva Contraseña</h2>', unsafe_allow_html=True)
    
    # 1. Conexión y búsqueda del usuario por token
    conn = psycopg2.connect(host="localhost", database="pprueba", user="postgres", password="peluche01", port="5432")
    cur = conn.cursor()
    
    # BUSQUEDA FLEXIBLE: Solo por token, sin importar el estado inicial
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

    # 2. Formulario de nueva clave
    with st.form("form_nueva_clave"):
        nueva_pass = st.text_input("Nueva Contraseña (8-12 caracteres):", type="password")
        confirm_pass = st.text_input("Confirma tu Contraseña:", type="password")
        btn_guardar = st.form_submit_button("GUARDAR CONTRASEÑA", use_container_width=True)

        if btn_guardar:
            if 8 <= len(nueva_pass) <= 12:
                if nueva_pass == confirm_pass:
                    try:
                        # ACTUALIZACIÓN: Guardamos clave, activamos cuenta y LIMPIAMOS el token
                        query_update = """
                            UPDATE usuarios 
                            SET clave = %s, 
                                estado = 'ACTIVO', 
                                token_verificacion = NULL 
                            WHERE token_verificacion = %s
                        """
                        cur.execute(query_update, (nueva_pass, token))
                        conn.commit()
                        
                        st.success("✅ ¡Contraseña actualizada con éxito!")
                        st.balloons()
                        time.sleep(3)
                        
                        # Limpiar la URL y volver al login
                        st.query_params.clear()
                        st.session_state.auth_step = 'login'
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")
                else:
                    st.warning("Las contraseñas no coinciden.")
            else:
                st.warning("La contraseña debe tener entre 8 y 12 caracteres.")
    
    cur.close()
    conn.close()
# ==========================================
# BLOQUE 1: CONFIGURACIÓN Y ESTILOS GLOBALES
# ==========================================
def aplicar_configuracion_estetica():
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

# ==========================================
# BLOQUE 2: EL APLICATIVO (CAJA NEGRA)
# ==========================================
def ejecutar_aplicativo_principal():
    """Aquí reside todo el código que ya funciona impecablemente"""
    
    # 1. LLAMADA GENERAL: Para Menú de Repaso, Entrena y Configuraciones
    mostrar_identidad_usuario()

    # --- Sub-rutinas Internas ---
    def procesar_voz_laboratorio(idioma_captura):
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

    def rutina_cargar_db(categoria, nivel, tipos_sel):
        try:
            conn = psycopg2.connect(host="localhost", database="pprueba", user="postgres", password="peluche01", port="5432")
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

    # --- Lógica de Interfaz Principal ---
    if 'data' not in st.session_state:
        st.session_state.update({
            'data': [], 'total_p': 0, 'jugando': False, 'menu_actual': "REPASO",
            'idx_entrena': 0, 'ent_step': 0, 'j_paso': 1, 'j_vistos': set(), 
            'j_fallidos_dict': {}, 'cat_activa': "PALABRAS", 'niv_activo': 1, 'idioma_ori': "Español",
            'r_ini': 1, 'r_fin': 20, 'modo_falla_activo': False, 'subset_fallas': [], 't_inicio': 0,
            'viendo_resumen': False, 'ayuda_juego': "Con Ayuda", 'input_voz': "", 'mod_j': "Escritura"
        })

    with st.sidebar:
        st.header("⚙️ PANEL DE CONTROL")
        if not st.session_state.jugando:
            habla = st.selectbox("Idioma Origen:", ["Español", "Inglés"])
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
                    'subset_fallas': []
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
                st.session_state.auth_step = 'inicio'
                st.rerun()
        else:
            info_partida = f"{st.session_state.mod_j.upper()}<br>{st.session_state.ayuda_juego.upper()}"
            st.markdown(f"<div class='modo-aviso'>{info_partida}</div>", unsafe_allow_html=True)
            if st.button("📊 VER FALLAS + NO MOSTRADOS"): st.session_state.viendo_resumen = True; st.rerun()
            if st.button("❌ ABORTAR JUEGO"): st.session_state.jugando = False; st.rerun()

    if st.session_state.data or st.session_state.modo_falla_activo:
        current_subset = st.session_state.subset_fallas if st.session_state.modo_falla_activo else st.session_state.data[(st.session_state.r_ini-1)*2 : st.session_state.r_fin*2]
        total_int = len(current_subset)//2

        if not st.session_state.jugando and not st.session_state.viendo_resumen:
            c1, c2, c3 = st.columns(3)
            with c1: st.button("📋 REPASO", on_click=lambda: st.session_state.update({'menu_actual': "REPASO"}), use_container_width=True)
            with c2: st.button("🎧 ENTRENA", on_click=lambda: st.session_state.update({'menu_actual': "ENTRENA"}), use_container_width=True)
            with c3: st.button("🎯 JUEGO", on_click=lambda: st.session_state.update({'menu_actual': "JUEGO"}), use_container_width=True)

        reloj = f"{int(time.time() - st.session_state.t_inicio)}s" if st.session_state.jugando else ""
        st.markdown(f"<div class='main-header'><div class='timer-box'>{reloj}</div><h3>{st.session_state.cat_activa.upper()} - NIVEL {st.session_state.niv_activo}</h3></div>", unsafe_allow_html=True)

        if st.session_state.viendo_resumen:
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

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🏠 REFORZAR FALLAS (MENÚ)", use_container_width=True):
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
            with col_btn2:
                if st.button("🎯 VOLVER AL JUEGO", use_container_width=True): 
                    st.session_state.viendo_resumen = False
                    st.rerun()

        elif st.session_state.menu_actual == "REPASO" and not st.session_state.jugando:
            for i in range(0, len(current_subset), 2):
                v_i, v_d, v_l, _ = obtener_par(i, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
                c_txt, c_aud, c_go = st.columns([7.5, 1.2, 1.3])
                num = i//2 + 1
                with c_txt: st.markdown(f"<div style='display:flex; justify-content:space-between; padding:8px; border-bottom:1px solid #ccc;'><span style='color:#000; font-weight:900;'>{num}. {v_i} ➔ {v_d}</span></div>", unsafe_allow_html=True)
                with c_aud: st.button("🔊", key=f"ra_{i}", on_click=rutina_audio, args=(v_d, v_l))
                with c_go: 
                    if st.button("🎯", key=f"rg_{i}"): st.session_state.update({'menu_actual': "ENTRENA", 'idx_entrena': i, 'ent_step': 0}); st.rerun()

        elif st.session_state.menu_actual == "JUEGO":
            # 2. SEGUNDA LLAMADA: Para que el nombre no desaparezca al refrescar la pantalla de juego
            mostrar_identidad_usuario()
            
            if not st.session_state.jugando:
                st.markdown("### 🎯 CONFIGURACIÓN JUEGO")
                c_a, c_b, c_c = st.columns(3)
                st.session_state['mod_j'] = c_a.selectbox("Modo:", ["Escritura", "Voz", "Pronunciación"])
                st.session_state['ord_j'] = c_b.selectbox("Orden:", ["Serial", "Aleatorio"])
                st.session_state.ayuda_juego = c_c.selectbox("Ayuda:", ["Con Ayuda", "Sin Ayuda"])
                if st.button("🚀 INICIAR", use_container_width=True):
                    ind = [i for i in range(0, len(current_subset), 2)]
                    if st.session_state['ord_j'] == "Aleatorio": random.shuffle(ind)
                    st.session_state.update({'j_indices': ind, 'aciertos': 0, 'fallos': 0, 'jugando': True, 'j_paso': 1, 'j_vistos': set(), 'j_fallidos_dict': {}, 't_inicio': time.time()})
                    st.rerun()
            else:
                pends = [i for i in st.session_state.j_indices if i not in st.session_state.j_vistos]
                if pends:
                    if st.session_state.j_paso == 1: st.session_state.c_idx = pends[0]
                    v_p, v_s, v_l, _ = obtener_par(st.session_state.c_idx, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
                    m1, m2, m3 = st.columns(3)
                    m1.markdown(f"<div class='stat-box'>Progreso: {len(st.session_state.j_vistos)+1}/{len(st.session_state.j_indices)}</div>", unsafe_allow_html=True)
                    m2.markdown(f"<div class='stat-box' style='color:green;'>✅ {st.session_state.aciertos}</div>", unsafe_allow_html=True)
                    m3.markdown(f"<div class='stat-box' style='color:red;'>❌ {st.session_state.fallos}</div>", unsafe_allow_html=True)

                    c_j1, c_j2 = st.columns([7, 3])
                    with c_j1:
                        if st.session_state.j_paso == 1:
                            txt_label = "🔊 (Escucha...)" if st.session_state['mod_j'] == "Voz" else v_p
                            st.markdown(f'<div class="word-box"><h3>TRADUCE:</h3><h1>{txt_label}</h1></div>', unsafe_allow_html=True)
                        elif st.session_state.j_paso == 2:
                            if st.session_state['mod_j'] == "Pronunciación":
                                lang_cap = "en-US" if v_l == 'en' else "es-ES"
                                res_voz = procesar_voz_laboratorio(lang_cap)
                                if res_voz: 
                                    st.session_state.input_voz = res_voz
                                    st.success(f"Capturado: {res_voz}")
                            else:
                                st.text_input("RESPUESTA:", key=f"j_in_{st.session_state.c_idx}")
                        elif st.session_state.j_paso == 3:
                            cl = "#2E7D32" if st.session_state.j_status == "OK" else "#D32F2F"
                            if st.session_state.j_status == "OK" or st.session_state.ayuda_juego == "Con Ayuda":
                                st.markdown(f'<div class="word-box" style="border-left-color:{cl};"><h3>{v_p}</h3><h1 style="color:{cl};">{v_s}</h1></div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="word-box" style="border-left-color:{cl};"><h3>{v_p}</h3><h1 style="color:{cl};">FALLO</h1></div>', unsafe_allow_html=True)
                    
                    with c_j2:
                        st.write("###")
                        if st.session_state.j_paso == 1:
                            if st.session_state['mod_j'] == "Voz": 
                                if st.button("🔊 OÍR"): rutina_audio(v_s, v_l)
                            if st.button("CONTINUAR ➔"): st.session_state.j_paso = 2; st.rerun()
                        elif st.session_state.j_paso == 2:
                            if st.button("COMPROBAR"):
                                ans = st.session_state.input_voz.strip().lower() if st.session_state['mod_j'] == "Pronunciación" else st.session_state.get(f"j_in_{st.session_state.c_idx}", "").strip().lower()
                                if ans == v_s.lower():
                                    st.session_state.j_status = "OK"; st.session_state.aciertos += 1; st.balloons()
                                    if v_p in st.session_state.j_fallidos_dict: del st.session_state.j_fallidos_dict[v_p]
                                    rutina_audio(v_s, v_l)
                                else:
                                    st.session_state.j_status = "ERR"; st.session_state.fallos += 1; st.snow()
                                    st.session_state.j_fallidos_dict[v_p] = {'traduccion': v_s}
                                    if st.session_state.ayuda_juego == "Con Ayuda": rutina_audio(v_s, v_l)
                                st.session_state.j_vistos.add(st.session_state.c_idx); st.session_state.j_paso = 3; st.rerun()
                        elif st.session_state.j_paso == 3:
                            if st.session_state['mod_j'] == "Pronunciación" or st.session_state.ayuda_juego == "Con Ayuda":
                                if st.button("🔊 OÍR"): rutina_audio(v_s, v_l)
                            if st.button("SIGUIENTE ➔"): st.session_state.j_paso = 1; st.session_state.input_voz = ""; st.rerun()
                else:
                    st.success("¡PARTIDA FINALIZADA!"); st.balloons()
                    if st.button("SALIR AL MENÚ"): st.session_state.jugando = False; st.rerun()

        elif st.session_state.menu_actual == "ENTRENA":
            v_p, v_s, v_l, _ = obtener_par(st.session_state.idx_entrena, current_subset, st.session_state.col_idx, st.session_state.idioma_ori)
            st.markdown(f"<div class='stat-box'>{(st.session_state.idx_entrena//2)+1} / {total_int}</div>", unsafe_allow_html=True)
            c_iz, c_de = st.columns([7, 3])
            with c_iz:
                st.markdown(f'<div class="word-box"><h3>TRADUCE:</h3><h1>{v_p}</h1></div>', unsafe_allow_html=True)
                if st.session_state.ent_step == 1: st.markdown(f'<div class="word-box" style="border-left-color:green;"><h1>{v_s}</h1></div>', unsafe_allow_html=True)
            with c_de:
                st.write("###")
                if st.button("SIGUIENTE"):
                    if st.session_state.ent_step == 0: st.session_state.ent_step = 1
                    else: st.session_state.idx_entrena = (st.session_state.idx_entrena + 2) % len(current_subset); st.session_state.ent_step = 0
                    st.rerun()
                st.button("🔊 OÍR", on_click=rutina_audio, args=(v_s, v_l))
# ==========================================
# BLOQUE 3: EL PORTERO (LÓGICA ACTUALIZADA)
# ==========================================

def registrar_usuario_inicial(nombre, alias, correo, nivel_texto):
    """
    Registra al usuario en estado PENDIENTE. 
    El password_hash se queda vacío (NULL) hasta que el usuario use el token.
    """
    try:
        # Generamos el token de seguridad
        token = secrets.token_urlsafe(16)
        
        conn = psycopg2.connect(
            host="localhost", database="pprueba", user="postgres", password="peluche01", port="5432"
        )
        cur = conn.cursor()
        
        # Lógica para evitar el error de NULL en Alias
        # Si no hay alias, usamos los primeros 10 caracteres del nombre sin espacios
        ali_final = alias.strip() if (alias and alias.strip()) else nombre.replace(" ", "")[:10]
        
        query = """
            INSERT INTO usuarios (nombre, alias, correo, nivel, token_verificacion, estado) 
            VALUES (%s, %s, %s, %s, %s, 'PENDIENTE')
        """
        
        cur.execute(query, (
            nombre.strip(), 
            ali_final, 
            correo.strip(), 
            nivel_texto, 
            token
        ))
        
        conn.commit()
        cur.close(); conn.close()
        return True, token
    except Exception as e:
        return False, f"Error detallado: {e}"

def validar_credenciales_db(password_ingresada):
    """
    Busca al usuario por su contraseña cifrada. 
    Solo permite acceso si el estado es 'ACTIVO'.
    """
    try:
        conn = psycopg2.connect(
            host="localhost", database="pprueba", user="postgres", password="peluche01", port="5432"
        )
        cur = conn.cursor()
        
        # Importante: Usamos la columna 'clave' que creamos en el nuevo SQL
        query = "SELECT nombre, alias FROM usuarios WHERE clave = %s AND estado = 'ACTIVO'"
        cur.execute(query, (password_ingresada.strip(),))
        registro = cur.fetchone()
        cur.close(); conn.close()
        
        if registro:
            # Prioridad al Alias para la visualización
            st.session_state['usuario_actual'] = registro[1] if registro[1] else registro[0]
            return True
        return False
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

def pantalla_seguridad():
    """
    Interfaz de acceso principal con Login, Registro y Recuperación.
    """
    if 'auth_step' not in st.session_state:
        st.session_state.auth_step = 'inicio'

    col_main_1, col_main_2, col_main_3 = st.columns([1, 2, 1])
    
    with col_main_2:
        st.markdown('<div style="font-size: 80px; text-align: center; margin-bottom: 10px;">🎓</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center;">DICCIONARIO INTERACTIVO</h2>', unsafe_allow_html=True)
        st.markdown('---')

        # --- ESTADO: BOTONES PRINCIPALES ---
        if st.session_state.auth_step == 'inicio':
            if st.button("INICIAR SESIÓN", use_container_width=True):
                st.session_state.auth_step = 'login'
                st.rerun()
            if st.button("CREAR UNA CUENTA", use_container_width=True):
                st.session_state.auth_step = 'registro'
                st.rerun()

        # --- ESTADO: LOGIN ---
        elif st.session_state.auth_step == 'login':
            st.write("### 🔐 Ingreso de Usuario")
            password = st.text_input("Contraseña:", type="password")
            
            if st.button("ENTRAR", use_container_width=True):
                # 1. Puerta Trasera de Desarrollo
                if password == "peluche 02":
                    st.session_state['usuario_actual'] = "Administrador"
                    st.session_state['auth'] = True
                    st.rerun()
                # 2. Validación estándar
                elif validar_credenciales_db(password):
                    st.session_state['auth'] = True
                    st.rerun()
                else:
                    st.error("Credenciales inválidas o cuenta pendiente de activación.")
            
            # --- BOTÓN DE RECUPERACIÓN (Fuera del IF de ENTRAR) ---
            if st.button("¿Olvidaste tu contraseña?"):
                st.session_state.auth_step = 'recuperar'
                st.rerun()
            
            if st.button("VOLVER"):
                st.session_state.auth_step = 'inicio'
                st.rerun()

        # --- ESTADO: RECUPERAR CONTRASEÑA ---
        elif st.session_state.auth_step == 'recuperar':
            st.write("### 🔑 Recuperar Acceso")
            correo_recu = st.text_input("Introduce tu correo registrado:")
            
            if st.button("ENVIAR ENLACE DE RECUPERACIÓN", use_container_width=True):
                if not correo_recu:
                    st.warning("Escribe tu correo.")
                else:
                    # Generamos un nuevo token y enviamos correo
                    exito = proceso_solicitar_recuperacion(correo_recu)
                    if exito:
                        st.success("Si el correo existe, recibirás un enlace en breve.")
                        time.sleep(3)
                        st.session_state.auth_step = 'inicio'
                        st.rerun()

            if st.button("VOLVER AL LOGIN"):
                st.session_state.auth_step = 'inicio'
                st.rerun()

        # --- ESTADO: REGISTRO ---
        elif st.session_state.auth_step == 'registro':
            st.write("### 📝 Registro de Nuevo Usuario")
            nom = st.text_input("Nombre Completo:")
            cor = st.text_input("Correo Electrónico:")
            ali = st.text_input("Alias (Nombre de usuario):")
            niv = st.selectbox("Nivel de Inglés:", ["Básico", "Intermedio", "Avanzado"])
            
            if st.button("REGISTRARSE", use_container_width=True):
                if not nom or not cor:
                    st.warning("El nombre y el correo son obligatorios.")
                else:
                    exito, resultado_token = registrar_usuario_inicial(nom, ali, cor, niv)
                    if exito:
                        if enviar_correo_activacion(cor, nom, resultado_token):
                            st.success(f"¡Registro exitoso! Revisa tu correo: {cor}")
                            st.info("Haz clic en el enlace del correo para crear tu clave.")
                        else:
                            st.warning("Usuario registrado, pero hubo un problema enviando el correo.")
                        
                        time.sleep(4)
                        st.session_state.auth_step = 'inicio'
                        st.rerun()
                    else:
                        st.error(resultado_token)
            
            if st.button("CANCELAR"):
                st.session_state.auth_step = 'inicio'
                st.rerun()
# ==========================================
# PUNTO DE ENTRADA (MAIN) - REPARADO
# ==========================================
def main():
    # 1. ESTO ES LO QUE DEVUELVE LOS COLORES
    # Debe ir antes de cualquier otra cosa
    aplicar_configuracion_estetica()
    
    # 2. Detectar si hay un token en la URL
    parametros = st.query_params
    
    if "token" in parametros:
        token_recibido = parametros["token"]
        pantalla_crear_password(token_recibido)
        return 

    # 3. Lógica de autenticación normal
    if 'auth' not in st.session_state:
        st.session_state['auth'] = False
    
    if not st.session_state['auth']:
        pantalla_seguridad()
    else:
        # Aquí también nos aseguramos de mostrar la identidad
        mostrar_identidad_usuario()
        ejecutar_aplicativo_principal()

if __name__ == "__main__":
    main()