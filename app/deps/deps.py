# Este fichero es muy importante dentro del sistema de autenticación. 
# Se encarga de definir las dependencias de FastAPI que verifican si un usuario está autenticado 
# y si tiene permisos de administrador antes de acceder a determinados endpoints.

# ======================================================
# DEPENDENCIAS DE AUTENTICACIÓN Y AUTORIZACIÓN
# ======================================================

# OAuth2PasswordBearer obtiene automáticamente el token JWT
# enviado por el cliente en la cabecera:
# Authorization: Bearer <token>
from fastapi.security import OAuth2PasswordBearer

# Importamos las utilidades necesarias de FastAPI
from fastapi import Depends, HTTPException, status

# Excepción que se lanzará si el token no es válido
from jose import JWTError

# Tipo Session para trabajar con la base de datos
from sqlalchemy.orm import Session

# Función que proporciona una sesión con la base de datos
from db.database import SessionLocal

# Función que verifica y decodifica el token JWT
from core.security import verificar_token

# Funciones CRUD de acceso a la base de datos
from crud.usuario import obtener_usuario_por_email

# ======================================================
# ESQUEMA DE AUTENTICACIÓN
# ======================================================

# Indica a FastAPI que el token JWT se obtendrá desde
# el endpoint "/login".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ======================================================
# OBTENER SESION DB
# ======================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ======================================================
# OBTENER EL USUARIO AUTENTICADO
# ======================================================

def get_current_user(
        # Obtiene automáticamente el token enviado
        # en la cabecera Authorization.
        token: str = Depends(oauth2_scheme),

        # Abre una sesión con la base de datos.
        db: Session = Depends(get_db)
):
    """
    Comprueba que el usuario esté autenticado.

    Si el token es válido, devuelve el usuario almacenado
    en la base de datos.

    Si el token no existe, ha caducado o el usuario no
    existe, devuelve un error 401.
    """

    # Excepción que utilizaremos cuando falle la autenticación.
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verificamos el token JWT.
        payload = verificar_token(token)

        # Obtenemos el email almacenado en el campo "sub"
        # (subject) del token.
        email: str | None = payload.get("sub")

        # Si el token no contiene un email,
        # consideramos que es inválido.
        if email is None:
            raise cred_exc

    # Si el token es incorrecto, ha sido modificado
    # o ha caducado.
    except JWTError:
        raise cred_exc

    # Buscamos el usuario en la base de datos
    user = obtener_usuario_por_email(db, email)

    # Si el usuario ya no existe
    if user is None:
        raise cred_exc

    # Devolvemos el usuario autenticado
    return user


# ======================================================
# COMPROBAR SI EL USUARIO ES ADMINISTRADOR
# ======================================================

def require_admin(current_user=Depends(get_current_user)):
    """
    Comprueba que el usuario autenticado tenga
    permisos de administrador.

    Si no los tiene, devuelve un error 403.
    """

    # Verificamos el rol del usuario
    if not current_user.es_admin:
        raise HTTPException(
            status_code=403,
            detail="No autorizado: se requiere rol admin"
        )

