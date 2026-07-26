from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.database.database import get_db

from app.models.usuario import Usuario
from app.models.empresa import Empresa

from app.schemas.auth import (
    CadastroRequest,
    LoginRequest,
    TokenResponse
)

from app.schemas.usuario import UsuarioResponse

from app.services.security import (
    create_access_token,
    hash_password,
    verify_password
)

from app.api.core.deps import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)



# ============================
# CADASTRO
# ============================

@router.post("/cadastro", response_model=UsuarioResponse)
def cadastro(
    dados: CadastroRequest,
    db: Session = Depends(get_db),
):

    existente = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()


    if existente:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )


    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_password(dados.senha),
        empresa_id=dados.empresa_id,
        tipo=dados.tipo
    )


    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)


    return novo_usuario




    # cria usuário ligado à empresa

    novo_usuario = Usuario(

        nome=dados.nome,

        email=dados.email,

        senha_hash=hash_password(
            dados.senha
        ),

        empresa_id=nova_empresa.id

    )


    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)


    return novo_usuario





# ============================
# LOGIN REACT
# ============================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):


    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()



    if not usuario:

        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )



    senha_ok = verify_password(
        dados.senha,
        usuario.senha_hash
    )



    if not senha_ok:

        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos"
        )



    token = create_access_token(
        str(usuario.id)
    )



    return {

        "access_token": token,

        "token_type": "bearer"

    }





# ============================
# USUARIO LOGADO
# ============================

@router.get(
    "/me",
    response_model=UsuarioResponse
)
def me(
    current_user: Usuario = Depends(get_current_user)
):

    return current_user





# ============================
# LOGIN SWAGGER OAUTH2
# ============================

@router.post(
    "/token",
    response_model=TokenResponse
)
def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):


    usuario = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()



    if not usuario or not verify_password(
        form_data.password,
        usuario.senha_hash
    ):

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Email ou senha inválidos",

            headers={
                "WWW-Authenticate": "Bearer"
            }

        )



    token = create_access_token(
        str(usuario.id)
    )



    return {

        "access_token": token,

        "token_type": "bearer"

    }