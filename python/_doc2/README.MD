env\Scripts\activate.bat
pip install flask
python app.py

python -m pip install -r requirements.txt

python simularvistabil07.py

#
streamlit run simularvistabil07.py

pip install streamlit
pip install psycopg2-binary
pip install SpeechRecognition
pip install gTTS

# Opcional
pip install pyaudio
pip install playsound


pip install reflex
reflex init
reflex run



import sqlite3

# Crea o se conecta a una base de datos existente
conexion = sqlite3.connect('mi_base_de_datos.db')

# Cierra la conexión al finalizar
conexion.close()

