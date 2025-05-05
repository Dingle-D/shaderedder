
from app.models import UserRegister, Token, Message
from app.db.users.utils import schedule_user, confirm_user, add_user, del_user, get_user_by_username, get_user_by_email
from app.security.access_token import create_access_token, decode_access_token
from app.core.config import settings
from app.email.utils import send_email, generate_account_activation_email

from fastapi import APIRouter, Depends, status, HTTPException

from datetime import timedelta

from jwt import InvalidTokenError 
from pydantic import ValidationError
from uuid import uuid4, UUID

router = APIRouter(prefix="/register", tags=["register"])

@router.post("/")
async def register_account(user: UserRegister):
    if settings.emails_enabled:
        has_username = await get_user_by_username(user.username)
        has_email = await get_user_by_email(user.email)
        if has_username or has_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with that username or email already exists")

        token = str(uuid4())
        try:
            await schedule_user(user, token)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with that username or email already exists")

        page = generate_account_activation_email(user.email, user.username, token)
        try:
            response = send_email(email_to=user.email, subject=page.subject, html_content=page.html_content)
        except ValidationError as e:
            await del_user(user.username)
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="could not send validation email")
        return Message(success=True)
    else:
        try:
            await add_user(user)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with that username or email already exists")
        return Message(success=True)


@router.post("/confirm")
async def activate_account(token: str):
    try:
        await confirm_user(token)
        return Message(success=True, comment="activated")
    except (ValueError) as e:
        return Message(success=False, comment=str(e))

