from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database.database import Base


class Servico(Base):
    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(
        String(150),
        nullable=False
    )

    descricao = Column(
        String(255)
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

