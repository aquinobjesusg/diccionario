import streamlit as st
import psycopg2
from gtts import gTTS
import io
import base64
import random
import time
import speech_recognition as sr  # Nueva técnica de laboratorio

# ==========================================
# RUTINA 1: ESTILOS (CSS) - SIN ALTERACIONES
# ==========================================
def rutina_estilos():
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
        
        .welcome-card {
            background: linear-gradient(135deg, #0044CC 0%, #002266 100%);
            color: white; padding: 40px; border-radius: 20px; text-align: center;
            border: 4px solid #FFD600; margin-bottom: 30px; box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
        }
        .welcome-quote { font-style: italic; font-size: 1.2rem; color: #FFD600; margin-top: 15px; }
        </style>
        """, unsafe_allow_html=True)

# ==========================================
# RUTINA DE PORTADA - SIN ALTERACIONES
# ==========================================
def mostrar_portada():
    st.markdown("""
        <div class="welcome-card">
            <h1>📖 DICCIONARIO INTERACTIVO</h1>
            <p style='font-size: 1.3rem;'>Herramienta Pedagógica para el Aprendizaje de Idiomas</p>
            <div class="welcome-quote">
                "Aprender un idioma es tener una ventana más desde la cual mirar el mundo."
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("### 🔐 Acceso al Sistema")
        clave = st.text_input("Ingrese la clave de acceso:", type="password")
        if st.button("INGRESAR AL PROGRAMA", use_container_width=True):
            if clave == "peluche 02":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Clave incorrecta. Intente de nuevo.")

# ==========================================
# RUTINA 2: MOTOR DE DATOS Y NUEVA PRONUNCIACIÓN
# ==========================================

def procesar_voz_laboratorio(idioma_captura):
    """Implementación de la técnica de laboratorio local"""
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

# ==========================================
# RUTINA 3: INTERFAZ PRINCIPAL
# ==========================================
def main():
    rutina_estilos()
    
    if 'auth' not in st.session_state: st.session_state['auth'] = False
    if not st.session_state['auth']:
        mostrar_portada()
        return
    
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

        # --- SECCIÓN DE FALLAS Y REGISTROS NO MOSTRADOS ---
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
                    # Agregar fallados
                    for p, info in st.session_state.j_fallidos_dict.items():
                        f1, f2 = [None]*10, [None]*10
                        f1[st.session_state.col_idx], f2[st.session_state.col_idx] = p, info['traduccion']
                        if st.session_state.idioma_ori == "Español": nueva_data.extend([f2, f1])
                        else: nueva_data.extend([f1, f2])
                    # Agregar no vistos
                    for pi in pends_idx:
                        nueva_data.extend([current_subset[pi], current_subset[pi+1]])
                    
                    st.session_state.update({
                        'subset_fallas': nueva_data, 
                        'modo_falla_activo': True, 
                        'menu_actual': "REPASO", 
                        'jugando': False, 
                        'viendo_resumen': False
                    })
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
                            # --- APLICACIÓN QUIRÚRGICA DE LA TÉCNICA DE LABORATORIO ---
                            if st.session_state['mod_j'] == "Pronunciación":
                                # Determinar idioma de captura basado en el idioma destino (v_l)
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
                            # BOTÓN AGREGADO PARA REPASO DE PRONUNCIACIÓN EN EL PASO FINAL
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

if __name__ == "__main__": main()