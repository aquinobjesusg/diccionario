import psycopg2

def inicializar_categorias():
    conexion = None
    try:
        conexion = psycopg2.connect(
            host="localhost", database="pprueba",
            user="postgres", password="peluche01", port="5432"
        )
        cursor = conexion.cursor()

        # Lista de los 9 tipos en el orden solicitado
        tipos = [
            "Sustantivos", "Adjetivos", "Determinantes", 
            "Pronombres", "Verbos", "Adverbios", 
            "Preposiciones", "Conjunciones", "Interjecciones"
        ]

        print("Insertando categorías en tipo_palabra...")
        
        for tipo in tipos:
            cursor.execute("INSERT INTO tipo_palabra (tipo_palabra) VALUES (%s)", (tipo,))
        
        conexion.commit()
        print("¡Categorías inicializadas con éxito!")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if conexion:
            cursor.close()
            conexion.close()

if __name__ == "__main__":
    inicializar_categorias()