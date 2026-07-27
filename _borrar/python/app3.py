
import psycopg2


# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================
DB_CONFIG = {
    'host': "localhost",
    'database': "systemsy_dicc1",
    'user': "systemsy_dicc",
    'password': "systemsy_dicc",
    'port': "5432"
}


# =============================================================================
# FUNCIONES DE BASE DE DATOS
# =============================================================================
def get_db_connection():
    """Obtiene conexión a la base de datos"""
    return psycopg2.connect(**DB_CONFIG)


def obtener_par(idx, lista, col_idx, idioma_ori):
    """Obtiene el par de palabras (origen-destino) según el idioma de origen"""
    if not lista or idx + 1 >= len(lista):
        return "---", "---", 'en'
    
    reg1, reg2 = lista[idx], lista[idx + 1]
    
    # Determinar cuál es inglés (id_lenguaje=1) y cuál español (id_lenguaje=2)
    palabra_ing = reg1[col_idx] if reg1[1] == 1 else reg2[col_idx]
    palabra_esp = reg1[col_idx] if reg1[1] == 2 else reg2[col_idx]
    
    if idioma_ori == "Español":
        return palabra_esp, palabra_ing, 'en'
    else:
        return palabra_ing, palabra_esp, 'es'


def obtener_datos_db(categoria, nivel, tipos_sel=None, subtipos_sel=None):
    """Obtiene datos de la base de datos según filtros"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        mapeo = {
            "Palabras": ("palabras", "id_palabra", 4, "id_tipo_palabra"),
            "Modismos": ("modismos", "id_modismo", 3, None),
            "Verbos Compuestos": ("verbos_compuestos", "id_verbo", 3, None)
        }
        
        if categoria not in mapeo:
            return [], 0
        
        tabla, id_col, col_idx, col_tipo = mapeo[categoria]
        query = f"SELECT * FROM {tabla} WHERE id_nivel = %s "
        params = [int(nivel)]
        
        if col_tipo and tipos_sel:
            query += f"AND {col_tipo} IN ({','.join(['%s'] * len(tipos_sel))}) "
            params.extend(tipos_sel)
            
            # Filtro por subtipo para verbos
            if tabla == "palabras" and subtipos_sel:
                query += f"AND subtipo IN ({','.join(['%s'] * len(subtipos_sel))}) "
                params.extend(subtipos_sel)
        
        query += f"ORDER BY {id_col}"
        cur.execute(query, tuple(params))
        datos = cur.fetchall()
        cur.close()
        conn.close()
        return datos, col_idx
    except Exception as e:
        print(f"Error en BD: {e}")
        return [], 0


def cargar_datos(categoria, nivel, tipos=None, subtipos=None, idioma_ori="Español"):
    """
    Función principal para cargar datos desde la base de datos
    
    Parámetros:
    - categoria: "Palabras", "Modismos" o "Verbos Compuestos"
    - nivel: 1, 2 o 3
    - tipos: lista de IDs de tipos (ej: [1, 5, 10] para palabras)
    - subtipos: lista de IDs de subtipos (para tiempos verbales)
    - idioma_ori: "Español" o "Inglés"
    
    Retorna:
    - dict con 'success', 'total' y 'palabras' (lista de {origen, destino, idx})
    """
    try:
        datos, col_idx = obtener_datos_db(categoria, nivel, tipos, subtipos)
        total_p = len(datos) // 2
        
        # Preparar datos
        palabras = []
        for i in range(0, len(datos), 2):
            if i + 1 < len(datos):
                origen, destino, _ = obtener_par(i, datos, col_idx, idioma_ori)
                palabras.append({
                    'origen': origen,
                    'destino': destino,
                    'idx': i
                })
        
        return {
            'success': True,
            'total': total_p,
            'palabras': palabras,
            'datos_raw': datos,
            'col_idx': col_idx
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'total': 0,
            'palabras': []
        }


# =============================================================================
# FUNCIONES DE ACTUALIZACIÓN (si las necesitas)
# =============================================================================
def actualizar_nivel_usuario(usuario_id, nuevo_nivel):
    """Actualiza el nivel de un usuario"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = "UPDATE usuarios SET nivel = %s WHERE id = %s"
        cur.execute(query, (nuevo_nivel, usuario_id))
        conn.commit()
        cur.close()
        conn.close()
        return True, "Nivel actualizado"
    except Exception as e:
        return False, str(e)


def obtener_estadisticas_usuario(usuario_id):
    """Obtiene estadísticas de progreso del usuario"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT COUNT(*) as total_aciertos 
            FROM progreso 
            WHERE usuario_id = %s AND estado = 'CORRECTO'
        """
        cur.execute(query, (usuario_id,))
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return 0


# =============================================================================
# EJEMPLO DE USO
# =============================================================================
if __name__ == "__main__":
    # Ejemplo: Cargar palabras del nivel 1 con tipos específicos
    resultado = cargar_datos(
        categoria="Palabras",
        nivel=1,
        tipos=[1, 5],  # Sustantivos y Verbos Regulares
        subtipos=[1],   # Forma Base/Presente
        idioma_ori="Español"
    )
    
    if resultado['success']:
        print(f"Total de palabras cargadas: {resultado['total']}")
        for palabra in resultado['palabras'][:300]:  # Mostrar primeras 5
            print(f"{palabra['origen']} -> {palabra['destino']}")
    else:
        print(f"Error: {resultado.get('error')}")