# Aquí está toda la lógica que trabaja con la base de datos.
# El archivo main.py únicamente recibe la petición y llama a estas funciones.

from sqlalchemy.orm import Session
from models.categoria import Categoria
from schemas.categoria import CategoriaCreate

#### CATEGORIA ########

def crear_categorias(db: Session, categoria: CategoriaCreate):
    db_categoria = Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def obtener_categorias(db: Session):
    return db.query(Categoria).all()