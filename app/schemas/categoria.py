# Este archivo es el encargado de definir los esquemas (schemas) de la API utilizando Pydantic. 
# Los esquemas sirven para validar los datos que llegan a la API y para controlar qué información se devuelve al cliente.

# Importamos BaseModel de Pydantic.
# Todas las clases que hereden de BaseModel servirán para validar los datos de entrada y salida de la API.
from pydantic import BaseModel

# ======================================================
# ESQUEMA BASE DE CATEGORÍAS
# ======================================================

# Contiene los campos comunes que utilizarán otros esquemas.
class CategoriaBase(BaseModel):

    # Nombre de la categoría
    nombre: str


# ======================================================
# ESQUEMA PARA CREAR CATEGORÍAS
# ======================================================

# Hereda todos los campos de CategoriaBase.
# De momento no añade ningún campo nuevo, pero esta estructura
# facilita ampliar el proyecto en el futuro.
class CategoriaCreate(CategoriaBase):
    pass


# ======================================================
# ESQUEMA DE RESPUESTA DE CATEGORÍAS
# ======================================================

# Hereda el campo "nombre" y añade el identificador.
class CategoriaResponse(CategoriaBase):

    # ID generado por la base de datos
    id: int

    class Config:
        # Permite devolver directamente objetos del ORM de SQLAlchemy.
        orm_mode = True
