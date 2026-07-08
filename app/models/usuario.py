from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base
from sqlalchemy.orm import relationship

# ==========================
# TABLA USUARIOS
# ==========================
class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, unique=True, index=True)

    email = Column(String, unique=True, index=True)

    # Aquí se almacenará la contraseña cifrada
    hashed_password = Column(String)

    # control de roles
    es_admin = Column(Boolean, default=False)

    # relación con carrito 1-1
    carrito = relationship("Carrito", back_populates="usuario", uselist=False)