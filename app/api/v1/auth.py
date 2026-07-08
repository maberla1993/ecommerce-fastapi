from fastapi import APIRouter
# Importamos el archivo donde están las operaciones CRUD y los esquemas de Pydantic
from schemas.usuario import UsuarioResponse, UsuarioCreate
from schemas.token import Token
from crud.usuario import crear_usuario, obtener_usuario_por_email
# Importamos las clases necesarias de FastAPI
from fastapi import Depends, HTTPException, status
# Importamos la función que crea y cierra automáticamente la conexión con la base de datos
# Importamos el tipo Session de SQLAlchemy para trabajar con la base de datos
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password, crear_token
from deps.deps import get_db, get_current_user, require_admin


api_router = APIRouter()

# ======================================================
# ENDPOINTS DE USUARIOS
# ======================================================

# Crea un nuevo usuario en la base de datos.
@api_router.post("/usuarios", response_model= UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
        usuario: UsuarioCreate,
        db: Session = Depends(get_db)
):
    try:
        return crear_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# login
@api_router.post("/login", response_model=Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = obtener_usuario_por_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    token = crear_token(sub = user.email, es_admin = user.es_admin)
    return {"access_token": token, "token_type": "bearer"}

@api_router.get("/usuarios/me", response_model= UsuarioResponse)
def leer_perfil(current_user = Depends(get_current_user)):
    return current_user

# devuelve rol
@api_router.get("/admin/ping")
def admin_ping(_admin = Depends(require_admin)):
    return {"ok": True, "role": "admin"}