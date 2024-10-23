from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import psycopg2
import os
from config import config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración de conexión a PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        database=os.getenv("PG_DB", "tasks_db"),
        user=os.getenv("PG_USER", "postgres"),  
        password=os.getenv("PG_PASSWORD", ""),
        port=os.getenv("PG_PORT", "6543") 
    )
    return conn


print("PG_USER:", os.getenv("PG_USER"))

SWAGGER_URL = '/api/docs'  # URL para exponer Swagger UI (sin barra al final)
API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Configuración de Swagger UI
        'app_name': "Api lista de tareas"
    },
)

app.register_blueprint(swaggerui_blueprint)


@app.route("/", methods=['GET'])
def mostrar_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sqlTasks = "SELECT * FROM tasks"
        cursor.execute(sqlTasks)
        tasks = cursor.fetchall()

        sqlUsers = "SELECT * FROM users"
        cursor.execute(sqlUsers)
        users = cursor.fetchall()

        respuesta = {
            "tasks": [],
            "users": []
        }
        for task in tasks:
            respuesta["tasks"].append({
                "taskID": task[0],
                "userID": task[1],
                "title": task[2],
                "description": task[3]
            })

        for user in users:
            respuesta["users"].append({
                "userID": user[0],
                "userName": user[1],
                "email": user[2],
                "password": user[3]
            })

        cursor.close()
        conn.close()
        return jsonify(respuesta)
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"})


@app.route("/<tabla>", methods=['GET'])
def mostrar_tabla(tabla):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM {};".format(tabla)
        cursor.execute(sql)
        datos = cursor.fetchall()
        if datos:
            respuesta = {
                "datos": datos
            }
        else:
            respuesta = {
                "msj": "No hay datos"
            }
        cursor.close()
        conn.close()
        return jsonify(respuesta)
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"}), 500


@app.route("/<tabla>", methods=['POST'])
def nuevo_dato(tabla):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if tabla == "users":
            sql = """INSERT INTO users (userName, email, password) VALUES 
            (%s, %s, %s);"""
            values = (
                request.json["userName"],
                request.json["email"],
                request.json["password"]
            )
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"msj": "Usuario registrado con éxito"})
        elif tabla == "tasks":
            userID = request.json["userID"]
            cursor.execute("SELECT * FROM users WHERE userID = %s", (userID,))
            user = cursor.fetchone()
            if user is None:
                return jsonify({"msj": "El userID no existe. Inserte un usuario existente."})
            sql = """INSERT INTO tasks (userID, title, description) VALUES 
            (%s, %s, %s);"""
            values = (
                request.json["userID"],
                request.json["title"],
                request.json["description"]
            )
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"msj": "Tarea registrada con éxito"})
        else:
            return jsonify({"msj": "Tabla no encontrada"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"}), 500


@app.route("/<tabla>/<id>", methods=['PUT'])
def actualizar(tabla, id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if tabla == "users":
            sql = "UPDATE users SET userName= %s, email= %s, password= %s WHERE userID = %s"
            values = (
                request.json["userName"],
                request.json["email"],
                request.json["password"],
                id
            )
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"msj": "Usuario actualizado con éxito"})
        elif tabla == "tasks":
            sql = "UPDATE tasks SET title= %s, description= %s WHERE taskID = %s"
            values = (
                request.json["title"],
                request.json["description"],
                id
            )
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"msj": "Tarea actualizada con éxito"})
        else:
            return jsonify({"msj": "La tabla no existe"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"}), 500


@app.route("/<tabla>/<id>", methods=['DELETE'])
def eliminar(tabla, id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if tabla == "users":
            sql = "DELETE FROM users WHERE userID= %s"
            values = (id,)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"msj": "Usuario eliminado con éxito"})
        elif tabla == "tasks":
            sql = "DELETE FROM tasks WHERE taskID= %s"
            values = (id,)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"msj": "Tarea eliminada con éxito"})
        else:
            return jsonify({"msj": "Ingrese un valor correcto"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"})


def pagina_error(error):
    return "Error", 404


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pagina_error)
    app.run()