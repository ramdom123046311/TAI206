#importaciones
from fastapi import FastAPI


#Inicializacion del servidor
app = FastAPI()

#Endpoints
@app.get("/")
async def holamundo():
    return {"mensaje":"Holamundo FastA"}

@app.get("/bienvenidos")
async def bienvenido():
    return {"mensaje":"Bienvenidos a tu API REST"}