from app.models.empresa import Empresa
from app.models.cliente import Cliente
from app.models.servico import Servico

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.agendamento import Agendamento
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse
from app.api.core.deps import get_current_user


router = APIRouter(
    prefix="/agendamentos",
    tags=["Agendamentos"]
)


@router.get("/", response_model=list[AgendamentoResponse])
def listar_agendamentos(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Agendamento).filter(
        Agendamento.empresa_id == current_user.empresa_id
    ).all()



@router.get("/{id}", response_model=AgendamentoResponse)
def buscar_agendamento(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):


    agendamento = (
        db.query(Agendamento)
        .filter(
            Agendamento.id == id,
            Agendamento.empresa_id == current_user.empresa_id,
        )
        .first()
    )


    if not agendamento:
         raise HTTPException(
            status_code=404,
            detail="Agendamento não encontrado."
        )

    return agendamento


@router.post("/", response_model=AgendamentoResponse)
def criar_agendamento(
    agendamento: AgendamentoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):



    # Verifica se a empresa existe
    empresa = db.query(Empresa).filter(
        Empresa.id == agendamento.empresa_id,
        Empresa.id == current_user.empresa_id,
    ).first()


    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada."
        )

    # Verifica se o cliente existe (somente da empresa do usuário)
    cliente = db.query(Cliente).filter(
        Cliente.id == agendamento.cliente_id,
        Cliente.empresa_id == current_user.empresa_id,
    ).first()


    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    # Verifica se o serviço existe (somente da empresa do usuário)
    servico = db.query(Servico).filter(
        Servico.id == agendamento.servico_id,
        Servico.empresa_id == current_user.empresa_id,
    ).first()


    if not servico:
        raise HTTPException(
            status_code=404,
            detail="Serviço não encontrado."
        )

    # Verifica conflito de horário (somente da empresa do usuário)
    agendamento_existente = (
        db.query(Agendamento)
        .filter(
            Agendamento.empresa_id == current_user.empresa_id,
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

    # Cria o agendamento
    if agendamento.empresa_id != current_user.empresa_id:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: agendamento fora da sua empresa.",
        )

    novo = Agendamento(**agendamento.model_dump())

    db.add(novo)

    db.commit()
    db.refresh(novo)

    return novo
