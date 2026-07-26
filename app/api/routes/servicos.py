from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.servico import Servico
from app.models.usuario import Usuario

from app.schemas.servico import (
    ServicoCreate,
    ServicoResponse
)

from app.api.core.deps import get_empresa_user


router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"]
)


def _query_base(db: Session, current_user: Usuario):
    """
    Admin enxerga todos os serviços.
    Usuário do tipo 'empresa' só enxerga os da própria empresa.
    """
    query = db.query(Servico)

    if current_user.tipo != "admin":
        query = query.filter(Servico.empresa_id == current_user.empresa_id)

    return query


@router.post("/", response_model=ServicoResponse)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    # Admin pode cadastrar serviço pra qualquer empresa (se o schema
    # tiver empresa_id opcional); empresa só cadastra pra si mesma.
    empresa_id = (
        getattr(servico, "empresa_id", None)
        if current_user.tipo == "admin" and getattr(servico, "empresa_id", None)
        else current_user.empresa_id
    )

    if empresa_id is None:
        raise HTTPException(
            status_code=400,
            detail="Nenhuma empresa vinculada para este serviço."
        )

    novo_servico = Servico(
        nome=servico.nome,
        descricao=servico.descricao,
        valor=servico.valor,
        duracao=servico.duracao,
        empresa_id=empresa_id,
    )

    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico


@router.get("/", response_model=list[ServicoResponse])
def listar_servicos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    return _query_base(db, current_user).all()


@router.delete("/{servico_id}")
def excluir_servico(
    servico_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    servico = _query_base(db, current_user).filter(
        Servico.id == servico_id
    ).first()

    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado"
        )

    db.delete(servico)
    db.commit()

    return {
        "message": "Serviço excluído com sucesso"
    }
