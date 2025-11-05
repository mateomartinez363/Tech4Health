from pydantic import BaseModel, Field
from typing import Optional

class CrearPaciente(BaseModel):
    nombre: str = Field(..., max_length=100, min_length=1)
    edad: int = Field(..., ge=0, le=120)
    historia_clinica: Optional[str] = Field(None, max_length=1000)

class LeerPaciente(CrearPaciente):
    id: int
    nombre: str
    edad: int
    historia_clinica: Optional[str]
    class Config:
        from_attributes = True