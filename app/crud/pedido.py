# Este fichero implementa la lógica para convertir el contenido del carrito de un usuario en un pedido. 
# Además, comprueba el stock disponible, descuenta las unidades compradas, calcula el importe total del pedido 
# y vacía el carrito una vez finalizada la compra.

# ======================================================
# OPERACIONES RELACIONADAS CON LOS PEDIDOS
# ======================================================

# Importamos Session para trabajar con la base de datos.
from sqlalchemy.orm import Session

# Importamos el modelo Producto para consultar
# el precio y el stock disponible.
from models.producto import Producto

# Importamos los modelos relacionados con pedidos.
from models.pedidos import Carrito, DetallePedido, Pedido


# ======================================================
# CREAR UN PEDIDO A PARTIR DEL CARRITO
# ======================================================

def crear_pedido(db: Session, usuario_id: int):
    """
    Convierte el carrito del usuario en un pedido.

    Comprueba que el carrito tenga productos,
    verifica el stock disponible, descuenta las
    unidades compradas, calcula el importe total
    y vacía el carrito.
    """

    # Buscamos el carrito del usuario.
    carrito = (
        db.query(Carrito)
        .filter_by(usuario_id=usuario_id)
        .first()
    )

    # Si el carrito no existe o está vacío,
    # lanzamos una excepción.
    if not carrito or not carrito.items:
        raise ValueError("El carrito está vacío")

    # Inicializamos el importe total del pedido.
    total = 0

    # Creamos el pedido con total 0.
    # El total definitivo se calculará al recorrer
    # todos los productos del carrito.
    pedido = Pedido(
        usuario_id=usuario_id,
        total=0
    )

    # Añadimos el pedido a la base de datos.
    db.add(pedido)

    # Guardamos los cambios para generar el ID.
    db.commit()

    # Actualizamos el objeto con el ID asignado.
    db.refresh(pedido)

    # Recorremos todos los productos del carrito.
    for item in carrito.items:

        # Obtenemos el producto correspondiente.
        producto = db.query(Producto).get(item.producto_id)

        # Si el producto no está disponible o su
        # precio no es válido, lo ignoramos.
        if producto.en_stock is False or producto.precio <= 0:
            continue

        # Comprobamos que haya suficiente stock.
        if item.cantidad > 0 and item.cantidad <= (producto.stock or 0):

            # Descontamos las unidades compradas.
            producto.stock -= item.cantidad

            # Calculamos el subtotal de este producto.
            subtotal = producto.precio * item.cantidad

            # Creamos el detalle del pedido.
            detalle = DetallePedido(
                pedido_id=pedido.id,
                producto_id=producto.id,
                cantidad=item.cantidad,
                subtotal=subtotal
            )

            # Guardamos el detalle.
            db.add(detalle)

            # Acumulamos el importe total.
            total += subtotal

    # Actualizamos el importe total del pedido.
    pedido.total = total

    # Guardamos todos los cambios realizados.
    db.commit()

    # Vaciamos el carrito eliminando todos sus productos.
    for item in carrito.items:
        db.delete(item)

    # Confirmamos la eliminación de los productos del carrito.
    db.commit()

    # Devolvemos el pedido creado.
    return pedido
