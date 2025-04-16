from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from tortoise.exceptions import DoesNotExist
from datetime import datetime, timedelta

from app.models import Prestamo, Libro, Usuario

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

# ---------- ESQUEMAS ----------
class PrestamoIn(BaseModel):
    libro_id: int
    usuario_id: int

class PrestamoOut(BaseModel):
    id: int
    libro_id: int
    usuario_id: int
    fecha_prestamo: str
    fecha_devolucion: Optional[str]
    estado: str

    class Config:
        from_attributes = True

# ---------- ENDPOINTS ----------

# Crear un préstamo
@router.post("/", response_model=PrestamoOut, status_code=201)
async def crear_prestamo(datos: PrestamoIn):
    libro = await Libro.get_or_none(id=datos.libro_id)
    usuario = await Usuario.get_or_none(id=datos.usuario_id)

    if not libro or not usuario:
        raise HTTPException(status_code=404, detail="Libro o usuario no encontrado")

    # Validar que el libro no esté ya prestado
    prestado = await Prestamo.filter(libro=libro, estado="activo").exists()
    if prestado:
        raise HTTPException(status_code=400, detail="El libro ya está prestado")

    prestamo = await Prestamo.create(
        libro=libro,
        usuario=usuario,
        estado="activo"
    )
    return prestamo

# Registrar una devolución
@router.put("/{prestamo_id}/devolver", response_model=PrestamoOut)
async def devolver_prestamo(prestamo_id: int):
    prestamo = await Prestamo.get_or_none(id=prestamo_id)

    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    if prestamo.estado != "activo":
        raise HTTPException(status_code=400, detail="El préstamo ya está cerrado")

    prestamo.fecha_devolucion = datetime.utcnow()
    prestamo.estado = "devuelto"
    await prestamo.save()
    return prestamo

# Listar préstamos activos
@router.get("/activos", response_model=List[PrestamoOut])
async def listar_activos():
    return await Prestamo.filter(estado="activo").all()

# Listar historial completo
@router.get("/historial", response_model=List[PrestamoOut])
async def historial():
    return await Prestamo.all()

# Listar vencidos (préstamos que llevan más de 15 días activos)
@router.get("/vencidos", response_model=List[PrestamoOut])
async def listar_vencidos():
    limite = datetime.utcnow() - timedelta(days=15)
    return await Prestamo.filter(estado="activo", fecha_prestamo__lt=limite).all()
