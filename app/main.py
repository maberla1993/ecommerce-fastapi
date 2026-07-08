from fastapi import FastAPI
from api.v1.api import api_router

# Creamos la aplicación de FastAPI
app = FastAPI(
    title="E-commerce API",
    description="""
        API RESTful completa para la gestión de un E-commerce.

        Incluye:
        -Autenticación con Jwt
        -Administración de productos y categorias
        -Carrito de compras
        -Gestión de pedidos
    """,
    version="1.0.0",
    contact={
        "name": "Maberla",
        "url": "https://github.com/maberla1993/ecommerce-fastapi.git",
        "email": "maberla1993@gmail.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://mit-license.org/"
    }
)

# todas las rutas van a comenzar con este prejijo api/v1
app.include_router(api_router, prefix="/api/v1")


