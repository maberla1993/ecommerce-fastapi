# Este archivo es el encargado de definir los esquemas (schemas) de la API utilizando Pydantic. 
# Los esquemas sirven para validar los datos que llegan a la API y para controlar qué información se devuelve al cliente.

# Importamos BaseModel de Pydantic.
# Todas las clases que hereden de BaseModel servirán para validar los datos de entrada y salida de la API.
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"