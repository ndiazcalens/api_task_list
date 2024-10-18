# Usa la imagen base de Python 3.9 en su versión ligera
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia todos los archivos del directorio actual al contenedor
COPY . .

# Instala las dependencias desde requirements.txt
RUN pip install -r requirements.txt

# Define el comando por defecto para ejecutar tu aplicación
CMD ["python", "app.py"]
