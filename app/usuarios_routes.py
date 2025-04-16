from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.models import Usuario
from tortoise.exceptions import DoesNotExist

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    rol: str
    activo: bool
    fecha_creacion: str

    class Config:
        orm_mode = True

class UsuarioUpdate(BaseModel):
    nombre: str
    apellido: str

@router.get("/", response_model=list[UsuarioOut])
async def listar_usuarios():
    return await Usuario.all()

@router.get("/{usuario_id}", response_model=UsuarioOut)
async def obtener_usuario(usuario_id: int):
    try:
        return await Usuario.get(id=usuario_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.put("/{usuario_id}", response_model=UsuarioOut)
async def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate):
    try:
        usuario = await Usuario.get(id=usuario_id)
        usuario.nombre = datos.nombre
        usuario.apellido = datos.apellido
        await usuario.save()
        return usuario
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
