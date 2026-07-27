import streamlit as st
import speech_recognition as sr

st.set_page_config(page_title="Laboratorio de Voz", layout="centered")

# Título e información
st.title("🎙️ Prueba de Micrófono Local")

# IMPORTANTE: Esta línea ayuda a que el navegador entienda que debe activar el audio
st.write("Asegúrate de que el icono del micrófono en la barra de direcciones esté permitido.")

idioma = st.radio("Idioma:", ["es-ES", "en-US"], horizontal=True)

# Componente de audio con una clave (key) para refrescarlo
audio_input = st.audio_input("Graba aquí tu palabra:", key="mic_local")

if audio_input is not None:
    st.audio(audio_input)
    r = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_input) as source:
            audio_data = r.record(source)
            # Conversión
            texto = r.recognize_google(audio_data, language=idioma)
            st.success(f"Palabra capturada: {texto}")
            st.session_state['vocal'] = texto
    except Exception as e:
        st.error("No se detectó sonido en la grabación. Revisa tu micrófono.")

st.text_input("Resultado:", value=st.session_state.get('vocal', ""))