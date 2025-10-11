from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from typing import Annotated

from app.core.config import settings
from app.security.access_token import decode_access_token

from app.db.services.users import get_user_by_username 
from app.db.services.sessions import get_session_by_token
from app.db.schemas import UsersOrm

from app.models import Role

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(token: TokenDep) -> UsersOrm:
    try:
        token_data = decode_access_token(token)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user_session = await get_session_by_token(token)
    if not user_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    user = await get_user_by_username(token_data['sub'])
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User {token_data['sub']} not found")
    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user

CurrentUser = Annotated[UsersOrm, Depends(get_current_user)]

async def get_current_active_user(token: TokenDep) -> UsersOrm:
    current_user = await get_current_user(token)
    if user.should_reset_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Have to change password")
    return user

async def get_current_admin(token: TokenDep) -> UsersOrm:
    user = await get_current_user(token)
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user

CurrentAdmin = Annotated[UsersOrm, Depends(get_current_admin)]
