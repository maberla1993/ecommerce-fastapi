# Este fichero define el endpoint encargado de confirmar una compra. 
# Su función es recibir la petición del usuario autenticado, 
# llamar a la lógica de negocio para crear el pedido y devolver la información del pedido generado o un error si no puede realizarse.

# ======================================================
# ENDPOINTS RELACIONADOS CON LOS PEDIDOS
# ======================================================

# Importamos APIRouter para agrupar los endpoints
# relacionados con los pedidos.
from fastapi import APIRouter, Depends, HTTPException

# Importamos Session para trabajar con la base de datos.
from sqlalchemy.orm import Session

# Importamos las dependencias necesarias:
# - get_db: obtiene una sesión con la base de datos.
# - get_current_user: devuelve el usuario autenticado.
from deps.deps import get_db, get_current_user

# Importamos las funciones CRUD relacionadas con pedidos.
from crud import pedido as crud_pedido


# Creamos el router de pedidos.
api_router = APIRouter()


# ======================================================
# CONFIRMAR UN PEDIDO
# ======================================================

@api_router.post("/confirmar", summary="Confirmar producto", response_description="Pedido creado correctamente")
def confirmar_pedido(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Convierte el carrito del usuario autenticado
    en un pedido.

    Si el pedido se crea correctamente, devuelve
    el identificador y el importe total.

    Si el carrito está vacío o se produce algún
    error de validación, devuelve un error 400.
    """

    try:

        # Creamos el pedido a partir del carrito
        # del usuario autenticado.
        pedido = crud_pedido.crear_pedido(
            db,
            user.id
        )

        # Devolvemos la información del pedido creado.
        return {
            "mensaje": "Pedido confirmado correctamente",
            "pedido_id": pedido.id,
            "total": pedido.total
        }

    # Capturamos los errores de validación generados
    # por la capa CRUD y los convertimos en una
    # respuesta HTTP 400 (Bad Request).
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )