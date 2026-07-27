import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Laboratorio Web de Voz", page_icon="🌐")

st.title("🎤 Laboratorio de Voz en la Nube")
st.write("Esta versión tiene seguridad HTTPS activa.")

idioma = st.radio("Idioma:", ["en-US", "es-ES"], horizontal=True)

def mic_web(lang):
    js_code = f"""
    <div style="text-align:center;">
        <button id="btn" style="
            width:100%; height:100px; font-weight:900; 
            background-color:#FFD600; border:4px solid #000; 
            border-radius:20px; cursor:pointer; font-size:20px;
        ">MANTÉN PULSADO PARA HABLAR</button>
        <p id="info" style="font-family:sans-serif; font-size:14px; margin-top:10px;">Listo para probar en la web</p>
    </div>

    <script>
    const btn = document.getElementById('btn');
    const info = document.getElementById('info');
    const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!Recognition) {{
        info.innerText = "Navegador no compatible";
    }} else {{
        const rec = new Recognition();
        rec.lang = '{lang}';
        
        btn.onmousedown = () => {{
            rec.start();
            btn.style.backgroundColor = '#FF5252';
            info.innerText = "Escuchando...";
        }};

        btn.onmouseup = () => {{
            rec.stop();
            btn.style.backgroundColor = '#FFD600';
            info.innerText = "Procesando...";
        }};

        rec.onresult = (event) => {{
            const result = event.results[0][0].transcript;
            window.parent.postMessage({{type: 'streamlit:setComponentValue', value: result}}, '*');
        }};
    }}
    </script>
    """
    return components.html(js_code, height=180)

# Captura de datos
resultado = mic_web(idioma)

if isinstance(resultado, str) and resultado.strip() != "":
    st.success(f"¡Te escuché! Dijiste: **{resultado}**")
    st.session_state['voz'] = resultado

st.text_input("Resultado final:", value=st.session_state.get('voz', ""))
Paso