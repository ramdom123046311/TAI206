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
    title='Cine API',
    description='Cartelera Digital - Manuel David Tovar Rodriguez', 
    version='1.0'
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

# 1. Lista de datos (Peliculas)
peliculas = [
    {"id": 1, "titulo": "Matrix", "genero": "Sci-Fi", "anio": 1999},
    {"id": 2, "titulo": "Inception", "genero": "Sci-Fi", "anio": 2010},
    {"id": 3, "titulo": "The Dark Knight", "genero": "Accion", "anio": 2008},
]

# 2. Modelo de validacion Pydantic
class PeliculaBase(BaseModel):
    id: int = Field(..., gt=0)
    titulo: str = Field(..., min_length=1, max_length=100)
    genero: str = Field(..., min_length=3, max_length=30)
    anio: int = Field(..., gt=1880, le=2026)

# -----Seguridad HTTP Basic------
security = HTTPBasic()    

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "admin")    
    ContraAuth = secrets.compare_digest(credentials.password, "123456789") 
    
    if not (usuarioAuth and ContraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de taquilla incorrectas",
        )
    return credentials.username

# --- Endpoints Base ---

@app.get("/")
async def home():
    return {"mensaje": "Bienvenido a CineAPI"}

@app.get("/v1/demo", tags=['Pruebas'])
async def asincronia_peli():
    await asyncio.sleep(5)
    return {"mensaje": "Carga de trailers finalizada"}

# --- Parametros ---

@app.get("/v1/pelicula/{id}", tags=['Busqueda'])
async def peli_id(id: int):
    await asyncio.sleep(2)
    for p in peliculas:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")

@app.get("/v1/filtro/", tags=['Busqueda'])
async def filtro_peli(id: Optional[int] = None):
    if id:
        for p in peliculas:
            if p["id"] == id:
                return p
        return {"msj": "No existe"}
    return {"catalogo": peliculas}

# --- CRUD Peliculas ---

@app.get("/v1/peliculas/", tags=['Cartelera'])
async def listar_cartelera():
    return {"count": len(peliculas), "peliculas": peliculas}

@app.post("/v1/peliculas/", tags=['Cartelera'])
async def nueva_peli(peli: PeliculaBase):
    for p in peliculas:
        if p["id"] == peli.id:
            raise HTTPException(status_code=400, detail="ID ocupado")
    peliculas.append(peli.dict())
    return {"mensaje": "Pelicula agregada", "peli": peli}

@app.put("/v1/peliculas/{id}", tags=['Cartelera'])
async def update_peli(id: int, info: PeliculaBase):
    for i, p in enumerate(peliculas):
        if p["id"] == id:
            peliculas[i] = info.dict()
            return {"msj": "Informacion actualizada"}
    raise HTTPException(status_code=404, detail="ID inexistente")

@app.delete("/v1/peliculas/{id}", tags=['Cartelera'])
async def remove_peli(id: int, user: str = Depends(verificar_peticion)):
    for i, p in enumerate(peliculas):
        if p["id"] == id:
            item = peliculas.pop(i)
            return {"user": user, "status": "Eliminado", "peli": item}
    raise HTTPException(status_code=404, detail="No se encontro la pelicula")

# --- Dockerfile Sugerido ---
# FROM python:3.12-slim
# WORKDIR /app
# COPY requeriments.txt .
# RUN pip install -r requeriments.txt
# COPY ./app ./app
# EXPOSE 5000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]