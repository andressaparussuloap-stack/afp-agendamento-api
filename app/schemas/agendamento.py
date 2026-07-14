from datetime import date, time

from pydantic import BaseModel


class AgendamentoCreate(BaseModel):
    empresa_id: int
    cliente_id: int
    servico_id: int
    data: date
    horario: time
    observacao: str | None = None


class AgendamentoResponse(AgendamentoCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
