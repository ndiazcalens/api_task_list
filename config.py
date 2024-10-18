import os

class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = os.getenv("(la URL o IP de tu base de datos en Railway)", "localhost")  # Usa localhost como valor por defecto para desarrollo local
    MYSQL_USER = os.getenv("(el usuario de la base de datos)", "root")        # Usa "root" como valor por defecto para desarrollo local
    MYSQL_PASSWORD = os.getenv("(la contraseña de la base de datos)", "")     # Usa una cadena vacía como valor por defecto
    MYSQL_DB = os.getenv("MYSQL_DB", "tasks_db")        # Usa "tasks_db" como valor por defecto para desarrollo local

config = {
    "development": DevelopmentConfig
}