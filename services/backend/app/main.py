from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api.api_router import api_router
from app.db.postgresql import init_db, close_db
from app.db.services.users import init_users
from app.db.services.shaders import init_shaders
from app.core.config import settings
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    #allow_origins=['http://localhost:8080'],
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['X-Uniforms', 'Uniforms', 'X-Custom-Uniforms'],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

@app.on_event("startup")
async def startup():
    await init_db()
    await init_users()
    await init_shaders()

@app.on_event("shutdown")
async def startup():
    await close_db()

@app.get("/")
def get_root():
    return "Hello, World"

app.include_router(api_router, prefix=settings.API_V1_STR)

