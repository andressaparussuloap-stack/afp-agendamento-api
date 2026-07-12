from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    telefone = Column(String(20))
    email = Column(String(150))

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

