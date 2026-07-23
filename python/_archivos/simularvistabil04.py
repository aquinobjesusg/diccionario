import streamlit as st
import time
import requests
from streamlit_lottie import st_lottie

# Configuración de página
st.set_page_config(page_title="Laboratorio de Estímulos", page_icon="🔥")

# Función para cargar animaciones Lottie desde la web
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URLs de animaciones gratuitas (Trofeo y Cohete)
lottie_trofeo = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_at4p5idj.json")
lottie_cohete = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_al9v6z6v.json")

st.title("🧪 Laboratorio de Animaciones Educativas")
st.write("Haz clic en los botones para ver cómo podrías premiar a tus alumnos.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Estímulo Nivel 1 (Globos)"):
        st.write("¡Buen trabajo!")
        st.balloons()

with col2:
    if st.button("Estímulo Nivel 2 (Insignia CSS)"):
        st.markdown("""
            <div style="
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                border: 2px solid #2E7D32;
                animation: pop 0.5s ease-out;
            ">
                <h2 style="margin:0;">🎯 ¡EXCELENTE!</h2>
                <p style="margin:0;">Has logrado una racha increíble.</p>
            </div>
            <style>
            @keyframes pop {
                0% { transform: scale(0.5); }
                80% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
            </style>
        """, unsafe_allow_html=True)
        time.sleep(1)
        st.snow()

with col3:
    if st.button("Estímulo Pro (Lottie Animation)"):
        st.success("¡NIVEL MAESTRO ALCANZADO!")
        st_lottie(lottie_trofeo, height=200, key="trofeo")
        st.balloons()

st.divider()

# Ejemplo de como se vería un "Mensaje Flotante" (Toast)
if st.button("Mostrar Notificación Rápida"):
    st.toast('¡Sigue así, Edwin!', icon='🔥')

# Sección de racha simulada
st.subheader("Simulación de Racha")
racha = st.slider("Desliza para simular aciertos del alumno:", 0, 50, 0)

if racha == 20:
    st.warning("🚀 ¡Racha de 20! Activando despegue...")
    st_lottie(lottie_cohete, height=250, key="cohete")