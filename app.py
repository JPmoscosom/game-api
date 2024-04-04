from flask import Flask, request, jsonify
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


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return 'Esta es la API de jueguitos!'



if __name__ == '__main__':
    app.run()
