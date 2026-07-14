from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: int


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    empresa_id: int

    class Config:
        from_attributes = True

