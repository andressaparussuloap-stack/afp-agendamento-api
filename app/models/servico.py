from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Servico(Base):

    __tablename__ = "servicos"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    nome = Column(
        String(150),
        nullable=False
    )


    descricao = Column(
        String(255),
        nullable=True
    )


    valor = Column(
        Float,
        nullable=False
    )


    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )


    empresa = relationship(
        "Empresa",
        back_populates="servicos"
    )


    agendamentos = relationship(
        "Agendamento",
        back_populates="servico"
    )