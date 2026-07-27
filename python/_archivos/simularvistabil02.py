import streamlit as st
import psycopg2
from gtts import gTTS
import io
import base64
import random
import time
import speech_recognition as sr
import re

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
# BLOQUE 3: EL PORTERO (LÓGICA DE CONTROL)
# ==========================================

def registrar_usuario_db(nombre, alias, correo, nivel_texto, clave):
    """
    Función: registrar_usuario_db
    Descripción: Inserta un nuevo registro en PostgreSQL. Convierte el nivel
                 de texto a número y maneja vacíos como NULL.
    """
    try:
        # Mapeo de nivel pedagógico a valor numérico para la DB
        mapping_niveles = {"Primaria": 1, "Secundaria": 2, "Avanzado": 3}
        nivel_numerico = mapping_niveles.get(nivel_texto, 1)

        # Limpieza de strings y manejo de Nulos
        nom_f = nombre.strip()
        ali_f = alias.strip() if alias and alias.strip() else None
        cor_f = correo.strip() if correo and correo.strip() else None
        cla_f = clave.strip()

        conn = psycopg2.connect(
            host="localhost", database="pprueba", user="postgres", password="peluche01", port="5432"
        )
        cur = conn.cursor()
        
        query = """
            INSERT INTO usuarios (nombre, alias, correo, nivel, clave) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (nom_f, ali_f, cor_f, nivel_numerico, cla_f))
        
        conn.commit()
        cur.close()
        conn.close()
        return True, f"Registro aceptado satisfactoriamente para {nom_f}."
    except Exception as e:
        return False, f"Error al insertar: {e}"

def validar_credenciales_db(password_ingresada):
    """
    Función: validar_credenciales_db
    Descripción: Busca la clave en la tabla usuarios. Si la encuentra, 
                 carga el Alias o Nombre en la variable global de sesión.
    """
    try:
        conn = psycopg2.connect(
            host="localhost", database="pprueba", user="postgres", password="peluche01", port="5432"
        )
        cur = conn.cursor()
        query = "SELECT nombre, alias FROM usuarios WHERE clave = %s"
        cur.execute(query, (password_ingresada.strip(),))
        registro = cur.fetchone()
        cur.close(); conn.close()
        
        if registro:
            # Prioridad: Alias (si existe), de lo contrario Nombre
            alias_db = str(registro[1]).strip() if registro[1] else ""
            st.session_state['usuario_actual'] = alias_db if alias_db else registro[0]
            return True
        return False
    except Exception as e:
        st.error(f"Error de conexión con la base de datos: {e}")
        return False

def pantalla_seguridad():
    """
    Función: pantalla_seguridad
    Descripción: Interfaz de entrada. Gestiona el Login, el Registro 
                 y el acceso especial de Administrador.
    """
    if 'auth_step' not in st.session_state:
        st.session_state.auth_step = 'inicio'

    col_main_1, col_main_2, col_main_3 = st.columns([1, 2, 1])
    
    with col_main_2:
         # --- ESTO RESTAURA EL LOGO ---
        st.markdown('<div style="font-size: 80px; text-align: center; margin-bottom: 10px;">🎓</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center;">DICCIONARIO INTERACTIVO</h2>', unsafe_allow_html=True)
        st.markdown('---')

        # ESTADO: BOTONES INICIALES
        if st.session_state.auth_step == 'inicio':
            if st.button("INICIAR SESIÓN", use_container_width=True):
                st.session_state.auth_step = 'login'
                st.rerun()
            if st.button("REGISTRAR NUEVA CUENTA", use_container_width=True):
                st.session_state.auth_step = 'registro'
                st.rerun()

        # ESTADO: FORMULARIO DE LOGIN
        elif st.session_state.auth_step == 'login':
            st.write("### 🔐 Acceso")
            password = st.text_input("Contraseña:", type="password")
            
            if st.button("ENTRAR", use_container_width=True):
                # 1. Chequeo de Puerta Trasera (Administrador)
                if password == "peluche 02":
                    st.session_state['usuario_actual'] = "Administrador"
                    st.session_state['auth'] = True
                    st.rerun()
                # 2. Chequeo en Base de Datos
                elif validar_credenciales_db(password):
                    st.session_state['auth'] = True
                    st.rerun()
                else:
                    st.error("Acceso denegado: Clave incorrecta")
            
            if st.button("VOLVER"):
                st.session_state.auth_step = 'inicio'
                st.rerun()

        # ESTADO: FORMULARIO DE REGISTRO
        elif st.session_state.auth_step == 'registro':
            st.write("### 📝 Formulario de Registro")
            nom = st.text_input("Nombre (Obligatorio):")
            ali = st.text_input("Alias (Opcional):")
            cor = st.text_input("Correo (Opcional):")
            niv = st.selectbox("Nivel Educativo:", ["Primaria", "Secundaria", "Avanzado"])
            p1 = st.text_input("Defina su Password:", type="password", key="reg_p1")
            p2 = st.text_input("Confirme su Password:", type="password", key="reg_p2")
            
            col_r1, col_r2 = st.columns(2)
            if col_r1.button("ENVIAR", use_container_width=True):
                if not nom or not p1:
                    st.warning("Nombre y Password son requeridos.")
                elif p1 != p2:
                    st.error("Las contraseñas no coinciden.")
                else:
                    # Ejecutamos la inserción en la DB
                    exito, mensaje = registrar_usuario_db(nom, ali, cor, niv, p1)
                    if exito:
                        st.success(mensaje)
                        import time
                        time.sleep(2)
                        st.session_state.auth_step = 'inicio'
                        st.rerun()
                    else:
                        st.error(mensaje)
            
            if col_r2.button("CANCELAR"):
                st.session_state.auth_step = 'inicio'
                st.rerun()
# ==========================================
# PUNTO DE ENTRADA (BOOTSTRAP)
# ==========================================
def main():
    aplicar_configuracion_estetica()
    
    # Inicializar estado de autenticación
    if 'auth' not in st.session_state:
        st.session_state['auth'] = False
    
    # Decisión de qué pantalla mostrar
    if not st.session_state['auth']:
        pantalla_seguridad()
    else:
        # Si está autenticado, llamamos a la "Caja Negra"
        ejecutar_aplicativo_principal()

if __name__ == "__main__":
    main()