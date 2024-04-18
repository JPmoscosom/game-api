from flask import Flask, jsonify, request
from database.db import get_connection
import psycopg2

app = Flask(__name__)


@app.route('/videojuegos', methods=['GET'])
def obtener_videojuegos():
    cur = get_connection().cursor()
    try:
        cur.execute("SELECT * FROM videojuegos")
        videojuegos = cur.fetchall()
        resultado = []
        for videojuego in videojuegos:
            datos_videojuego = {
                'id': videojuego[0],
                'titulo': videojuego[1],
                'descripcion': videojuego[2],
                'plataforma': videojuego[3],
                'genero': videojuego[4],
                'desarrollador': videojuego[5],
                'editor': videojuego[6],
                'fecha_lanzamiento': videojuego[7].isoformat(),
                'precio': float(videojuego[8]),
                'clasificacion_edad': videojuego[9],
                'puntuacion_media': float(videojuego[10]) if videojuego[10] is not None else None
            }
            resultado.append(datos_videojuego)
        return jsonify(resultado)
    except (Exception, psycopg2.Error) as error:
        return jsonify({'mensaje': 'Error al obtener los videojuegos', 'error': str(error)}), 500
    finally:
        cur.close()


@app.route('/add', methods=['POST', 'GET'])
def agregar_videojuego():
    data = request.get_json()
    print(data)
    cur = get_connection().cursor()
    try:
        cur.execute(
            """INSERT INTO videojuegos (id, titulo, descripcion, plataforma, genero, desarrollador, editor,
            fecha_lanzamiento, precio, clasificacion_edad, puntuacion_media) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s)""",
            (data['id'], data['titulo'], data['descripcion'], data['plataforma'], data['genero'], data['desarrollador'],
             data['editor'], data['fecha_lanzamiento'], data['precio'], data['clasificacion_edad'],
             data['puntuacion_media']))
        get_connection().commit()
        cur.connection.commit()
        return jsonify({'mensaje': 'Videojuego agregado exitosamente'}), 201
    except (Exception, psycopg2.Error) as error:
        return jsonify({'mensaje': 'Error al agregar el videojuego', 'error': str(error)}), 500
    finally:
        cur.close()


@app.route('/videojuegos/delete/<int:id>', methods=['DELETE'])
def eliminar_videojuego(id):
    cur = get_connection().cursor()
    try:
        cur.execute("DELETE FROM videojuegos WHERE id = %s", (id,))
        get_connection().commit()
        return jsonify({'mensaje': 'Videojuego eliminado exitosamente'}), 200
    except (Exception, psycopg2.Error) as error:
        return jsonify({'mensaje': 'Error al eliminar el videojuego', 'error': str(error)}), 500
    finally:
        cur.close()


@app.route('/videojuegos/update/<int:id>', methods=['PATCH'])
def actualizar_videojuego(id):
    data = request.get_json()
    cur = get_connection().cursor()
    try:
        cur.execute(
            "UPDATE videojuegos SET titulo = %s, descripcion = %s, plataforma = %s, genero = %s, desarrollador = %s, "
            "editor = %s, fecha_lanzamiento = %s, precio = %s, clasificacion_edad = %s, puntuacion_media = %s WHERE "
            "id = %s",
            (data['titulo'], data['descripcion'], data['plataforma'], data['genero'], data['desarrollador'],
             data['editor'], data['fecha_lanzamiento'], data['precio'], data['clasificacion_edad'],
             data['puntuacion_media'], id))
        get_connection().commit()
        return jsonify({'mensaje': 'Videojuego actualizado exitosamente'}), 200
    except (Exception, psycopg2.Error) as error:
        return jsonify({'mensaje': 'Error al actualizar el videojuego', 'error': str(error)}), 500
    finally:
        cur.close()


@app.route('/health', methods=['GET'])
def health():  # put application's code here
    return jsonify({"Status de la API de Video Juegos": "200 Todo Melo",
                    "Status de la BD de Video Juegos": "UP"})


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return 'Esta es la API de jueguitos!'


if __name__ == '__main__':
    app.run()
