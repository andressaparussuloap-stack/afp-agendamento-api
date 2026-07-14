from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"


    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)

    # senha criptografada (hash)
    senha_hash = Column(String(255), nullable=False)

    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    empresa = relationship("Empresa", back_populates="usuarios")


