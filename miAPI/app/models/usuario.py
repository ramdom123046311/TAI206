from pydantic import BaseModel, Field

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    edad: int = Field(..., gt=0, description="Edad del usuario", example="30", le=121)