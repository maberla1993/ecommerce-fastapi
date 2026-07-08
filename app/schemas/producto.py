# Este archivo es el encargado de definir los esquemas (schemas) de la API utilizando Pydantic. 
# Los esquemas sirven para validar los datos que llegan a la API y para controlar qué información se devuelve al cliente.

# Importamos BaseModel de Pydantic.
# Todas las clases que hereden de BaseModel servirán para validar los datos de entrada y salida de la API.
from pydantic import BaseModel


# ======================================================
# ESQUEMA PARA CREAR PRODUCTOS
# ======================================================

class ProductoCreate(BaseModel):
    # Nombre del producto
    nombre: str

    # Precio del producto
    precio: float

    # Indica si el producto está disponible
    en_stock: bool

    # ID de la categoría a la que pertenece el producto
    categoria_id: int

    stock: int


# ======================================================
# ESQUEMA DE RESPUESTA DE PRODUCTOS
# ======================================================

# Hereda todos los campos de ProductoCreate
# y añade el campo id, que genera automáticamente la base de datos.
class ProductoResponse(ProductoCreate):

    # Identificador único del producto
    id: int

    class Config:
        # Permite convertir automáticamente un objeto de SQLAlchemy
        # en un objeto de Pydantic sin necesidad de hacerlo manualmente.
        orm_mode = True