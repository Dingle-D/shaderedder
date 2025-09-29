
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from starlette.requests import Request

from datetime import timedelta, datetime

import jwt
from jwt.exceptions import InvalidTokenError

from app.security.access_token import create_access_token
from app.core.config import settings
from app.db.services.users import authenticate, get_user_by_email, add_user_oauth
from app.db.services.sessions import add_session
from app.models import UserView, UserLogin, Token, UserOauth, SessionBase

from app.api.utils import CurrentUser
import app.security.oauth as oauth

from typing import Annotated

router = APIRouter(prefix="/login", tags=["login"])

@router.post("")
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate(UserLogin(username=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password")
    elif not user.is_activated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token = create_access_token(user.username, expires_delta=access_token_expires)
    )
    await add_session(SessionBase(token=token.access_token, creation_date=datetime.utcnow(), user_id=user.id))
    
    return token

@router.get("/google-login")
async def google_login(request: Request):
    return await oauth.login(request)

# имя функции должно быть именно google_auth для коректной работы starlette
@router.get("/google-auth")
async def google_auth(request: Request):
    userinfo = await oauth.auth(request)
    user = await get_user_by_email(userinfo["user"]["email"])
    if not user:
        add_user_oauth(UserOauth(username=userinfo["user"]["name"], email=userinfo["user"]["email"]))
    access_token_expires = timedelta(seconds=userinfo["token"]["expires_in"])
    token = Token(
        access_token = create_access_token(userinfo["user"]["name"], expires_delta=access_token_expires)
    )
    await add_session(SessionBase(token=token.access_token, creation_date=datetime.utcnow(), user_id=user.id))
    return token

@router.get("/google-login-rd")
async def google_login_rd(request: Request):
    return await oauth.login(request, "google_auth_rd")

# то же что и предыдущая но использует редирект для фронтенда
@router.get("/google-auth-rd")
async def google_auth_rd(request: Request):
    userinfo = await oauth.auth(request)
    user = await get_user_by_email(userinfo["user"]["email"])
    if not user:
        await add_user_oauth(UserOauth(username=userinfo["user"]["name"], email=userinfo["user"]["email"]))
    access_token_expires = timedelta(seconds=userinfo["token"]["expires_in"])
    token = Token(
        access_token = create_access_token(userinfo["user"]["name"], expires_delta=access_token_expires)
    )
    await add_session(SessionBase(token=token.access_token, creation_date=datetime.utcnow(), user_id=user.id))
    redirect = RedirectResponse(url=f"{settings.FRONTEND_HOST}/auth-callback")
    #redirect.headers['Authorization'] = f"{token.token_type} {token.access_token}"
    redirect.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=False,
    )
    redirect.set_cookie(
        key="token_type",
        value="Bearer",
        httponly=False,
    )
    
    return redirect

@router.post("/test-token", response_model=UserView)
async def login_test_token(current_user: CurrentUser):
    view = UserView(
        id=current_user.id,
        role=current_user.role,
        is_activated=current_user.is_activated,
        should_reset_password=current_user.should_reset_password,
        email=current_user.email,
        username=current_user.username
    )
    return view
