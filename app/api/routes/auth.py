from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.auth import CadastroRequest, LoginRequest, TokenResponse
from app.schemas.usuario import UsuarioResponse
from app.services.security import create_access_token, hash_password, verify_password
from jose import jwt

from app.api.core.deps import get_current_user

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/cadastro", response_model=UsuarioResponse)
def cadastro(
    dados: CadastroRequest,
    db: Session = Depends(get_db),
):
    existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_password(dados.senha),
        empresa_id=dados.empresa_id,
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


@router.post("/login", response_model=TokenResponse)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not user or not verify_password(dados.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.post("/token", response_model=TokenResponse)
def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer"
    }
