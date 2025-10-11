from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.api.api_router import api_router
from app.db.postgresql import init_db, close_db
from app.db.services.users import init_users
from app.db.services.shaders import init_shaders
from app.security.security_headers_middleware import FrameOptionsMiddleware, CSPMiddleware
from app.core.config import settings
import warnings
import asyncio

app = FastAPI(redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    #allow_origins=settings.all_cors_origins,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

#app.add_middleware(FrameOptionsMiddleware)
#app.add_middleware(CSPMiddleware)
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


