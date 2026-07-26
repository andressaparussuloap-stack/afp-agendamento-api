from pydantic import BaseModel, EmailStr
from typing import Optional


class CadastroRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: Optional[int] = None
    tipo: str = "empresa"



class LoginRequest(BaseModel):
    email: EmailStr
    senha: str



class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nome: str
    tipo: str