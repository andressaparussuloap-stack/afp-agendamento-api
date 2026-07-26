from app.models.empresa import Empresa
from app.models.cliente import Cliente
from app.models.servico import Servico

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.agendamento import Agendamento
from app.models.usuario import Usuario
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse
from app.api.core.deps import get_empresa_user


router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)


def _query_base(db: Session, current_user: Usuario):
    """
    Admin enxerga todos os agendamentos.
    Usuário do tipo 'empresa' só enxerga os da própria empresa.
    """
    query = db.query(Agendamento)

    if current_user.tipo != "admin":
        query = query.filter(Agendamento.empresa_id == current_user.empresa_id)

    return query


@router.get("/", response_model=list[AgendamentoResponse])
def listar_agendamentos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    return _query_base(db, current_user).all()


@router.get("/{id}", response_model=AgendamentoResponse)
def buscar_agendamento(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    agendamento = _query_base(db, current_user).filter(
        Agendamento.id == id
    ).first()

    if not agendamento:
        raise HTTPException(
            status_code=404,
            detail="Agendamento não encontrado."
        )

    return agendamento


@router.delete("/{id}")
def excluir_agendamento(
    id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    agendamento = _query_base(db, current_user).filter(
        Agendamento.id == id
    ).first()

    if not agendamento:
        raise HTTPException(
            status_code=404,
            detail="Agendamento não encontrado."
        )

    db.delete(agendamento)
    db.commit()

    return {
        "message": "Agendamento excluído com sucesso."
    }


@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(
    agendamento: AgendamentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    # Admin criando agendamento precisa informar empresa_id no schema
    # (ver observação abaixo sobre AgendamentoCreate)
    empresa_id = (
        agendamento.empresa_id
        if current_user.tipo == "admin" and getattr(agendamento, "empresa_id", None)
        else current_user.empresa_id
    )

    if empresa_id is None:
        raise HTTPException(
            status_code=400,
            detail="Nenhuma empresa vinculada para este agendamento."
        )

    # Verifica se o cliente pertence à empresa do agendamento
    cliente = db.query(Cliente).filter(
        Cliente.id == agendamento.cliente_id,
        Cliente.empresa_id == empresa_id,
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    # Verifica se o serviço pertence à empresa do agendamento
    servico = db.query(Servico).filter(
        Servico.id == agendamento.servico_id,
        Servico.empresa_id == empresa_id,
    ).first()

    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado."
        )

    # Verifica conflito de horário
    agendamento_existente = (
        db.query(Agendamento)
        .filter(
            Agendamento.empresa_id == empresa_id,
            Agendamento.data == agendamento.data,
            Agendamento.horario == agendamento.horario,
        )
        .first()
    )

    if agendamento_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um agendamento para este horário."
        )

    novo = Agendamento(
        empresa_id=empresa_id,
        cliente_id=agendamento.cliente_id,
        servico_id=agendamento.servico_id,
        data=agendamento.data,
        horario=agendamento.horario,
        observacao=agendamento.observacao,
        status="agendado"
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo
