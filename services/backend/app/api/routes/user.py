from fastapi import APIRouter, Depends, HTTPException

from app.api.routes.login import CurrentUser
from app.models import UserView, Message

from app.db.services.users import change_users_username, get_user_by_username

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserView)
def read_users_me(current_user: CurrentUser):
    return current_user

@router.post("/change_username", response_model=Message)
def change_username(current_user: CurrentUser, username: str):
    # TODO: добавить валидацию
    await change_user_username(current_user.id, username)

