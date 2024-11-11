from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Ajusta según tu configuración de MySQL
        password='',  # Ajusta según tu configuración de MySQL
        database='wineapp'
    )
    return connection

@app.route('/', methods=['GET'])
def index():
    # Obtener filtros de la URL
    variedad = request.args.get('variedad', None)  # Filtro de variedad
    maridaje = request.args.get('maridaje', None)  # Filtro de maridaje
    orden = request.args.get('orden', None)  # Filtro de ordenación

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Consulta SQL base
    query = 'SELECT * FROM vinos WHERE 1'

    # Lista de parámetros a pasar a la consulta
    query_params = []

    # Aplicar filtro de variedad
    if variedad:
        query += ' AND variedad = %s'  # Usamos 'variedad' aquí
        query_params.append(variedad)
    
    # Aplicar filtro de maridaje
    if maridaje:
        query += ' AND maridaje LIKE %s'
        query_params.append(f'%{maridaje}%')
    
    # Aplicar ordenación
    if orden == 'precio_asc':
        query += ' ORDER BY precio ASC'
    elif orden == 'precio_desc':
        query += ' ORDER BY precio DESC'
    elif orden == 'puntuacion_desc':
        query += ' ORDER BY puntuacion DESC'

    # Ejecutar la consulta con los parámetros adecuados
    cursor.execute(query, tuple(query_params))
    vinos = cursor.fetchall()  # Obtener los resultados
    cursor.close()
    connection.close()

    # Consultar variedades para los filtros
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT variedad FROM vinos')  # Traemos las variedades disponibles
    variedades = cursor.fetchall()  # Trae los tipos de vinos disponibles
    cursor.close()
    connection.close()

    return render_template('index.html', vinos=vinos, variedades=variedades)

if __name__ == '__main__':
    app.run(debug=True)
