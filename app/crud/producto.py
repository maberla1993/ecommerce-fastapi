# Aquí está toda la lógica que trabaja con la base de datos.
# El archivo main.py únicamente recibe la petición y llama a estas funciones.

from sqlalchemy.orm import Session
from models.producto import Producto
from schemas.producto import ProductoCreate

#### PRODUCTO ########

def crear_producto(db: Session, producto: ProductoCreate):

    # Convierte el esquema recibido en un objeto Producto
    db_producto = Producto(**producto.dict())

    # Lo añade a la sesión
    db.add(db_producto)

    # Guarda los cambios
    db.commit()

    # Actualiza el objeto con el ID generado por PostgreSQL
    db.refresh(db_producto)

    return db_producto

def obtener_productos(db: Session):

    # Devuelve todos los productos
    return db.query(Producto).all()

def obtener_producto(db: Session, producto_id: int):

    # Busca el primer producto cuyo id coincida
    return (
        db.query(Producto)
        .filter(Producto.id == producto_id)
        .first()
    )

def actualizar_productos(db:Session, producto_id: int, datos:ProductoCreate):
    producto = obtener_producto(db, producto_id)

    if producto:
        for key, value in datos.dict().items():
            setattr(producto, key, value)
        db.commit()
        db.refresh(producto)
    return producto

def eliminar_producto(db:Session, producto_id: int):
    producto = obtener_producto(db, producto_id)

    if producto:
        db.delete(producto)
        db.commit()
    return producto