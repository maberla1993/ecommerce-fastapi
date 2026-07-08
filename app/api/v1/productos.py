from fastapi import APIRouter
# Importamos las clases necesarias de FastAPI
from fastapi import Depends, HTTPException
# Importamos el tipo Session de SQLAlchemy para trabajar con la base de datos
from sqlalchemy.orm import Session
# Importamos el archivo donde están las operaciones CRUD y los esquemas de Pydantic
from schemas.producto import ProductoCreate, ProductoResponse
from crud.producto import *
# Importamos la función que crea y cierra automáticamente la conexión con la base de datos
from deps.deps import get_db, require_admin

api_router = APIRouter()

# ======================================================
# ENDPOINTS DE PRODUCTOS
# ======================================================

# Obtener todos los productos
@api_router.get("/productos", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    """
    Devuelve una lista con todos los productos almacenados
    en la base de datos.
    """
    return obtener_productos(db)


# Crear un nuevo producto
# Con dependencies=[Depends(require_admin)] protegemos la ruta para que solo los usuarios admin puedan crear productos
@api_router.post("/productos", response_model=ProductoCreate, dependencies=[Depends(require_admin)])
def agregar_producto(
        producto: ProductoCreate,
        db: Session = Depends(get_db)
):
    """
    Recibe un producto en formato JSON,
    lo guarda en la base de datos y devuelve
    el producto creado.
    """
    return crear_producto(db, producto)


# Actualizar un producto existente
@api_router.put("/productos/{id}", response_model=ProductoCreate)
def actualizar_producto(
        producto_id: int,
        datos: ProductoCreate,
        db: Session = Depends(get_db)
):
    """
    Busca un producto por su ID y actualiza
    todos sus datos.
    """

    # Llamamos a la función del CRUD
    producto = actualizar_productos(db, producto_id, datos)

    # Si no existe el producto devolvemos un error 404
    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Si existe, devolvemos el producto actualizado
    return producto


# Eliminar un producto
@api_router.delete("/productos/{id}")
def eliminar_producto(
        producto_id: int,
        db: Session = Depends(get_db)
):
    """
    Elimina un producto de la base de datos
    utilizando su identificador.
    """

    producto = eliminar_producto(db, producto_id)

    # Si el producto no existe
    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    # Mensaje de confirmación
    return {"mensaje": "Producto eliminado"}
