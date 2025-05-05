
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

import jwt
from jwt.exceptions import InvalidTokenError

from app.security.access_token import create_access_token
from app.core.config import settings
from app.db.users.utils import authenticate
from app.models import UserView, UserLogin, Token

from app.api.utils import CurrentUser

from typing import Annotated

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate(UserLogin(username=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password")
    elif not user.is_activated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token = create_access_token(user.username, expires_delta=access_token_expires)
    )

@router.post("/test-token", response_model=UserView)
async def login_test_token(current_user: CurrentUser):
    return current_user
