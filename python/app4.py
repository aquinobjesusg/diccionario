#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2

DB_CONFIG = {
    'host': "localhost",
    'database': "systemsy_dicc1",
    'user': "systemsy_dicc",
    'password': "systemsy_dicc",
    'port': "5432"
}

def application(environ, start_response):
    """Aplicacion WSGI para Passenger"""
    
    path = environ.get('PATH_INFO', '/')
    
    # Solo mostramos la tabla en la raiz
    if path == '/':
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM palabras")
            palabras = cursor.fetchall()
            
            # Generar HTML - todo en ASCII o con encode correcto
            html = """<!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Tabla Palabras</title>
                <style>
                    body { font-family: Arial; margin: 20px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #4CAF50; color: white; }
                </style>
            </head>
            <body>
                <h1>Tabla Palabras</h1>
                <table border='1'>
            """
            
            if palabras:
                # Cabeceras
                html += "<tr>"
                for desc in cursor.description:
                    html += f"<th>{desc[0]}</th>"
                html += "</tr>"
                
                # Datos
                for palabra in palabras:
                    html += "<tr>"
                    for valor in palabra:
                        html += f"<td>{valor if valor else 'NULL'}</td>"
                    html += "</tr>"
            else:
                html += "<tr><td>No hay datos</td></tr>"
            
            html += """
                </table>
                <p>Total registros: {}</p>
            </body>
            </html>
            """.format(len(palabras))
            
            cursor.close()
            conn.close()
            
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
            return [html.encode('utf-8')]
            
        except Exception as e:
            error_html = f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"
            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
            return [error_html.encode('utf-8')]
    
    # 404
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html; charset=utf-8')])
        # CORRECTO: Usar encode() en lugar de b'string con acentos'
        return ["<h1>404 - Pagina no encontrada</h1>".encode('utf-8')]