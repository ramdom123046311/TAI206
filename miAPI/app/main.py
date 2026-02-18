# importaciones
from fastapi import FastAPI,status,HTTPException
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field

# Inicializacion del servidor
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

usuarios = [
    {"id": 1, "nombre": "Manuel Tovar", "edad": 38},
    {"id": 2, "nombre": "Andres Martinez", "edad": 20},
    {"id": 3, "nombre": "Diego Rubio", "edad": 21},
]

# Modelo de validacion pydantic
class UsuarioBase(BaseModel):
    id:int = Field(...,gt=0, description="identificador unico del usuario", example="1")
    nombre:str = Field(...,min_length=3, max_length=50, description="Nomre de usuario")
    edad:int = Field(...,gt=0, description="Edad del usuario", example="30", le=121)
    
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
async def cunsultaUsuariosO(id: int):
    await asyncio.sleep(3)
    return {"Bienvenidos a tu api REST": id}

@app.get("/v1/ParametroOp/", tags=['Parametro opcionales'])
async def cunsultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"usuario encontrado con el id": id, "usuario": usuario}
        
        
        return {"Mensaje": "usuario no encontrado"} 
    
    else:
        return {"Aviso": "no se proporciono id"}
    
@app.get("/v1/usuarios/", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }
    
@app.post("/v1/usuarios/", tags=['CRUD usuarios'])
async def agregar_usuarios(usuario:UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
           raise HTTPException(
               status_code=400,
               detail="el id ya existe"
           )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado",
        "datos":usuario,
        "status":"200"
    }
#tarea hacer put y delete

#endpoint para put
@app.put("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            
            usuarios[index] = {
                "id": id,
                "nombre": usuario_actualizado.get("nombre", usuario["nombre"]),
                "edad": usuario_actualizado.get("edad", usuario["edad"])
            }
            
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usuarios[index],
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
    
#enpoint para delete
@app.delete("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def eliminar_usuario(id: int):
    
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            
            return {
                "mensaje": "Usuario eliminado correctamente",
                "usuario_eliminado": usuario_eliminado,
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )