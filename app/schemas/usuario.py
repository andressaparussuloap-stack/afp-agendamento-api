from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: Optional[int] = None
    tipo: str = "empresa"



class UsuarioResponse(BaseModel):

    id: int
    nome: str
    email: EmailStr
    empresa_id: Optional[int]
    tipo: str


    class Config:
        from_attributes = True