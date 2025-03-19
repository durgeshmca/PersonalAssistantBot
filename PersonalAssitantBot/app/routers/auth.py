from fastapi import APIRouter
from app.lib.db import SessionDep
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.models.tokens import Token
from fastapi import HTTPException , status
from datetime import timedelta
from app.config import Config

from app.auth import (
    authenticate_user,
    create_access_token,
)

auth_router = APIRouter()
@auth_router.post("/auth/token",tags=['Authentication'])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session : SessionDep
) -> Token:
    user = authenticate_user(session,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

