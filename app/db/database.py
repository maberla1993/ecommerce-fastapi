# Importaciones necesarias de SQLAlchemy
from sqlalchemy import create_engine                 # Crea la conexión con la base de datos
from sqlalchemy.ext.declarative import declarative_base   # Clase base para los modelos
from sqlalchemy.orm import sessionmaker              # Creador de sesiones con la BD
from core.config import settings

# Cadena de conexión a PostgreSQL

# Creamos el motor de conexión
engine = create_engine(settings.DATABASE_URL)

# Fábrica de sesiones
# Cada petición abrirá una sesión independiente
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base de la que heredarán todos los modelos
Base = declarative_base()