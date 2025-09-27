from fastapi import APIRouter

from app.api.routes import admin
from app.api.routes import login 
from app.api.routes import register
from app.api.routes import explore
from app.api.routes import shader

api_router = APIRouter()
api_router.include_router(admin.router)
api_router.include_router(login.router)
api_router.include_router(register.router)
api_router.include_router(explore.router)
api_router.include_router(shader.router)
