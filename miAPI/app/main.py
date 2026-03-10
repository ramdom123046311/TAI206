from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from datetime import date

# Inicializacion del servidor
app = FastAPI(
    title='API de Citas Médicas',
    description='Manuel David Tovar Rodriguez - CRUD Protegido', 
    version='1.1'
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5001"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

# Base de datos ficticia
Citas = [
    {"id": 1, "nombre": "Manuel Tovar", "dia": 10, "mes": 3, "anio": 2026, "motivo": "dolor abdominal", "confirmacion": True},
    {"id": 2, "nombre": "Andres Martinez", "dia": 14, "mes": 4, "anio": 2026, "motivo": "dolor de cabeza", "confirmacion": True},
    {"id": 3, "nombre": "Diego Rubio", "dia": 17, "mes": 6, "anio": 2026, "motivo": "dolor de estomago", "confirmacion": True},
]

# Modelo de validacion pydantic
class CitaBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único")
    nombre: str = Field(..., min_length=3, max_length=50)
    dia: int = Field(..., ge=1, le=31)
    mes: int = Field(..., ge=1, le=12)
    anio: int = Field(..., ge=2024)
    motivo: str = Field(..., min_length=3, max_length=100)
    confirmacion: bool

    # Validación personalizada para la fecha
    @validator('dia')
    @classmethod  # Esto elimina el error de 'cls' y la línea roja
    def validar_fecha_futura(cls, v, values):
        # Verificamos que 'anio' y 'mes' ya existan en el diccionario de valores
        if 'anio' in values and 'mes' in values:
            try:
                # Importante: date debe estar importado (from datetime import date)
                fecha_cita = date(values['anio'], values['mes'], v)
                if fecha_cita < date.today():
                    raise ValueError('La fecha no puede ser anterior a la actual')
            except ValueError as e:
                # Esto captura fechas imposibles como 31 de febrero
                raise ValueError(f'Fecha inválida o pasada: {e}')
        return v

# ----- Seguridad HTTP Basic ------
security = HTTPBasic()    

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_valido = secrets.compare_digest(credentials.username, "root")    
    contra_valida = secrets.compare_digest(credentials.password, "1234") 
    
    if not (usuario_valido and contra_valida):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- Endpoints Públicos ---

@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Holamundo FastAPI"}

# --- Endpoints Protegidos (CRUD) ---

@app.get("/v1/citas/", tags=['CRUD citas'])
async def consultaCitas(usuario: str = Depends(verificar_peticion)):
    return {
        "total": len(Citas),
        "data": Citas
    }

@app.get("/v1/citas/{id}", tags=['CRUD citas'])
async def consultarCitaPorId(id: int, usuario: str = Depends(verificar_peticion)):
    for cita in Citas:
        if cita["id"] == id:
            return {"cita": cita}
    raise HTTPException(status_code=404, detail="Cita no encontrada")

@app.post("/v1/citas/", tags=['CRUD citas'], status_code=status.HTTP_201_CREATED)
async def agregar_citas(cita: CitaBase, usuario: str = Depends(verificar_peticion)):
    # Verificar si el ID ya existe
    if any(c['id'] == cita.id for c in Citas):
        raise HTTPException(status_code=400, detail="El ID ya existe")
    
    nueva_cita = cita.dict()
    Citas.append(nueva_cita)
    return {
        "mensaje": "Cita agendada correctamente",
        "datos": nueva_cita
    }

@app.put("/v1/citas/{id}", tags=['CRUD citas'])
async def actualizar_cita(id: int, cita_actualizada: CitaBase, usuario: str = Depends(verificar_peticion)):
    for index, cita in enumerate(Citas):
        if cita["id"] == id:
            # Reemplazamos con los nuevos datos validados
            Citas[index] = cita_actualizada.dict()
            return {
                "mensaje": "Cita actualizada correctamente",
                "datos": Citas[index]
            }
    
    raise HTTPException(status_code=404, detail="Cita no encontrada")

@app.delete("/v1/citas/{id}", tags=['CRUD citas'])
async def eliminar_cita(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    for index, cita in enumerate(Citas):
        if cita["id"] == id:
            cita_eliminada = Citas.pop(index)
            return {
                "mensaje": f"Cita eliminada correctamente por {usuarioAuth}",
                "datos_eliminados": cita_eliminada
            }
    
    raise HTTPException(status_code=404, detail="Cita no encontrada")

# --- Otros Endpoints ---

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(1) # Reducido para pruebas rápidas
    return {"mensaje": "Tu calificacion en TAI es 10"}