# API de Reseñas con Análisis de Sentimiento

## Descripción

Este proyecto consiste en una API REST desarrollada con FastAPI para administrar reseñas ficticias de clientes de un negocio local.

Cada reseña contiene el nombre del cliente, un comentario y una calificación del 1 al 5. La información se almacena en una base de datos SQLite, por lo que los registros permanecen disponibles después de reiniciar el servidor.

La API implementa un CRUD completo que permite crear, listar, consultar, actualizar y eliminar reseñas.

## Funcionalidad de inteligencia artificial

El proyecto incorpora un servicio de inteligencia artificial con dos funcionalidades principales:

1. **Análisis de sentimiento:** analiza el comentario de una reseña y lo clasifica como positivo, neutral o negativo. El resultado se guarda en la base de datos junto con la reseña.

2. **Resumen general:** recopila todos los comentarios almacenados y, cuando el usuario lo solicita, genera un resumen de los temas mencionados con mayor frecuencia, incluyendo aspectos positivos, problemas repetidos y posibles oportunidades de mejora.

El resumen general se genera bajo demanda y no se almacena en la base de datos.

## Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- SQLite
- HTTPX
- Python Dotenv
- Uvicorn
- uv
- Servicio externo de inteligencia artificial

## Validación y manejo de errores

Los datos recibidos son validados mediante modelos Pydantic. Entre las principales reglas se encuentran:

- El nombre del cliente debe tener una longitud válida.
- El comentario debe cumplir una longitud mínima y máxima.
- La calificación debe ser un número entre 1 y 5.

La API devuelve un error 422 cuando los datos enviados no cumplen las validaciones y un error 404 cuando se intenta consultar, actualizar, analizar o eliminar una reseña inexistente.

También se manejan errores de conexión, respuestas inválidas y problemas de comunicación con el servicio de inteligencia artificial.

## Seguridad

La clave utilizada para acceder al modelo de inteligencia artificial se almacena en un archivo `.env` y no se incluye directamente en el código fuente.

El archivo `.env` está excluido del repositorio mediante `.gitignore`. El proyecto incluye un archivo `.env.example` que muestra las variables necesarias sin revelar credenciales reales.

Todos los datos utilizados para demostrar y probar el funcionamiento de la API son ficticios.

## Endpoints principales

- **POST /resenas:** crea una nueva reseña.
- **GET /resenas:** muestra todas las reseñas.
- **GET /resenas/{id}:** obtiene una reseña por su identificador.
- **PUT /resenas/{id}:** actualiza una reseña existente.
- **DELETE /resenas/{id}:** elimina una reseña.
- **POST /resenas/{id}/analizar:** analiza y guarda el sentimiento de una reseña.
- **POST /resenas/resumen-general:** genera un resumen general de los temas más frecuentes en todos los comentarios.

## Instalación y ejecución

Después de clonar el repositorio, las dependencias se instalan con `uv sync`.

Antes de ejecutar la aplicación, debe crearse un archivo `.env` tomando como referencia `.env.example` y completando las variables relacionadas con el servicio de inteligencia artificial.

La aplicación puede iniciarse con `uv run fastapi dev main.py`.

Una vez iniciado el servidor, la documentación interactiva estará disponible en la ruta `/docs`.

## Documentación

La documentación automática de FastAPI permite consultar los endpoints, revisar los modelos de datos y realizar pruebas directamente desde el navegador.

El repositorio incluye capturas de la documentación interactiva en las que se muestra el CRUD de reseñas y el funcionamiento de los endpoints de inteligencia artificial.