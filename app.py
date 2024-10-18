from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_mysqldb import MySQL
from config import config
import os

app=Flask(__name__)

conexion= MySQL(app)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
#API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)
API_URL = "/static/swagger.json"



swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Api de ejemplo"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)




@app.route("/", methods=['GET'])
def mostrar_db():
    try: 
        cursor= conexion.connection.cursor()

        sqlTasks= "SELECT * FROM `tasks`"
        cursor.execute(sqlTasks)
        tasks= cursor.fetchall()

        sqlUsers= "SELECT * FROM `users`"
        cursor.execute(sqlUsers)
        users= cursor.fetchall()

        respuesta= {
            "tasks":[],
            "users": []
        }
        for task in tasks:
            respuesta["tasks"].append({
                "tasksID": task[0],
                "userID":task[1],
                "title": task[2],
                "description": task[3]
                })
# Itera sobre cada usuario en la lista de usuarios y agrega sus datos a la respuesta.
# Cada usuario se representa como un diccionario con los campos userID, userName y email.
# Se pueden agregar mas campos segun el esquema de tu base de datos.
        for user in users:
            respuesta["users"].append({
                "userID": user[0],
                "userName": user[1],
                "email": user[2],
                "password": user[3]
            })

        return jsonify(respuesta)
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"})


@app.route("/<tabla>", methods= ['GET'])
def mostrar_tabla(tabla):
    try: 
        cursor= conexion.connection.cursor()
        sql= "SELECT * FROM `{0}`;".format(tabla)
        cursor.execute(sql)
        datos= cursor.fetchall()
        if datos is not None and len(datos)>0:
            respuesta={
                "datos": datos
                }
        else:
            respuesta= {
            "msj": "No hay datos"
        }
        return jsonify(respuesta)
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"}),500



@app.route("/<tabla>", methods= ['POST'])
def nuevo_dato(tabla):
    try:
        cursor= conexion.connection.cursor()
        if tabla == "users":
            sql= """INSERT INTO users (`userName`,`email`,`password`) VALUES 
            (%s, %s, %s);"""
            values=(
                request.json["userName"],
                request.json["email"],
                request.json["password"]
                )
            cursor.execute(sql, values)
            conexion.connection.commit()
            return jsonify({"msj": "Usuario registrado con exito"})
        elif tabla == "tasks":
            userID= request.json["userID"]
            cursor.execute("SELECT * FROM users WHERE userID = %s", (userID,))
            user = cursor.fetchone()
            if user == None:
                 return jsonify({"msj": "El userID no existe. Inserte un usuario existente."})
            sql= """INSERT INTO tasks (`userID`,`title`,`description`) VALUES 
            (%s, %s, %s);"""#aca use placeholders (%s) que cada espacio despues es reemplazado por el valor en vaules
            values= (
            request.json["userID"],
            request.json["title"],
            request.json["description"])
            cursor.execute(sql, values)
            conexion.connection.commit()
            return jsonify({"msj": "Tarea registrada con exito"})
        else:
            return jsonify({"msj": "Tabla no encontrada"}),400
    except Exception as ex:
        print(ex)
        return jsonify({"msj": "Error"}),500


@app.route("/<tabla>/<id>", methods=['PUT'])
def actualizar(tabla, id):
    try:
        cursor= conexion.connection.cursor()
        if tabla == "users":
            sql= "UPDATE users SET userName= %s, email= %s, password= %s WHERE userID = %s"
            values= (
                request.json["userName"],
                request.json["email"],
                request.json["password"],
                id
            )
            cursor.execute(sql,values)
            conexion.connection.commit()
            return (jsonify({"msj": "Usuario actualizado con exito"}))
        elif tabla == "tasks":
            sql= "UPDATE tasks SET title= %s, description= %s WHERE taskID = %s"
            values= (
                request.json["title"],
                request.json["description"],
                id
            )
            cursor.execute(sql,values)
            conexion.connection.commit()
            return (jsonify({"msj": "Tarea actualizada con exito"}))
        else:
            return (jsonify({"msj": "La tabla no existe"})),400
    except Exception as ex:
        print(ex)
        return jsonify({"msj":"Error"}),500



@app.route("/<tabla>/<id>", methods= ['DELETE'])
def eliminar(tabla,id):
    try:
        cursor= conexion.connection.cursor()
        if tabla == "users":
            sql= "DELETE FROM users WHERE userID= %s"
            values= (id,)
            cursor.execute(sql,values)
            conexion.connection.commit()
            return(jsonify({"msj": "Usuario eliminado con exito"}))
        elif tabla == "tasks":
            sql= "DELETE FROM tasks WHERE taskID= %s"
            values= (id,)
            cursor.execute(sql,values)
            conexion.connection.commit()
            return(jsonify({"msj": "Tarea eliminada con exito"}))
        else:
            return(jsonify({"msj": "Ingrese un valor correcto"}))
    except Exception as ex:
        print(ex)
        return (jsonify({"msj":"Error"}))

def pagina_error(error):
    return ("Error"), 404

if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pagina_error)
    app.run()