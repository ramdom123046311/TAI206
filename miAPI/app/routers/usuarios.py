from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.data.database import usuarios
from app.models.usuario import UsuarioBase
from app.security.auth import verificar_peticion
from miAPI.app.data import database

router = APIRouter(prefix="/v1/usuarios", tags=['CRUD usuarios'])

@router.get("/")
async def consultaUsuarios():
    return {
        "status": "200",
        "total": len(database.usuarios),
        "data": database.usuarios
    }

@router.post("/")
async def agregar_usuarios(usuario: UsuarioBase):
    for usr in database.usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="el id ya existe"
            )
    # Convertir el modelo Pydantic a dict para mantener consistencia
    database.usuarios.append(usuario.dict())
    return {
        "mensaje": "Usuario agregado",
        "datos": usuario,
        "status": "200"
    }

@router.put("/{id}")
async def actualizar_usuario(id: int, usuario_actualizado: Dict[str, Any]):
    for index, usuario in enumerate(database.usuarios):
        if usuario["id"] == id:
            database.usuarios[index] = {
                "id": id,
                "nombre": usuario_actualizado.get("nombre", usuario["nombre"]),
                "edad": usuario_actualizado.get("edad", usuario["edad"])
            }
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": database.usuarios[index],
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@router.delete("/{id}")
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    for index, usuario in enumerate(database.usuarios):
        if usuario["id"] == id:
            usuario_eliminado = database.usuarios.pop(index)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "usuario_eliminado": usuario_eliminado,
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )