# importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# Inicializacion del servidor
app = FastAPI(
    title='API de Gestión de Productos',
    description='Examen TAI - Manuel David Tovar Rodriguez', 
    version='1.0'
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

# 1. Lista de datos (Productos)
productos = [
    {"id": 1, "nombre": "Laptop Gamer", "precio": 25000.0, "stock": 10},
    {"id": 2, "nombre": "Mouse Inalambrico", "precio": 500.0, "stock": 50},
    {"id": 3, "nombre": "Monitor 4K", "precio": 8000.0, "stock": 15},
]

# 2. Modelo de validación Pydantic
class ProductoBase(BaseModel):
    id: int = Field(..., gt=0, description="ID único del producto")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del producto")
    precio: float = Field(..., gt=0, description="Precio unitario")
    stock: int = Field(..., ge=0, description="Cantidad en almacén")

# -----Seguridad HTTP Basic------
security = HTTPBasic()    

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "admin")    
    ContraAuth = secrets.compare_digest(credentials.password, "123456789") 
    
    if not (usuarioAuth and ContraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de administrador incorrectas",
        )
    return credentials.username

# --- Endpoints Base ---

@app.get("/", tags=['Inicio'])
async def holamundo():
    return {"mensaje": "API de Productos Activa"}

@app.get("/bienvenidos", tags=['Inicio'])
async def bienvenido():
    return {"mensaje": "Bienvenido al sistema de inventarios TAI"}

@app.get("/v1/estado_servidor", tags=['Asincronia'])
async def estado_red():
    # Simulación de latencia de red
    await asyncio.sleep(4)
    return {"status": "Online", "latencia": "40ms", "mensaje": "Servidor operando correctamente"}

# --- Endpoints de Parámetros ---

@app.get("/v1/producto/{id}", tags=['Consulta Individual'])
async def consulta_producto_id(id: int):
    """Consulta obligatoria por ID con delay de base de datos"""
    await asyncio.sleep(2)
    for p in productos:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Producto no localizado")

@app.get("/v1/buscar/", tags=['Busqueda Opcional'])
async def buscar_producto(id: Optional[int] = None):
    await asyncio.sleep(1)
    if id is not None:
        for p in productos:
            if p["id"] == id:
                return {"encontrado": True, "producto": p}
        return {"encontrado": False, "mensaje": "No existe el producto"}
    return {"Aviso": "Por favor proporcione un ID para la busqueda", "total": len(productos)}

# --- CRUD Productos ---

@app.get("/v1/productos/", tags=['CRUD'])
async def listar_productos():
    return {
        "status": "success",
        "total_inventario": len(productos),
        "data": productos
    }

@app.post("/v1/productos/", tags=['CRUD'], status_code=201)
async def crear_producto(item: ProductoBase):
    for p in productos:
        if p["id"] == item.id:
            raise HTTPException(status_code=400, detail="El ID del producto ya esta registrado")
    
    nuevo_producto = item.dict()
    productos.append(nuevo_producto)
    return {
        "mensaje": "Producto registrado exitosamente",
        "item": nuevo_producto
    }

@app.put("/v1/productos/{id}", tags=['CRUD'])
async def actualizar_producto(id: int, update: ProductoBase):
    for index, p in enumerate(productos):
        if p["id"] == id:
            productos[index] = update.dict()
            return {
                "mensaje": "Producto actualizado",
                "datos_nuevos": productos[index]
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado para actualizar")

@app.delete("/v1/productos/{id}", tags=['CRUD'])
async def borrar_producto(id: int, admin_user: str = Depends(verificar_peticion)):
    for index, p in enumerate(productos):
        if p["id"] == id:
            eliminado = productos.pop(index)
            return {
                "mensaje": f"Accion realizada por: {admin_user}",
                "producto_eliminado": eliminado,
                "status": "Borrado exitoso"
            }
    raise HTTPException(status_code=404, detail="ID no encontrado en la base de datos")

# --- Dockerfile Sugerido ---
# FROM python:3.12-slim
# WORKDIR /app
# COPY requeriments.txt .
# RUN pip install -r requeriments.txt
# COPY ./app ./app
# EXPOSE 8001
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]