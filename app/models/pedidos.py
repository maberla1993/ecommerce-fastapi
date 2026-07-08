# Este fichero define los modelos relacionados con el proceso de compra de la aplicación: el carrito de la compra, 
# los productos que contiene, los pedidos realizados y el detalle de cada pedido.

# ======================================================
# MODELOS RELACIONADOS CON CARRITOS Y PEDIDOS
# ======================================================

# Importamos los tipos de columnas que utilizaremos
# para definir las tablas de la base de datos.
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey

# Permite establecer relaciones entre tablas.
from sqlalchemy.orm import relationship

# Clase base de la que heredarán todos los modelos.
from db.database import Base

# Se utiliza para asignar automáticamente la fecha
# de creación del pedido.
from datetime import datetime


# ======================================================
# TABLA CARRITOS
# ======================================================

class Carrito(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "carritos"

    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Usuario propietario del carrito
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )

    # Relación con la tabla Usuario
    # Un usuario tiene un único carrito.
    usuario = relationship(
        "Usuario",
        back_populates="carrito"
    )

    # Relación uno a muchos con ItemCarrito.
    # Un carrito puede contener varios productos.
    #
    # cascade="all, delete" indica que, si se elimina
    # el carrito, también se eliminarán automáticamente
    # todos los productos contenidos en él.
    items = relationship(
        "ItemCarrito",
        back_populates="carrito",
        cascade="all, delete"
    )


# ======================================================
# TABLA ITEMS DEL CARRITO
# ======================================================

class ItemCarrito(Base):

    __tablename__ = "items_carrito"

    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Carrito al que pertenece este producto
    carrito_id = Column(
        Integer,
        ForeignKey("carritos.id")
    )

    # Producto añadido al carrito
    producto_id = Column(
        Integer,
        ForeignKey("productos.id")
    )

    # Número de unidades del producto
    cantidad = Column(Integer, default=1)

    # Relación con el carrito
    carrito = relationship(
        "Carrito",
        back_populates="items"
    )

    # Relación con el producto
    producto = relationship("Producto")


# ======================================================
# TABLA PEDIDOS
# ======================================================

class Pedido(Base):

    __tablename__ = "pedidos"

    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Usuario que ha realizado el pedido
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )

    # Fecha de creación del pedido.
    # Se asigna automáticamente la fecha y hora actuales.
    fecha = Column(
        DateTime,
        default=datetime.now
    )

    # Importe total del pedido
    total = Column(Float)

    # Relación con el detalle del pedido.
    # Un pedido puede contener varios productos.
    detalles = relationship(
        "DetallePedido",
        back_populates="pedido"
    )


# ======================================================
# TABLA DETALLES DEL PEDIDO
# ======================================================

class DetallePedido(Base):

    __tablename__ = "detalles_pedido"

    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # Pedido al que pertenece este detalle
    pedido_id = Column(
        Integer,
        ForeignKey("pedidos.id")
    )

    # Producto comprado
    producto_id = Column(
        Integer,
        ForeignKey("productos.id")
    )

    # Cantidad comprada
    cantidad = Column(Integer)

    # Importe correspondiente a este producto
    # (precio × cantidad)
    subtotal = Column(Float)

    # Relación con el pedido
    pedido = relationship(
        "Pedido",
        back_populates="detalles"
    )

    # Relación con el producto
    producto = relationship("Producto")