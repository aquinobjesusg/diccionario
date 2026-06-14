import psycopg2
import random
import os
import msvcrt
from gtts import gTTS
from playsound import playsound
import time

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def hablar(texto, idioma_opc):
    lang = 'en' if idioma_opc == "EN" else 'es'
    archivo_temp = "temp_audio.mp3"
    try:
        tts = gTTS(text=texto, lang=lang)
        tts.save(archivo_temp)
        playsound(archivo_temp)
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)
    except Exception as e:
        print(f"\n(Error de audio: {e})")

def mostrar_diccionario_completo(arreglo, nombre):
    limpiar_pantalla()
    print(f"\n{'='*75}")
    print(f"{'REPASO FINAL: ' + nombre:^75}")
    print(f"{'='*75}")
    print(f"{'PREGUNTA':<35} | {'RESPUESTA':<35}")
    print(f"{'-'*75}")
    for fila in arreglo:
        print(f"{fila[0]:<35} | {fila[1]:<35}")
    print(f"\nPresione cualquier tecla para salir...")
    msvcrt.getch()

def ejecutar_programa():
    conexion = None
    try:
        conexion = psycopg2.connect(
            host="localhost", database="pprueba",
            user="postgres", password="peluche01", port="5432"
        )
        cursor = conexion.cursor()

        print("\n--- SISTEMA DE APRENDIZAJE POR NIVELES ---")
        print("Categorías: [M] Modismos | [V] Verbos Compuestos | [P] Palabras")
        opcion = input("Seleccione Categoría: ").upper()

        config = {
            'M': ('modismos', 3, 'MODISMOS', 'id_modismos'),
            'V': ('verbos_compuestos', 3, 'VERBOS COMPUESTOS', 'id_verbo'),
            'P': ('palabras', 4, 'PALABRAS', 'id_palabra')
        }

        if opcion not in config: return
        tabla, col_texto, nombre, col_id = config[opcion]

        # --- SECCIÓN DE NIVEL CORREGIDA (ENTERO) ---
        try:
            nivel_seleccionado = int(input("Seleccione Nivel (1: Básico, 2: Intermedio, 3: Avanzado): "))
        except ValueError:
            print("Entrada no válida. Usando Nivel 1 por defecto.")
            nivel_seleccionado = 1

        print("\nDIRECCIÓN:")
        print("1. Inglés -> Español")
        print("2. Español -> Inglés")
        direccion_opc = input("Seleccione (1 o 2): ")
        
        # SQL con filtro numérico explícito y orden por ID
        query = f"SELECT * FROM {tabla} WHERE id_nivel = %s ORDER BY {col_id};"
        cursor.execute(query, (nivel_seleccionado,))
        registros_crudos = cursor.fetchall()
        
        if not registros_crudos:
            print(f"\nNo hay registros numéricos para el Nivel {nivel_seleccionado} en {nombre}.")
            return

        diccionario_datos = []
        idioma_audio = "ES" if direccion_opc == '1' else "EN"

        for i in range(0, len(registros_crudos), 2):
            if i + 1 < len(registros_crudos):
                en = str(registros_crudos[i][col_texto]).strip()
                es = str(registros_crudos[i+1][col_texto]).strip()
                if direccion_opc == '2':
                    diccionario_datos.append([es, en])
                else:
                    diccionario_datos.append([en, es])

        modo = input("\n¿Orden Secuencial (S) o Aleatorio (A)?: ").upper()
        if modo == 'A': random.shuffle(diccionario_datos)

        limpiar_pantalla()
        print(f"ESTUDIO: {nombre} | NIVEL: {nivel_seleccionado}")
        print("Control: [Cualquier tecla] Ver Respuesta | [ESC] Salir\n")

        for pareja in diccionario_datos:
            limpiar_pantalla()
            print(f"NIVEL {nivel_seleccionado} - PREGUNTA: {pareja[0]}")
            print("-" * 40)
            
            tecla = ord(msvcrt.getch())
            if tecla == 27: break
            
            print(f"RESPUESTA: {pareja[1]}")
            hablar(pareja[1], idioma_audio)
            
            print("\n[Cualquier tecla para continuar | ESC para salir]")
            tecla = ord(msvcrt.getch())
            if tecla == 27: break

        mostrar_diccionario_completo(diccionario_datos, nombre)

    except Exception as error:
        print(f"Error técnico: {error}")
    finally:
        if conexion:
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    ejecutar_programa()