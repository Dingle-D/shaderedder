from fastapi import APIRouter, Depends, HTTPException, status

from app.api.routes.login import CurrentUser
from app.models import UserView, Message, SessionView

from app.db.services.users import change_user_username, get_user_by_username
from app.db.services.sessions import (
    get_sessions_by_user_id, 
    del_session_by_id,
)

router = APIRouter(prefix="/user", tags=["user"])

#@router.get("/me", response_model=UserView)
#def read_users_me(current_user: CurrentUser):
#    return current_user

@router.post("/change_username", response_model=Message)
async def change_username(current_user: CurrentUser, username: str):
    # TODO: добавить валидацию
    await change_user_username(current_user.id, username)

@router.get("/sessions", response_model=SessionView)
async def get_user_sessions(current_user: CurrentUser):
    sessions = await get_sessions_by_user_id(current_user.id)
    sviews = [SessionView(id=s.id, user_id=s.user_id, token=s.token, expiration_date=s.expiration_date) for s in sessions]
    return sviews

@router.post("/delete-session/{id}", response_model=Message)
async def del_user_session(current_user: CurrentUser, session_id: int):
    sessions = await get_sessions_by_user_id(current_user.id)
    for s in sessions:
        if s.user_id == current_user.id:
            await del_session_by_id(current_user.id)
            return Message(success=True)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
