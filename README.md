# API REST - Lista de Tareas

Una API REST desarrollada en **Python** con **Flask** para gestionar una base de datos **PostgreSQL**. Esta API permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre una lista de tareas, vinculadas a usuarios mediante claves foráneas.

## Descripción del proyecto

Esta API contiene dos entidades principales:

- **Usuarios**: Representa a los usuarios que realizan las tareas.
- **Tareas**: Cada tarea tiene un ID único, descripción y un `userID` como clave foránea que vincula la tarea a un usuario.

El propósito de este proyecto es demostrar habilidades en el desarrollo de aplicaciones backend, integrando Flask como framework web y PostgreSQL como base de datos.

---

## Endpoints disponibles

### Usuarios

| Método  | Ruta            | Descripción                         |
|---------|-----------------|-------------------------------------|
| GET     | `/users`        | Obtener todos los usuarios          |
| GET     | `/users/<id>`   | Obtener un usuario específico       |
| POST    | `/users`        | Crear un nuevo usuario              |
| PUT     | `/users/<id>`   | Actualizar un usuario existente     |
| DELETE  | `/users/<id>`   | Eliminar un usuario específico      |

### Tareas

| Método  | Ruta            | Descripción                         |
|---------|-----------------|-------------------------------------|
| GET     | `/tasks`        | Obtener todas las tareas            |
| GET     | `/tasks/<id>`   | Obtener una tarea específica        |
| POST    | `/tasks`        | Crear una nueva tarea               |
| PUT     | `/tasks/<id>`   | Actualizar una tarea existente      |
| DELETE  | `/tasks/<id>`   | Eliminar una tarea específica       |

---

## Tecnologías utilizadas

- **Lenguaje**: Python
- **Framework**: Flask
- **Base de datos**: PostgreSQL
- **Control de versiones**: Git
- **Pruebas**: Postman

---

## Requisitos previos

1. Tener Python 3.10 o superior instalado.
2. Tener PostgreSQL configurado en tu entorno local o en un servidor remoto.
3. Clonar este repositorio:
   ```bash
   git clone https://github.com/tuusuario/api-task-list.git
   cd api-task-list
4.Crear un entorno virtual e instalar dependencias:
  python -m venv env
  source env/Scripts/activate      # Para Windows
  source env/bin/activate          # Para Linux/Mac
  pip install -r requirements.txt
  
5.Configurar las variables de entorno creando un archivo .env con el siguiente contenido:
  PG_HOST=tu_host
  PG_USER=tu_usuario
  PG_PASSWORD=tu_password
  PG_DB=tu_base_de_datos
  PG_PORT=5432

---

## Uso de la API
1. Inicia el servidor:
  flask run
2.Accede a la API en http://localhost:5000 o el dominio donde esté alojada.
3.Realiza peticiones a los endpoints utilizando herramientas como Postman o cURL.

---

## Archivo Postman
En el repositorio encontrarás un archivo api_task_list.postman_collection.json que contiene todas las peticiones preconfiguradas para probar la API. Puedes importar este archivo en Postman para facilitar las pruebas.

---

## Despliegue
La API está desplegada en Vercel y puede ser accedida en el siguiente enlace:
[https://api-task-list.vercel.app](https://api-task-list-ochre.vercel.app)

---

## Autor
Nicolás Díaz Calens

Desarrollador Backend Freelance
