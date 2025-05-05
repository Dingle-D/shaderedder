from fastapi import APIRouter, Depends, HTTPException

from app.api.routes.login import CurrentUser
from app.models import UserView

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserView)
def read_users_me(current_user: CurrentUser):
    return current_user


