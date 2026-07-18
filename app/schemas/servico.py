from pydantic import BaseModel


class ServicoCreate(BaseModel):
    nome: str
    descricao: str | None = None
    valor: float
  


class ServicoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None = None
    valor: float
    empresa_id: int

    class Config:
        from_attributes = True

