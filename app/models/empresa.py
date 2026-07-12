from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    telefone = Column(String(20))
    email = Column(String(150))

