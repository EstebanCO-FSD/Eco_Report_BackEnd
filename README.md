# ---------------------------
# Documentación del proyecto
# ---------------------------

## Descripción
Backend en Python (FastAPI) con MongoDB Atlas para reportar fuentes de contaminación en Bogotá.

El proyecto sigue una arquitectura en capas usando patrones DAO y DTO con POO. La API (main.py) recibe requests y llama a la lógica/servicios (main.py + dao.py), que valida y procesa los datos antes de acceder a la base de datos MongoDB mediante el DAO (dao.py). Los modelos DTO (dto.py) definen la estructura y validación de los datos, y los ObjectId de MongoDB se convierten a strings para compatibilidad con Pydantic.


## Requisitos
- Python 3.9+
- Cuenta en [MongoDB Atlas](https://www.mongodb.com/atlas)


## Instalación
```bash
pip install -r requirements.txt
```


## Ejecución
```bash
uvicorn main:app --reload
```


## Documentación Swagger
Al iniciar el servidor, la documentación interactiva de los servicios se encuentra en:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)


## Endpoints principales
- **POST /reports** → Crear reporte
- **GET /reports** → Listar reportes
- **GET /reports/{id}** → Obtener reporte por ID
- **PUT /reports/{id}** → Actualizar reporte
- **DELETE /reports/{id}** → Eliminar reporte
- **GET /health** → Estado de la conexión