from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.models import Usuario
from tortoise.exceptions import DoesNotExist
from passlib.hash import bcrypt
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Autenticación"])

SECRET_KEY = "clave_super_secreta"

def crear_token(user_id: int):
    expiracion = datetime.utcnow() + timedelta(hours=1)
    datos = {"user_id": user_id, "exp": expiracion}
    return jwt.encode(datos, SECRET_KEY, algorithm="HS256")

class UsuarioRegistro(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/registro", status_code=201)
async def registrar(usuario: UsuarioRegistro):
    if await Usuario.filter(email=usuario.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    hashed = bcrypt.hash(usuario.password)
    user = await Usuario.create(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        password=hashed,
        rol="usuario",
        activo=True
    )
    return {"mensaje": "Usuario creado", "id": user.id}

@router.post("/login")
async def login(usuario: UsuarioLogin):
    user = await Usuario.filter(email=usuario.email).first()
    if not user or not bcrypt.verify(usuario.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = crear_token(user.id)
    return {"access_token": token, "token_type": "bearer"}