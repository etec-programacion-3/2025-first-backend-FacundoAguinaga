# 2025-first-backend-FacundoAguinaga

Este proyecto es un **Sistema de Gestión de Biblioteca** desarrollado como parte de GitHub Classroom. Permite administrar libros de una biblioteca escolar mediante una API REST y una interfaz web.

## Tecnologías utilizadas

- **Backend:** FastAPI, Tortoise ORM, SQLite
- **Frontend:** HTML, Bootstrap, JavaScript (fetch API)
- **Otros:** CORS habilitado para desarrollo local

## Estructura de archivos principales

- `main.py`: API REST con endpoints para CRUD de libros, búsqueda y estadísticas.
- `index.html`: Interfaz web para gestionar libros y visualizar estadísticas.
- `requirements.txt`: Dependencias del backend.
- `requests.http`: Archivo de pruebas para la API (compatible con REST Client de VSCode).

## Endpoints principales

- `GET /libros`: Listar libros (con paginación)
- `POST /libros`: Crear libro
- `PUT /libros/{id}`: Actualizar libro
- `DELETE /libros/{id}`: Eliminar libro
- `GET /libros/buscar`: Buscar y filtrar libros
- `GET /estadisticas`: Estadísticas generales

## Ejecución del backend

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```
   El backend estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Uso de la interfaz web

Abre `index.html` en tu navegador. La interfaz se conecta automáticamente al backend para mostrar y gestionar los libros.

## Ejemplo de uso de la API

Puedes probar la API usando el archivo `requests.http` con la extensión REST Client de VSCode, o usando herramientas como Postman.

---

Proyecto realizado por Facundo Aguinaga.
