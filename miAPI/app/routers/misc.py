from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data import database

router = APIRouter(tags=['Inicio', 'Asincronia', 'Parametros'])

@router.get("/")
async def holamundo():
    return {"mensaje": "Holamundo FastAPI"}

@router.get("/bienvenidos")
async def bienvenido():
    return {"mensaje": "Bienvenidos a tu API REST"}

@router.get("/v1/calificaciones")
async def calificaciones():
    await asyncio.sleep(6)
    return {"mensaje": "Tu calificacion en TAI es 10"}

@router.get("/v1/ParametroO/{id}")
async def consultaUsuariosO(id: int):
    await asyncio.sleep(3)
    return {"Bienvenidos a tu api REST": id}

@router.get("/v1/ParametroOp/")
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in database.usuarios:
            if usuario["id"] == id:
                return {"usuario encontrado con el id": id, "usuario": usuario}
        return {"Mensaje": "usuario no encontrado"}
    else:
        return {"Aviso": "no se proporciono id"}