# Aquí está toda la lógica que trabaja con la base de datos.
# El archivo main.py únicamente recibe la petición y llama a estas funciones.

from sqlalchemy.orm import Session
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate
from core.security import hash_password
from sqlalchemy import or_

#### USUARIO ########

# Buscar un usuario por su correo electrónico.
# Devuelve el objeto Usuario si existe o None en caso contrario.
def obtener_usuario_por_email(db: Session, email: str) -> Usuario | None:

    # Buscamos el primer usuario cuyo email coincida
    return (
        db.query(Usuario)
        .filter(Usuario.email == email)
        .first()
    )


# Buscar un usuario por su identificador.
# Devuelve el usuario si existe o None si no se encuentra.
def obtener_usuario_por_id(db: Session, usuario_id: int) -> Usuario | None:

    # Buscamos el usuario utilizando su clave primaria
    return (
        db.query(Usuario)
        .filter(Usuario.id == usuario_id)
        .first()
    )


# Crear un nuevo usuario en la base de datos.
def crear_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:

    # Comprobamos que no exista otro usuario con el mismo correo electrónico o el mismo nombre.
    existe = db.query(Usuario).filter(
        or_(
            Usuario.email == usuario.email,
            Usuario.nombre == usuario.nombre
        )
    ).first()

    # Si ya existe un usuario con alguno de esos datos, lanzamos una excepción.
    if existe:
        raise ValueError("Ya existe un usuario con ese email o nombre")

    # Creamos el objeto Usuario.
    # La contraseña nunca se almacena en texto plano, sino que se cifra utilizando bcrypt mediante la función hash_password().
    db_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hash_password(usuario.password),
        es_admin=usuario.es_admin
    )

    # Añadimos el nuevo usuario a la sesión
    db.add(db_usuario)

    # Guardamos los cambios en la base de datos
    db.commit()

    # Actualizamos el objeto con los datos generados por la BD
    # (por ejemplo, el ID asignado automáticamente).
    db.refresh(db_usuario)

    # Devolvemos el usuario creado
    return db_usuario