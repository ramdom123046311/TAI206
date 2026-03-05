from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
import asyncio

# --- CONFIGURACIONES DE SEGURIDAD (Reporte a) ---
SECRET_KEY = "mi_llave_secreta_super_segura_2026" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Definición del esquema OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title='mi API con Seguridad JWT',
    description='Investigación Teórica: OAuth2 + JWT', 
    version='2.0'
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5001"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Base de datos simulada
usuarios = [
    {"id": 1, "nombre": "Manuel Tovar", "edad": 38},
    {"id": 2, "nombre": "Andres Martinez", "edad": 20},
    {"id": 3, "nombre": "Diego Rubio", "edad": 21},
]

class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="Id único")
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., gt=0, le=121)

# --- LÓGICA DE TOKENS (Reporte b y c) ---

def create_access_token(data: dict):
    """Genera un token JWT con tiempo limitado."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # b. Límite de 30 min
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """c. Implementar validación de tokens"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido, expirado o inexistente",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# --- ENDPOINT DE AUTENTICACIÓN ---

@app.post("/token", tags=['Seguridad'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Genera el token si las credenciales son correctas."""
    if form_data.username == "admin" and form_data.password == "123456789":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuario o contraseña incorrectos"
    )

# --- ENDPOINTS PÚBLICOS ---

@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "Holamundo FastAPI con JWT"}

@app.get("/v1/usuarios/", tags=['CRUD usuarios'])
async def consultaUsuarios():
    return {"status": "200", "total": len(usuarios), "data": usuarios}

# --- ENDPOINTS PROTEGIDOS (Reporte d) ---

@app.put("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def actualizar_usuario(
    id: int, 
    usuario_act: dict, 
    user_auth: str = Depends(get_current_user) # d. Protección
):
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuarios[index]["nombre"] = usuario_act.get("nombre", usuario["nombre"])
            usuarios[index]["edad"] = usuario_act.get("edad", usuario["edad"])
            return {
                "mensaje": "Usuario actualizado",
                "modificado_por": user_auth,
                "datos": usuarios[index]
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['CRUD usuarios'])
async def eliminar_usuario(
    id: int, 
    user_auth: str = Depends(get_current_user) # d. Protección
):
    for index, usuario in enumerate(usuarios):
        if usuario["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {user_auth}",
                "datos": usuario_eliminado
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado") 
