from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)

    empresa_id = Column(Integer, ForeignKey("empresas.id"))

    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    servico_id = Column(Integer, ForeignKey("servicos.id"))

    data = Column(Date)

    horario = Column(Time)

    status = Column(String, default="Agendado")

    observacao = Column(String)

    empresa = relationship("Empresa", back_populates="agendamentos")

    cliente = relationship("Cliente", back_populates="agendamentos")

    servico = relationship("Servico", back_populates="agendamentos")