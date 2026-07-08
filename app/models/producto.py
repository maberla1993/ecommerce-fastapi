# Modelos de la base de datos

# Categoria
#         │
#         │ 1
#         │
#         │
#         ▼
# Producto

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

# ==========================
# TABLA PRODUCTOS
# ==========================
class Producto(Base):

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, index=True)

    precio = Column(Float)

    # Valor por defecto
    en_stock = Column(Boolean, default=True)

    # Clave foránea
    categoria_id = Column(
        Integer,
        ForeignKey("categorias.id")
    )

    # Relación con Categoría
    categorias = relationship(
        "Categoria",
        back_populates="productos"
    )

    stock = Column(Integer, default=0)