from sqlalchemy import select

from app.db.ext import connection
from app.db.shaders.shcemas import ShaderOrm

from app.core.config import settings

@connection 
async def init_shaders(session):
    empty = ShaderOrm(title='empty', 
                     vertex_shader='',
                     fragment_shader='',
                     preview='', 
                     description="Empty shader"
    )
    session.add(empty)
    await session.commit()
