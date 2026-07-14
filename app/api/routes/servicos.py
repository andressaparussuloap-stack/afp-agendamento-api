from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.servico import Servico
from app.schemas.servico import ServicoCreate, ServicoResponse
from app.api.core.deps import get_current_user



router = APIRouter(
    prefix="/servicos",
    tags=["Serviços"]
)


@router.post("/", response_model=ServicoResponse)
def criar_servico(
    servico: ServicoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    novo_servico = Servico(
        nome=servico.nome,
        descricao=servico.descricao,
        valor=servico.valor,
        empresa_id=current_user.empresa_id
    )


    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico


@router.get("/", response_model=list[ServicoResponse])
def listar_servicos(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return db.query(Servico).filter(
        Servico.empresa_id == current_user.empresa_id
    ).all()


