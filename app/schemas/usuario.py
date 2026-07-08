# Este archivo es el encargado de definir los esquemas (schemas) de la API utilizando Pydantic. 
# Los esquemas sirven para validar los datos que llegan a la API y para controlar qué información se devuelve al cliente.

# Importamos BaseModel de Pydantic.
# Todas las clases que hereden de BaseModel servirán para validar los datos de entrada y salida de la API.
from pydantic import BaseModel, EmailStr

# ======================================================
# ESQUEMA PARA CREAR USUARIOS
# ======================================================
class UsuarioBase(BaseModel):

    nombre: str
    email: EmailStr

# hereda nombre y email y añade password y es_admin
class UsuarioCreate(UsuarioBase):
    #contraseña cifrada mas adelante
    password: str
    # control de roles, por defecto no admin
    es_admin: bool = False

class UsuarioResponse(UsuarioBase):
    id: int
    es_admin: bool

    class Config:
        # Permite devolver directamente objetos del ORM de SQLAlchemy.
        orm_mode = True
