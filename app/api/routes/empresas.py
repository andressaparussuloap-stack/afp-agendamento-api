from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaResponse


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


@router.post("/", response_model=EmpresaResponse)
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):

    nova_empresa = Empresa(
        nome=empresa.nome,
        telefone=empresa.telefone,
        email=empresa.email
    )

    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)

    return nova_empresa


@router.get("/", response_model=list[EmpresaResponse])
def listar_empresas(
    db: Session = Depends(get_db)
):

    return db.query(Empresa).all()


@router.get("/{empresa_id}", response_model=EmpresaResponse)
def buscar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    return empresa


@router.put("/{empresa_id}", response_model=EmpresaResponse)
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaCreate,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    empresa.nome = dados.nome
    empresa.telefone = dados.telefone
    empresa.email = dados.email

    db.commit()
    db.refresh(empresa)

    return empresa


@router.delete("/{empresa_id}")
def excluir_empresa(
    empresa_id: int,
    db: Session = Depends(get_db)
):

    empresa = db.query(Empresa).filter(
        Empresa.id == empresa_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )

    db.delete(empresa)
    db.commit()

    return {
        "mensagem": "Empresa excluída com sucesso"
    }

