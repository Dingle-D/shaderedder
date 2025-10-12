from sqlalchemy import select, delete
from datetime import timedelta, datetime

from app.db.postgresql import connection
from app.db.schemas import UsersOrm, SessionsOrm

from app.security.access_token import is_token_valid

from app.models import SessionBase, SessionView

from app.core.config import settings


@connection 
async def get_sessions_by_user_id(id: int, session):
    result = await session.execute(select(SessionsOrm).where(SessionsOrm.user_id == id))
    sessions = result.scalars().all()
    return sessions

@connection 
async def get_sessions_by_user_id_remove_invalid(id: int, session):
    result = await session.execute(select(SessionsOrm).where(SessionsOrm.user_id == id))
    sessions = result.scalars().all()
    to_remove = []
    valid = []
    for s in sessions:
        if is_token_valid(s.token):
            valid.append(s)
        else:
            to_remove.append(s.id)
    await session.execute(delete(SessionsOrm).where(SessionsOrm.id in to_remove))
    return valid


@connection 
async def get_session_by_token(token: str, session):
    result = await session.execute(select(SessionsOrm).where(SessionsOrm.token == token))
    se = result.scalars().first()
    return se


@connection
async def add_session(user_session: SessionBase, session):
    new_session = SessionsOrm(token=user_session.token, user_id=user_session.user_id, creation_date=user_session.creation_date)
    session.add(new_session)
    await session.commit()

@connection 
async def del_session_by_id(id: int, session):
    result = await session.execute(select(SessionsOrm).where(SessionsOrm.id == id))
    se = result.scalars().first()
    if not se:
        raise ValueError("session not found")
    session.delete(se)
    await session.commit()

@connection 
async def del_session_by_token(token: str, session):
    result = await session.execute(select(SessionsOrm).where(SessionsOrm.token == token))
    se = result.scalars().first()
    if not se:
        raise ValueError("user not found")
    session.delete(se)
    await session.commit()

@connection
async def del_expired_sessions(delete_before: datetime, session):
    await session.execute(delete(SessionsOrm).where(SessionsOrm.expiration_date < delete_before))
    await session.commit()

@connection
async def del_user_sessions(user_id: int, session):
    await session.execute(delete(SessionsOrm).where(SessionsOrm.user_id == user_id))
    await session.commit()
