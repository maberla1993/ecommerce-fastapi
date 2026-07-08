# Modelos de la base de datos

# Categoria
#         │
#         │ 1
#         │
#         │
#         ▼
# Producto

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


# ==========================
# TABLA CATEGORIAS
# ==========================
class Categoria(Base):

    # Nombre real de la tabla en PostgreSQL
    __tablename__ = "categorias"

    # Clave primaria
    id = Column(Integer, primary_key=True, index=True)

    # El nombre no podrá repetirse
    nombre = Column(String, unique=True, index=True)

    # Relación uno a muchos
    # Una categoría tiene muchos productos
    productos = relationship(
        "Producto",
        back_populates="categorias"
    )