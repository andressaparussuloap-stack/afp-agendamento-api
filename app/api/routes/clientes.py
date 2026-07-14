from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.api.core.deps import get_current_user



router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.post("/", response_model=ClienteResponse)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    novo_cliente = Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email,
        empresa_id=current_user.empresa_id
    )


    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return db.query(Cliente).filter(
        Cliente.empresa_id == current_user.empresa_id
    ).all()

