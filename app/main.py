from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routes import router as libros_router
from app.auth_routes import router as auth_router
from app.usuarios_routes import router as usuarios_router
from app.config import TORTOISE_ORM
from app.prestamos_routes import router as prestamos_router

app = FastAPI(
    title="API de Gestión de Biblioteca Escolar",
    description="API REST para gestión de libros y usuarios",
    version="1.0.0"
)

app.include_router(libros_router, prefix="/libros", tags=["Libros"])
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(prestamos_router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"mensaje": "Bienvenido a la API de la biblioteca"}