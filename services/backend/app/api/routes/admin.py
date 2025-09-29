from app.models import (
    UserRegister, 
    PaginationOptions, 
    PaginationMeta,
    PaginationResponse,
    Role, 
    UserView, 
    UserBase,
    Message,
    SessionView
)
from app.db.services.users import (
    get_user_by_id,
    get_users, 
    add_user, 
    get_users_total, 
    deactivate_user, 
    activate_user
)
from app.db.services.sessions import get_sessions_by_user_id_remove_invalid, del_session_by_id
from app.api.utils import get_current_admin, CurrentAdmin

from fastapi import APIRouter, Depends, status, HTTPException
from app.security.access_token import is_token_valid 

from pydantic import ValidationError
from typing import List, Annotated


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/get-users", dependencies=[Depends(get_current_admin)], response_model=PaginationResponse[UserView])
async def router_get_users(pagination: PaginationOptions = Depends(PaginationOptions.as_query)):
    result = await get_users(pagination)
    #print("RESULT:", type(result[0]))
    user_views = [UserView.from_orm(u) for u in result] #UserView.from_orm(result)
    total = await get_users_total()
    return PaginationResponse[UserView](
        data=user_views,
        meta=PaginationMeta(
            offset=pagination.offset,
            limit=pagination.limit, 
            total=total
        )
    )

@router.get("/get-user/{id}", response_model=UserView)
async def router_get_user(id: int, current_admin: CurrentAdmin):
    result = await get_user_by_id(id)
    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return result


@router.post("/add-user", dependencies=[Depends(get_current_admin)])
async def router_add_user(user: UserRegister):
    try:
        await add_user(user)
        return Message(success=True)
    except Exception as e:
        return Message(success=False)

@router.post("/activate-user/{id}", dependencies=[Depends(get_current_admin)])
async def router_activate_user(id: int):
    try:
        await activate_user(id)
        return Message(success=True)
    except Exception as e:
        return Message(success=False)

@router.post("/deactivate-user/{id}", dependencies=[Depends(get_current_admin)])
async def router_deactivate_user(id: int):
    try:
        await deactivate_user(id)
        return Message(success=True)
    except Exception as e:
        return Message(success=False)

@router.get("/user-sessions/{user_id}")
async def get_user_sessions_admin(user_id: int, current_admin: CurrentAdmin):
    sessions = await get_sessions_by_user_id_remove_invalid(user_id)
    sviews = [SessionView(id=s.id, user_id=s.user_id, token=s.token, creation_date=s.creation_date) for s in sessions]
    return sviews

@router.post("/delete-session/{session_id}")
async def delete_session_by_id_admin(session_id: int, current_admin: CurrentAdmin):
    try:
        await del_session_by_id(session_id)
    except ValueError as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="session not found")


