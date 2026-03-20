from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import usuarios, misc

# Inicialización del servidor
app = FastAPI(
    title='mi primer API',
    description='Manuel David Tovar Rodriguez',
    version='1.0'
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5001"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

# Incluir los routers
app.include_router(misc.router)        # Endpoints varios 
app.include_router(usuarios.router)    # Endpoints CRUD de usuarios
