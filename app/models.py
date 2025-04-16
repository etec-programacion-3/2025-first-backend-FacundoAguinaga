from tortoise import fields, models

class Libro(models.Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13, unique=True)
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)

class Usuario(models.Model):
    id = fields.IntField(pk=True)
    nombre = fields.CharField(max_length=100)
    apellido = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    rol = fields.CharField(max_length=50)
    activo = fields.BooleanField(default=True)
    fecha_creacion = fields.DatetimeField(auto_now_add=True)