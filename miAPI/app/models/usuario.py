from pydantic import BaseModel, Field

class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="identificador unico del usuario", example="1")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario")
    edad: int = Field(..., gt=0, description="Edad del usuario", example="30", le=121)