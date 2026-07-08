# Este fichero contiene la lógica para gestionar el carrito de la compra. 
# Permite obtener el carrito de un usuario, añadir productos al carrito y eliminar productos del mismo.

# ======================================================
# OPERACIONES CRUD DEL CARRITO DE LA COMPRA
# ======================================================

# Importamos Session para trabajar con la base de datos.
from sqlalchemy.orm import Session

# Importamos los modelos relacionados con el carrito.
from models.pedidos import Carrito, ItemCarrito


# ======================================================
# OBTENER EL CARRITO DE UN USUARIO
# ======================================================

def obtener_carrito(db: Session, usuario_id: int):
    """
    Busca el carrito asociado a un usuario.

    Si el usuario todavía no tiene un carrito,
    se crea automáticamente y se devuelve.
    """

    # Buscamos el carrito del usuario.
    carrito = (
        db.query(Carrito)
        .filter(Carrito.usuario_id == usuario_id)
        .first()
    )

    # Si no existe, creamos uno nuevo.
    if not carrito:

        carrito = Carrito(usuario_id=usuario_id)

        # Añadimos el carrito a la sesión.
        db.add(carrito)

        # Guardamos los cambios.
        db.commit()

        # Actualizamos el objeto con el ID generado.
        db.refresh(carrito)

    # Devolvemos el carrito encontrado o creado.
    return carrito


# ======================================================
# AÑADIR UN PRODUCTO AL CARRITO
# ======================================================

def agregar_item(
        db: Session,
        carrito_id: int,
        producto_id: int,
        cantidad: int = 1
):
    """
    Añade un producto al carrito.

    Si el producto ya existe en el carrito,
    incrementa la cantidad.

    Si no existe, crea un nuevo registro.
    """

    # Buscamos si el producto ya está en el carrito.
    item = (
        db.query(ItemCarrito)
        .filter(
            ItemCarrito.carrito_id == carrito_id,
            ItemCarrito.producto_id == producto_id
        )
        .first
    )

    # Si ya existe, aumentamos la cantidad.
    if item:
        item.cantidad += cantidad

    # Si no existe, creamos un nuevo elemento.
    else:

        item = ItemCarrito(
            carrito_id=carrito_id,
            producto_id=producto_id,
            cantidad=cantidad
        )

        db.add(item)

    # Guardamos los cambios.
    db.commit()

    # Actualizamos el objeto.
    db.refresh(item)

    # Devolvemos el elemento del carrito.
    return item


# ======================================================
# ELIMINAR UN PRODUCTO DEL CARRITO
# ======================================================

def eliminar_item(db: Session, item_id: int):
    """
    Elimina un producto concreto del carrito.
    """

    # Buscamos el producto por su ID.
    item = db.query(ItemCarrito).get(item_id)

    # Si existe, lo eliminamos.
    if item:

        db.delete(item)

        db.commit()
