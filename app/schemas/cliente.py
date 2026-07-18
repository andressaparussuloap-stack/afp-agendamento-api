from pydantic import BaseModel

class ClienteCreate(BaseModel):
    nome: str
    telefone: str | None = None
    email: str | None = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str | None = None
    email: str | None = None
    empresa_id: int

    class Config:
        from_attributes = True
