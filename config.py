import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env si existe
load_dotenv()

class DevelopmentConfig():
    DEBUG = True
    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_USER = os.getenv("PG_USER", "postgres")
    PG_PASSWORD = os.getenv("PG_PASSWORD", "")
    PG_DB = os.getenv("PG_DB", "tasks_db")
    PG_PORT = os.getenv("PG_PORT", "6543")

# Configuración general de la aplicación
config = {
    "development": DevelopmentConfig
}