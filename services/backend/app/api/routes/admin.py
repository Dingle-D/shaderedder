from app.models import (
    UserRegister, 
    PaginationOptions, 
    PaginationMeta,
    PaginationResponse,
    Role, 
    UserView, 
    UserBase,
    Message
)
from app.db.services.users import get_users, add_user, get_users_total, deactivate_user, activate_user
from app.api.utils import get_current_admin, CurrentAdmin

from fastapi import APIRouter, Depends, status, HTTPException

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


@router.post("/add-user", dependencies=[Depends(get_current_admin)])
async def router_add_user(user: UserRegister):
    try:
        await add_user(user)
        return Message(success=True)
    except Exception as e:
        return Message(success=False)

@router.post("/activate-user", dependencies=[Depends(get_current_admin)])
async def router_activate_user(user: UserBase):
    try:
        await activate_user(user.username)
        return Message(success=True)
    except Exception as e:
        return Message(success=False)

@router.post("/deactivate-user", dependencies=[Depends(get_current_admin)])
async def router_deactivate_user(user: UserBase):
    try:
        await deactivate_user(user.username)
        return Message(success=True)
    except Exception as e:
        return Message(success=False)

