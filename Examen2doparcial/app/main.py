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
    allow_origins=["http://localhost:5000", "http://localhost:5001"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

Citas = [
    {"id": 1, "nombre": "Manuel Tovar", "fecha": 10,"motivo":"dolor abdominal","confirmacion":1},
    {"id": 2, "nombre": "Andres Martinez", "fecha": 15,"motivo":"dolor de cabeza","confirmacion":1},
    {"id": 3, "nombre": "Diego Rubio", "fecha": 20,"motivo":"dolor de estomago","confirmacion":1},
]

# Modelo de validacion pydantic
class CitaBase(BaseModel):
    id:int = Field(...,gt=0, description="identificador unico del usuario", example="1")
    nombre:str = Field(...,min_length=3, max_length=50, description="Nomre de usuario")
    fecha:int = Field(...,gt=0, description="fecha de la cita", example="30", le=121)
    motivo:str = Field(...,min_length=3, max_length=100, description="motivo de la cita")
    confirmacion:bool = Field(...,gt=0, description="identificador de confirmacion", example="1")
# -----Seguridad HTTP Basic------
security = HTTPBasic()    

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth= secrets.compare_digest(credentials.username,"root")    
    ContraAuth= secrets.compare_digest(credentials.password,"1234") 
    
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
async def cunsultaUsuariosO(id: int):
    await asyncio.sleep(3)
    return {"Bienvenidos a tu api REST": id}

@app.get("/v1/ParametroOp/", tags=['Parametro opcionales'])
async def cunsultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    
    if id is not None:
        for cita in Citas:
            if cita["id"] == id:
                return {"cita encontrada con el id": id, "cita": cita}
        
        
        return {"Mensaje": "cita no encontrada"} 
    
    else:
        return {"Aviso": "no se proporciono id"}
    
@app.get("/v1/citas/", tags=['CRUD citas'])
async def consultaCitas():
    return{
        "status":"200",
        "total": len(Citas),
        "data":Citas
    }
    
@app.post("/v1/citas/", tags=['CRUD citas'])
async def agregar_citas(cita:CitaBase):
    for cit in Citas:
        if cit["id"] == cita.id:
           raise HTTPException(
               status_code=400,
               detail="el id ya existe"
           )
    Citas.append(cita)
    return{
        "mensaje":"Cita agregada",
        "datos":cita,
        "status":"200"
    }
#tarea hacer put y delete

#endpoint para put
@app.put("/v1/citas/{id}", tags=['CRUD citas'])
async def actualizar_cita(id: int, cita_actualizada: dict):
    
    for index, cita in enumerate(Citas):
        if cita["id"] == id:
            
            Citas[index] = {
                "id": id,
                "nombre": cita_actualizada.get("nombre", cita["nombre"]),
                "fecha":  cita_actualizada.get("fecha", cita["fecha"]),
                "motivo": cita_actualizada.get("motivo", cita["motivo"]),
                "confirmacion": cita_actualizada.get("confirmacion", cita["confirmacion"]),
            }
            
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": Citas[index],
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
    
#enpoint para delete
@app.delete("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            
        
            return {"message": f"Usuario eliminadoo por {usuarioAuth}"}
        
            return {
                "mensaje": "Usuario eliminado correctamente",
                "usuario_eliminado": usuario_eliminado,
                "status": "200"
            }
    
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )