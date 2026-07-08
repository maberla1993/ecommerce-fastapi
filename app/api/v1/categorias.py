from fastapi import APIRouter
# Importamos las clases necesarias de FastAPI
from fastapi import Depends
# Importamos el tipo Session de SQLAlchemy para trabajar con la base de datos
from sqlalchemy.orm import Session
# Importamos el archivo donde están las operaciones CRUD y los esquemas de Pydantic
from crud.categoria import crear_categorias, obtener_categorias
from schemas.categoria import CategoriaResponse, CategoriaCreate
# Importamos la función que crea y cierra automáticamente la conexión con la base de datos
from deps.deps import get_db


api_router = APIRouter()

# ======================================================
# ENDPOINTS DE CATEGORÍAS
# ======================================================

# Crear una nueva categoría
@api_router.post("/categorias", response_model= CategoriaResponse)
def crear_categoria(
        categoria: CategoriaCreate,
        db: Session = Depends(get_db)
):
    """
    Crea una nueva categoría en la base de datos.
    """
    return crear_categorias(db, categoria)


# Obtener todas las categorías
@api_router.get("/categorias", response_model=list[CategoriaResponse])
def listar_categoria(db: Session = Depends(get_db)):
    """
    Devuelve todas las categorías registradas.
    """
    return obtener_categorias(db)
