from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.schemas.empresa import EmpresaCreate, EmpresaResponse
from app.api.core.deps import get_admin_user, get_empresa_user


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"],
)


def _checar_acesso(empresa: Empresa, current_user: Usuario):
    """Admin acessa qualquer empresa; usuário 'empresa' só a própria."""
    if current_user.tipo != "admin" and empresa.id != current_user.empresa_id:
        raise HTTPException(
            status_code=403,
            detail="Você não tem acesso a esta empresa",
        )


@router.post("/", response_model=EmpresaResponse)
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    # Só admin cadastra empresas novas no sistema
    current_user: Usuario = Depends(get_admin_user),
):
    nova_empresa = Empresa(
        nome=empresa.nome,
        telefone=empresa.telefone,
        email=empresa.email,
    )

    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return nova_empresa


@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    query = db.query(Empresa)

    if current_user.tipo != "admin":
        query = query.filter(Empresa.id == current_user.empresa_id)

    return query.all()


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    _checar_acesso(empresa, current_user)

    return empresa


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_empresa_user),
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    _checar_acesso(empresa, current_user)

    empresa.nome = dados.nome
    empresa.telefone = dados.telefone
    empresa.email = dados.email

    db.commit()
    db.refresh(empresa)

    return empresa


@router.delete("/{empresa_id}")
def excluir_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    # Só admin exclui empresas
    current_user: Usuario = Depends(get_admin_user),
):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada",
        )

    db.delete(empresa)
    db.commit()

    return {"mensagem": "Empresa excluída com sucesso"}
