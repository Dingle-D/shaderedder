from sqlalchemy import select, func
from datetime import timedelta

from app.db.postgresql import connection
from app.db.schemas import UsersOrm
from app.db.redis import redis_client

from app.models import UserLogin, UserOauth, UserRegister, PaginationOptions, Role
from app.core.config import settings

from app.security.password import get_password_hash, verify_password

import app.security

CONFIRM_PREFIX = 'activate:'

@connection 
async def init_users(session):
    admin = UsersOrm(username='admin', 
                     email=settings.FIRST_SUPERUSER, 
                     password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD), 
                     is_activated=True, 
                     role=Role.ADMIN
    )
    shaderedder = UsersOrm(username="shaderedder",
                           email="shaderedder@example.com",
                           password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                           is_activated=True,
                           role=Role.USER)
    session.add(admin)
    session.add(shaderedder)
    await session.commit()

@connection
async def get_users(options: PaginationOptions, session):
    result = await session.execute(select(UsersOrm).offset(options.offset).limit(options.limit))
    users = result.scalars().all()
    return users


@connection 
async def get_users_total(session):
    result = await session.execute(select(func.count()).select_from(UsersOrm))
    total = result.scalar_one()
    return total

@connection
async def get_user_by_username(username: str, session):
    result = await session.execute(select(UsersOrm).where(UsersOrm.username == username))
    user = result.scalars().first()
    return user

@connection
async def get_user_by_email(email: str, session):
    result = await session.execute(select(UsersOrm).where(UsersOrm.email == email))
    user = result.scalars().first()
    return user

###
# This function can be used to add user instantly without email
# confirmation. It supposed to be used by admins or by service
###
@connection
async def add_user(user: UserRegister, session, role: Role = Role.USER):
    new_user = UsersOrm(username=user.username, email=user.email, password=get_password_hash(user.password), is_activated=True, role=role)
    session.add(new_user)
    await session.commit()

@connection
async def add_user_plain(user: UserRegister, session, role: Role = Role.USER):
    new_user = UsersOrm(username=user.username, email=user.email, password=user.password, is_activated=True, role=role)
    session.add(new_user)
    await session.commit()

###
# This function adds user using data from OAuth2
###
@connection
async def add_user_oauth(user: UserOauth, session):
    new_user = UsersOrm(username=user.username, email=user.email, password="", is_activated=True, role=Role.USER)
    session.add(new_user)
    await session.commit()

@connection 
async def change_user_username(id: int, username: str, session):
    result = await session.execute(select(UsersOrm).where(UserOrm.id == id))
    user = result.scalars().first()
    if not user:
        return None 
    user.username = username 
    await session.commit()
    await session.refresh(user)
    return user

###
# This function adds regular user into temporary redis
# database. Record can be accessed by UUID
async def schedule_user(user: UserRegister, token: str):
    ttl = timedelta(minutes=settings.EMAIL_ACTIVATION_TOKEN_EXPIRE_MINUTES)
    key = CONFIRM_PREFIX + token
    if redis_client.exists(key):
        raise ValueError("Redis: Key already exists")
    redis_client.hmset(key, {
        'username': user.username,
        'email': user.email,
        'password': get_password_hash(user.password)
    })
    redis_client.expire(key, ttl)

    
async def confirm_user(token: str):
    key = CONFIRM_PREFIX + token
    user_info = redis_client.hgetall(key)
    if not user_info:
        raise ValueError("Redis: Key not found")
    user = UserRegister(
        username=user_info.get('username'),
        email=user_info.get('email'),
        password=user_info.get('password')
    )
    redis_client.delete(key)
    await add_user_plain(user)


@connection 
async def del_user(username: str, session):
    result = await session.execute(select(UsersOrm).where(UsersOrm.username == username))
    user = result.scalars().first()
    if not user:
        raise ValueError("user not found")
    session.delete(user)
    await session.commit()

@connection 
async def activate_user(username: str, session):
    result = await session.execute(select(UsersOrm).where(UsersOrm.username == username))
    user = result.scalars().first()
    if not user:
        raise ValueError("user not found")
    user.is_activated = True 
    await session.commit()

@connection 
async def deactivate_user(username: str, session):
    result = await session.execute(select(UsersOrm).where(UsersOrm.username == username))
    user = result.scalars().first()
    if not user:
        raise ValueError("user not found")
    user.is_activated = False
    await session.commit()

@connection 
async def set_user_password(username: str, password: str, session):
    result = await session.execute(select(UsersOrm).where(UsersOrm.username == username))
    user = result.scalars().first()
    if not user:
        raise ValueError("user not found")
    user.password = password 
    await session.commit()


async def authenticate(user: UserLogin):
    db_user = await get_user_by_username(user.username)
    if not db_user:
        print("Could not find user")
        return None 
    if not verify_password(user.password, db_user.password):
        print("Could not verify password")
        return None
    return db_user

