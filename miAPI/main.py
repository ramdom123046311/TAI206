#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Inicializacion del servidor
app = FastAPI(
    title='mi primer API',
    description='Manuel David Tovar Rodriguez', 
    version='1.0'
)

usuarios=[
    {"id":1,"nombre":"Manuel Tovar","edad":38},
    {"id":2,"nombre":"Andres Martinez","edad":20},
    {"id":3,"nombre":"Diego Rubio","edad":21},
]

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":"Holamundo FastAPI"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}

@app.get("/v1/calificaciones",tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje":"Tu calificacion en TAI es 10"}
#opcinal
@app.get("/v1/usuarios_op/", tags=['Parametro opcionales'])
async def cunsultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        return {"Bienvenidos a tu api REST":id }


@app.get("/v1/usuarios/{id}", tags=['Parametro obligatorio'])
async def cunsultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"Bienvenidos a tu api REST":id }