from fastapi import Depends, HTTPException
from app.api.core.deps import get_current_user


def admin_required(
    current_user=Depends(get_current_user)
):

    if current_user.tipo != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido somente administrador"
        )


    return current_user