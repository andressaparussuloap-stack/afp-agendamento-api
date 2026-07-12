from pydantic import BaseModel


class EmpresaCreate(BaseModel):
    nome: str
    telefone: str | None = None
    email: str | None = None


class EmpresaResponse(BaseModel):
    id: int
    nome: str
    telefone: str | None = None
    email: str | None = None

    class Config:
        from_attributes = True
