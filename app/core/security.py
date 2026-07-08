# Este archivo se encarga de la autenticación mediante JWT (JSON Web Token). 
# Su función es crear un token cuando un usuario inicia sesión correctamente 
# y verificar ese token en las peticiones posteriores para comprobar que el usuario está autenticado.

# Importamos las funciones necesarias para trabajar con JWT.
# JWTError se utiliza para capturar errores al validar un token.
# jwt permite crear y verificar tokens.
from operator import sub

from jose import JWTError, jwt

# Importamos las clases para trabajar con fechas y tiempos.
from datetime import datetime, timedelta

# Importamos CryptContext de Passlib.
# Esta clase permite gestionar distintos algoritmos de cifrado
# de contraseñas de forma sencilla.
from passlib.context import CryptContext

from .config import settings


# Creamos el contexto de cifrado.
#
# schemes=["bcrypt"] indica que utilizaremos el algoritmo bcrypt,
# uno de los más seguros y utilizados actualmente para almacenar
# contraseñas.
#
# deprecated="auto" permitirá marcar automáticamente algoritmos
# antiguos como obsoletos si en el futuro cambiamos el método de cifrado.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ======================================================
# CREAR UN TOKEN JWT
# ======================================================

def crear_token(sub: str, es_admin: bool):
    """
    Recibe un diccionario con los datos del usuario
    y genera un token JWT con fecha de expiración.
    """

    # Calculamos la fecha y hora en la que el token dejará de ser válido.
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    data = {
        "sub": sub,
        "exp": expire,
        "es_admin": es_admin
    }

    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


# ======================================================
# VERIFICAR UN TOKEN JWT
# ======================================================

def verificar_token(token: str):
    """
    Comprueba si un token es válido.

    Si el token es correcto devuelve la información almacenada
    en él (payload).

    Si el token es incorrecto, ha sido modificado o ha caducado,
    devuelve None.
    """

    try:
        # Decodificamos el token utilizando la clave secreta.
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Si todo ha ido bien devolvemos los datos del token.
        return payload

    except JWTError:
        # Si ocurre cualquier error (token inválido,
        # modificado o caducado), devolvemos None.
        return None
    
###################################################
##################################################
#     Usuario introduce usuario y contraseña
#                 │
#                 ▼
#       Se comprueban las credenciales
#                 │
#                 ▼
#         crear_token()
#                 │
#                 ▼
#       Se genera un JWT firmado
#                 │
#                 ▼
#  El cliente guarda el token (navegador, app...)
#                 │
#                 ▼
#  En cada petición envía el token en la cabecera
#         Authorization: Bearer <token>
#                 │
#                 ▼
#         verificar_token()
#                 │
#         ┌───────┴────────┐
#         │                │
#   Token válido     Token inválido
#         │                │
#         ▼                ▼
# Acceso permitido   Error 401 Unauthorized


# ======================================================
# CIFRAR UNA CONTRASEÑA
# ======================================================

def hash_password(password: str):
    """
    Recibe una contraseña en texto plano y devuelve
    su versión cifrada (hash).

    Ejemplo:
        Entrada:
            "123456"

        Salida:
            "$2b$12$Hn6hA9..."
    """

    return pwd_context.hash(password)


# ======================================================
# COMPROBAR UNA CONTRASEÑA
# ======================================================

def verify_password(password: str, hashed: str):
    """
    Comprueba si la contraseña introducida por el usuario
    coincide con el hash almacenado en la base de datos.

    Devuelve:
        True  -> si la contraseña es correcta.
        False -> si es incorrecta.
    """

    return pwd_context.verify(password, hashed)