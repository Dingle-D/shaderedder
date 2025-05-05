from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from typing import Annotated

from app.core.config import settings
from app.security.access_token import decode_access_token

from app.db.users.utils import get_user_by_username 
from app.db.users.schemas import UsersOrm

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
    user = await get_user_by_username(token_data['sub'])
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    if not user.is_activated:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user

CurrentUser = Annotated[UsersOrm, Depends(get_current_user)]

async def get_current_admin(token: TokenDep) -> UsersOrm:
    user = await get_current_user(token)
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user

CurrentAdmin = Annotated[UsersOrm, Depends(get_current_admin)]
