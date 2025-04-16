from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.models import Libro
from tortoise.exceptions import DoesNotExist

router = APIRouter()

class LibroIn(BaseModel):
    titulo: str
    autor: str
    isbn: str
    categoria: str
    estado: Optional[str] = "disponible"

class LibroOut(LibroIn):
    id: int
    fecha_creacion: str

    class Config:
        orm_mode = True

@router.get("/", response_model=List[LibroOut])
async def listar_libros(titulo: Optional[str] = Query(None), autor: Optional[str] = Query(None), categoria: Optional[str] = Query(None)):
    filtros = {}
    if titulo: filtros["titulo__icontains"] = titulo
    if autor: filtros["autor__icontains"] = autor
    if categoria: filtros["categoria__icontains"] = categoria
    return await Libro.filter(**filtros).all()

@router.get("/{libro_id}", response_model=LibroOut)
async def obtener_libro(libro_id: int):
    try:
        return await Libro.get(id=libro_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.post("/", response_model=LibroOut, status_code=201)
async def crear_libro(libro: LibroIn):
    return await Libro.create(**libro.dict())

@router.put("/{libro_id}", response_model=LibroOut)
async def actualizar_libro(libro_id: int, datos: LibroIn):
    try:
        libro = await Libro.get(id=libro_id)
        await libro.update_from_dict(datos.dict())
        await libro.save()
        return libro
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.delete("/{libro_id}", status_code=204)
async def eliminar_libro(libro_id: int):
    eliminado = await Libro.filter(id=libro_id).delete()
    if not eliminado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")