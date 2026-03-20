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
    title='mi primer API',
    description='Manuel David Tovar Rodriguez', 
    version='1.0'
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)
#1 Cambiar la lista de datos (usuarios → autos)
autos = [
    {"id": 1, "marca": "Toyota", "modelo": "Camry", "año": 2020},
    {"id": 2, "marca": "Honda", "modelo": "Civic", "año": 2019},
    {"id": 3, "marca": "Ford", "modelo": "Mustang", "año": 2021},
]
#2 Cambiar la clase Pydantic (UsuarioBase → AutoBase)
# Modelo de validacion pydantic
class AutoBase(BaseModel):
    id: int = Field(..., gt=0, description="ID del auto")
    marca: str = Field(..., min_length=2, max_length=50, description="Marca del auto")
    modelo: str = Field(..., min_length=1, max_length=50, description="Modelo del auto")
    anio: int = Field(..., gt=1900, le=2026, description="Año del auto")

# -----Seguridad HTTP Basic------
security = HTTPBasic()    

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth= secrets.compare_digest(credentials.username,"admin")    
    ContraAuth= secrets.compare_digest(credentials.password,"123456789") 
    
    if not (usuarioAuth and ContraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="credenciales incorrectas",
        )
    return credentials.username
    
    
# --- Endpoints ---

@app.get("/")
async def holamundo():
    return {"mensaje": "Holamundo FastAPI"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje": "Tu calificacion en TAI es 10"}

@app.get("/v1/ParametroO/{id}", tags=['Parametro obligatorio'])
async def cunsultaAutosO(id: int):
    await asyncio.sleep(3)
    return {"Bienvenidos a tu api REST": id}

@app.get("/v1/ParametroOp/", tags=['Parametro opcionales'])
async def cunsultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    
    if id is not None:
        for auto in autos:
            if auto["id"] == id:
                return {"auto encontrado con el id": id, "auto": auto}
        
        
        return {"Mensaje": "auto no encontrado"} 
    
    else:
        return {"Aviso": "no se proporciono id"}
    
#3 Cambiar nombres de endpoints Solo cambias usuarios → autos


@app.get("/v1/autos/", tags=['CRUD autos'])
async def consultaAutos():
    return{
        "status":"200",
        "total": len(autos),
        "data":autos
    }
    
@app.post("/v1/autos/", tags=['CRUD autos'])
async def agregar_autos(auto:AutoBase):
    for a in autos:
        if a ["id"] == auto.id:
           raise HTTPException(
               status_code=400,
               detail="el id ya existe"
           )
    autos.append(auto)
    return{
        "mensaje":"Auto agregado",
        "datos":auto,
        "status":"200"
    }
    
#tarea hacer put y delete

@app.put("/v1/autos/{id}", tags=['CRUD autos'])
async def actualizar_auto(id: int, auto_actualizado: dict):
    # 1. Buscamos el auto por ID
    for index, auto in enumerate(autos):
        if auto["id"] == id:
            # 2. Actualizamos los valores
            autos[index] = {
                "id": id,
                "marca": auto_actualizado.get("marca", auto["marca"]),
                "modelo": auto_actualizado.get("modelo", auto["modelo"]),
                "anio": auto_actualizado.get("anio", auto["anio"])
            }
            
            # 3. Retornamos inmediatamente si lo encontramos
            return {
                "mensaje": "Auto actualizado correctamente",
                "datos": autos[index],
                "status": "200"
            }
    
    # 4. Si el ciclo termina y no se encontró el ID, lanzamos el error
    raise HTTPException(
        status_code=404,
        detail="Auto no encontrado"
    )
#enpoint para delete
@app.delete("/v1/autos/{id}", tags=['CRUD autos'])
async def eliminar_auto(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    
    for index, auto in enumerate(autos):
        if auto["id"] == id:
            auto_eliminado = autos.pop(index)
            
        
            return {"message": f"Auto eliminadoo por {usuarioAuth}"}
        
            return {
                "mensaje": "Auto eliminado correctamente",
                "auto_eliminado": auto_eliminado,
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail="Auto no encontrado"
    )
    #Resumen rápido para tu examen

#Si te dicen:

#"Haz un CRUD de autos"

#Solo cambias:

#1️ Lista
#usuarios → autos
#2️ Modelo
#UsuarioBase → AutoBase
#3️ Campos
#nombre → marca
#edad → anio
#+ modelo
#4️ endpoints
#/usuarios → /autos
#construir contenedores docker-compose build
#levantar contenedores docker-compose up
#borrar contenedores docker-compose down
#verificar contenedores docker ps
#docker build -t imagen-autos .
#asignamos el nombre docker run -d --name autos -p 7000:7000 imagen-autos
# para ver los errores docker logs autos
# deten y borramos el contenedor actual docker stop autos
#docker rm autos