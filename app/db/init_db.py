# Este archivo crea todas las tablas definidas en models.py

from database import engine, Base
from models import *

# Recorre todos los modelos que heredan de Base
# y crea las tablas correspondientes en la base de datos.
Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente")