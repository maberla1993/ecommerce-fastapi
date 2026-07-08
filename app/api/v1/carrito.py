# Este fichero define los endpoints relacionados con el carrito de la compra. 
# Su función es recibir las peticiones HTTP, obtener el usuario autenticado y 
# delegar la lógica de negocio en las funciones del módulo crud.carrito.

# ======================================================
# ENDPOINTS DEL CARRITO DE LA COMPRA
# ======================================================

# Importamos APIRouter para agrupar los endpoints
# relacionados con el carrito.
from fastapi import APIRouter, Depends

# Importamos Session para trabajar con la base de datos.
from sqlalchemy.orm import Session

# Importamos las funciones CRUD del carrito.
from crud import carrito as crud_carrito

# Importamos las dependencias necesarias:
# - get_db: obtiene una sesión con la base de datos.
# - get_current_user: devuelve el usuario autenticado.
from deps.deps import get_db, get_current_user


# Creamos el router del carrito.
api_router = APIRouter()


# ======================================================
# VER EL CONTENIDO DEL CARRITO
# ======================================================

@api_router.get("/", summary="Ver contenido del carrito")
def ver_carrito(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Devuelve el carrito del usuario autenticado.

    Si el usuario todavía no dispone de un carrito,
    se crea automáticamente.
    """

    # Obtenemos el carrito del usuario.
    carrito = crud_carrito.obtener_carrito(db, user.id)

    # Devolvemos el carrito junto con sus productos.
    return carrito


# ======================================================
# AÑADIR UN PRODUCTO AL CARRITO
# ======================================================

@api_router.post("/agregar/{producto_id}")
def agregar_producto(
    producto_id: int,
    cantidad: int = 1,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Añade un producto al carrito del usuario.

    Si el producto ya existe en el carrito,
    incrementa la cantidad.
    """

    # Obtenemos el carrito del usuario.
    carrito = crud_carrito.obtener_carrito(db, user.id)

    # Añadimos el producto al carrito.
    item = crud_carrito.agregar_item(
        db,
        carrito.id,
        producto_id,
        cantidad
    )

    # Devolvemos un mensaje de confirmación.
    return {
        "mensaje": "Producto agregado",
        "item": item
    }


# ======================================================
# ELIMINAR UN PRODUCTO DEL CARRITO
# ======================================================

@api_router.delete("/eliminar/{item_id}")
def eliminar_item(
    item_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Elimina un producto del carrito del usuario.
    """

    # Eliminamos el producto indicado.
    crud_carrito.eliminar_item(db, item_id)

    # Devolvemos un mensaje de confirmación.
    return {
        "mensaje": "Producto eliminado del carrito"
    }