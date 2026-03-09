# importaciones
from fastapi import FastAPI,status,HTTPException,Depends
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# Inicializacion del servidor
app = FastAPI(
    title='Libreria Digital API',
    description='Gestion de Biblioteca - Manuel David Tovar Rodriguez', 
    version='1.0'
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

# 1. Lista de datos (Libros)
libros = [
    {"id": 1, "titulo": "Clean Code", "autor": "Robert Martin", "anio": 2008},
    {"id": 2, "titulo": "Python Crash Course", "autor": "Eric Matthes", "anio": 2019},
    {"id": 3, "titulo": "The Pragmatic Programmer", "autor": "Andrew Hunt", "anio": 1999},
]

# 2. Modelo de validacion Pydantic
class LibroBase(BaseModel):
    id: int = Field(..., gt=0)
    titulo: str = Field(..., min_length=1, max_length=100)
    autor: str = Field(..., min_length=2, max_length=50)
    anio: int = Field(..., gt=1450, le=2026)

# -----Seguridad HTTP Basic------
security = HTTPBasic()    

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "admin")    
    ContraAuth = secrets.compare_digest(credentials.password, "123456789") 
    
    if not (usuarioAuth and ContraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado a la biblioteca",
        )
    return credentials.username

# --- Endpoints de Prueba ---

@app.get("/")
async def index():
    return {"mensaje": "Bienvenido a la Libreria Virtual"}

@app.get("/check", tags=['Sistema'])
async def health_check():
    await asyncio.sleep(2)
    return {"status": "Libreria en linea", "registros": len(libros)}

# --- Parametros ---

@app.get("/v1/libro/{id}", tags=['Consultas'])
async def libro_por_id(id: int):
    await asyncio.sleep(1)
    for l in libros:
        if l["id"] == id:
            return l
    raise HTTPException(status_code=404, detail="El libro no existe en el catalogo")

@app.get("/v1/buscar_libro/", tags=['Consultas'])
async def buscar_opcional(id: Optional[int] = None):
    if id:
        for l in libros:
            if l["id"] == id:
                return l
        raise HTTPException(status_code=404, detail="No encontrado")
    return {"error": "Debe enviar un id", "catalogo": libros}

# --- CRUD Libros ---

@app.get("/v1/libros/", tags=['CRUD'])
async def todos_los_libros():
    return {"total": len(libros), "libros": libros}

@app.post("/v1/libros/", tags=['CRUD'])
async def nuevo_libro(libro: LibroBase):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="ID duplicado")
    libros.append(libro.dict())
    return {"status": "creado", "data": libro}

@app.put("/v1/libros/{id}", tags=['CRUD'])
async def editar_libro(id: int, data: LibroBase):
    for i, l in enumerate(libros):
        if l["id"] == id:
            libros[i] = data.dict()
            return {"mensaje": "Actualizado correctamente"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/v1/libros/{id}", tags=['CRUD'])
async def eliminar_libro(id: int, user: str = Depends(verificar_peticion)):
    for i, l in enumerate(libros):
        if l["id"] == id:
            eliminado = libros.pop(i)
            return {"autorizado_por": user, "eliminado": eliminado}
    raise HTTPException(status_code=404, detail="No se pudo eliminar: ID inexistente")

# --- Dockerfile Sugerido ---
# FROM python:3.12-slim
# WORKDIR /app
# COPY requeriments.txt .
# RUN pip install -r requeriments.txt
# COPY ./app ./app
# EXPOSE 8002
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]