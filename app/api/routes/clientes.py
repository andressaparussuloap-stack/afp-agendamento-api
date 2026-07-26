from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.api.core.deps import get_empresa_user


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


def _query_base(db: Session, current_user: Usuario):
    """
    Admin enxerga todos os clientes.
    Usuário do tipo 'empresa' só enxerga os da própria empresa.
    """
    query = db.query(Cliente)

    if current_user.tipo != "admin":
        query = query.filter(Cliente.empresa_id == current_user.empresa_id)

    return query


@router.post("/", response_model=ClienteResponse)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    # Admin pode cadastrar cliente pra qualquer empresa (se o schema
    # tiver empresa_id opcional); empresa só cadastra pra si mesma.
    empresa_id = (
        getattr(cliente, "empresa_id", None)
        if current_user.tipo == "admin" and getattr(cliente, "empresa_id", None)
        else current_user.empresa_id
    )

    if empresa_id is None:
        raise HTTPException(
            status_code=400,
            detail="Nenhuma empresa vinculada para este cliente."
        )

    novo_cliente = Cliente(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email,
        empresa_id=empresa_id,
    )

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    return _query_base(db, current_user).all()


@router.delete("/{cliente_id}")
def excluir_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    cliente = _query_base(db, current_user).filter(
        Cliente.id == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    db.delete(cliente)
    db.commit()

    return {
        "message": "Cliente excluído com sucesso"
    }
