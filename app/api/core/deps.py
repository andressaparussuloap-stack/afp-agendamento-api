from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from jose import jwt, JWTError

from app.database.database import get_db
from app.models.usuario import Usuario
from app.services.security import JWT_ALGORITHM, JWT_SECRET


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    usuario = db.query(Usuario).filter(
        Usuario.id == int(user_id)
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return usuario


# ============================
# Permissão somente ADMIN
# ============================
def get_admin_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:

    if current_user.tipo != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido somente para administrador"
        )

    return current_user


# ============================
# Permissão empresa OU admin
# (apenas confirma que é um dos dois papéis válidos)
# ============================
def get_empresa_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:

    if current_user.tipo not in ["admin", "empresa"]:
        raise HTTPException(
            status_code=403,
            detail="Usuário sem permissão"
        )

    return current_user  # <-- fix: faltava esse return


# ============================
# Garante que o usuário tem empresa vinculada
# (admin pode não ter empresa_id, então NÃO barra admin aqui)
# ============================
def verificar_empresa(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:

    if current_user.tipo != "admin" and current_user.empresa_id is None:
        raise HTTPException(
            status_code=403,
            detail="Usuário sem empresa vinculada"
        )

    return current_user
