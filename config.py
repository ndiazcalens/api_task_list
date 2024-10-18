import os

class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")  # Usa localhost como valor por defecto para desarrollo local
    MYSQL_USER = os.getenv("MYSQL_USER", "root")        # Usa "root" como valor por defecto para desarrollo local
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")     # Usa una cadena vacía como valor por defecto
    MYSQL_DB = os.getenv("MYSQL_DB", "tasks_db")        # Usa "tasks_db" como valor por defecto para desarrollo local

config = {
    "development": DevelopmentConfig
}