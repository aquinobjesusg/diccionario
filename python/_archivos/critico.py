import streamlit as st
import speech_recognition as sr

st.set_page_config(page_title="Laboratorio de Voz", layout="centered")

# Estilo para que la interfaz se vea limpia
st.title("🎙️ Laboratorio de Voz Simplificado")

# 1. Selección de idioma (Limpio y directo)
idioma = st.radio("Idioma de captura:", ["es-ES", "en-US"], horizontal=True)

st.divider()

# 2. El botón de captura (Interfase oficial simplificada)
# Nota: Streamlit muestra un pequeño círculo, es la forma más estable 
# de asegurar que no te de 'Network Error' en local.
audio_input = st.audio_input("Pulsa para hablar:")

# --- LÓGICA OCULTA DE PROCESAMIENTO ---
if audio_input:
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_input) as source:
            audio_data = r.record(source)
            # El motor hace su trabajo en silencio
            texto = r.recognize_google(audio_data, language=idioma)
            
            # Guardamos el resultado en la "memoria" de la app
            st.session_state['vocal_simple'] = texto
    except:
        st.error("No se pudo entender. Intenta de nuevo.")

st.divider()

# 3. Resultado Final (Solo la palabra, sin barras de audio)
# Si hay algo en la memoria, lo mostramos grande y claro
if 'vocal_simple' in st.session_state and st.session_state['vocal_simple']:
    st.markdown(f"### 🎯 Palabra: **{st.session_state['vocal_simple']}**")

# Cuadro de confirmación por si quieres copiar la palabra
st.text_input("Texto en sistema:", value=st.session_state.get('vocal_simple', ""))

if st.button("Limpiar"):
    st.session_state['vocal_simple'] = ""
    st.rerun()