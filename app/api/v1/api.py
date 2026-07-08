# Este fichero es el encargado de agrupar todas las rutas de la API. En lugar de definir todos los endpoints en main.py, 
# FastAPI permite dividirlos en distintos archivos mediante APIRouter para mantener el proyecto más organizado.

# ======================================================
# ENRUTADOR PRINCIPAL DE LA API
# ======================================================

from fastapi import APIRouter
from api.v1 import auth, productos, categorias, carrito, pedido

# Creamos el router principal. Este router agrupará todos los routers de la aplicación.
api_router = APIRouter()

# ======================================================
# RUTAS DE AUTENTICACIÓN, PRODUCTOS Y CATEGORIAS 
# ======================================================

api_router.include_router(auth.api_router, prefix="/auth", tags=["auth"])
api_router.include_router(productos.api_router, prefix="/producto", tags=["productos"])
api_router.include_router(categorias.api_router, prefix="/categorias", tags=["categorias"])
api_router.include_router(carrito.api_router, prefix="/carrito", tags=["carrito"])
api_router.include_router(pedido.api_router, prefix="/pedido", tags=["pedido"])