from pydantic import BaseModel, EmailStr


class CadastroRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    empresa_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

