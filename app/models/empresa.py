from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Empresa(Base):

    __tablename__ = "empresas"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    nome = Column(
        String(150),
        nullable=False
    )


    cnpj = Column(
        String(20),
        unique=True,
        nullable=True
    )


    telefone = Column(
        String(20),
        nullable=True
    )


    email = Column(
        String(150),
        nullable=True
    )


    usuarios = relationship(
        "Usuario",
        back_populates="empresa"
    )


    clientes = relationship(
        "Cliente",
        back_populates="empresa"
    )


    servicos = relationship(
        "Servico",
        back_populates="empresa"
    )


    agendamentos = relationship(
        "Agendamento",
        back_populates="empresa"
    )