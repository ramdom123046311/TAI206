from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.data.database import usuarios
from app.models.usuario import UsuarioBase
from app.security.auth import verificar_peticion
from app.data import database
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as UsuarioDB

router = APIRouter(prefix="/v1/usuarios", tags=['CRUD usuarios'])

@router.get("/")
async def consultaUsuarios( db: Session = Depends(get_db)):
    
    consultaUsuariosusuarios= db.query(UsuarioDB).all()
    
    return {
        "status": "200",
        "total": len(consultaUsuariosusuarios),
        "data": consultaUsuariosusuarios
    }

@router.get("/{id}")
async def Consultausuario(id: int, db: Session = Depends(get_db)):
    
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    return {
        "status": "200",
        "data": usuario
    }

@router.post("/")
async def agregar_usuarios(usuario: UsuarioBase, db: Session = Depends(get_db)):
    
    nuevo_usuario= UsuarioDB(nombre=usuario.nombre, edad=usuario.edad)
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {
        "mensaje": "Usuario agregado",
        "datos": usuario,
        "status": "200"
    }

@router.put("/{id}")
async def actualizar_usuario(id: int, usuario_actualizado: UsuarioBase, db: Session = Depends(get_db)):
    
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # actualizar campos
    usuario.nombre = usuario_actualizado.nombre
    usuario.edad = usuario_actualizado.edad
    
    db.commit()
    db.refresh(usuario)
    
    return {
        "mensaje": "Usuario actualizado correctamente",
        "data": usuario,
        "status": "200"
    }

@router.delete("/{id}")
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion), db: Session = Depends(get_db)):
    
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    
    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}",
        "data": {"id": id},
        "status": "200"
    }