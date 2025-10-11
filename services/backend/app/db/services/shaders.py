from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.schemas import ShadersOrm, ShaderFileOrm, UsersOrm
from app.db.postgresql import connection

from app.core.config import settings

from app.models import ShaderDescription, ShaderFileDescription, PaginationOptions

from pathlib import Path 
from typing import List

# returns absolute path for given filename in predefined shaders directory
def _get_absolute_path(filename: str) -> str:
    pth = Path.cwd() / "app/shaders"
    file_path = pth / filename
    if not file_path.exists():
        raise RuntimeError("Predefined shaders path does not exists")
    print("Predefined path:", file_path)
    return str(file_path)

@connection
async def add_shader(sv: ShaderDescription, sf: ShaderFileDescription, session):
    shader = ShadersOrm(title=sv.title,
        description=sv.description,
        access=sv.access_type,
        author_id=sv.author_id
    )
    session.add(shader)

    file = ShaderFileOrm(
        type=sf.type,
        file=sf.source,
        storage_type=sf.storage_type,
        uniforms=sf.uniforms,
        shader=shader
    )
    session.add(file)
    await session.commit()

@connection
async def get_shader_by_id(id: int, session):
    result = await session.execute(select(ShadersOrm).where(ShadersOrm.id == id))
    shader = result.scalars().first()
    return shader

@connection
async def get_shader_file_by_shader_id(id: int, session):
    result = await session.execute(select(ShaderFileOrm).where(ShaderFileOrm.shader_id == id))
    shader_file = result.scalars().first()
    return shader_file

@connection
async def delete_shader_by_id(id: int, session):
    result = await session.execute(select(ShadersOrm).where(ShadersOrm.id == id))
    shader = result.scalars().first()
    if not shader:
        raise ValueError("Shader not found")
    session.delete(shader)
    await session.commit()

@connection 
async def delete_shader(shader: ShadersOrm, session):
    session.delete(shader)
    await session.commit()

@connection 
async def get_shaders_by_substring(pattern: str, session):
    pass

@connection
async def get_shaders_window(options: PaginationOptions, session):
    result = await session.execute(select(ShadersOrm).offset(options.offset).limit(options.limit))
    users = result.scalars().all()
    return users

@connection
async def get_shaders_view_window(options: PaginationOptions, session):
    result = await session.execute(select(ShadersOrm).offset(options.offset).limit(options.limit).options(selectinload(ShadersOrm.author)))
    users = result.scalars().all()
    return users

@connection
async def get_shaders_total(session):
    result = await session.execute(select(func.count()).select_from(ShadersOrm))
    total = result.scalar_one()
    return total


@connection 
async def init_shaders(session):
    # example 1
    default = ShadersOrm(title='gradient', 
        description='Default shader for showcase',
        author_id=2
    )
    default_file = ShaderFileOrm(
        type="frag",
        file=_get_absolute_path("default.frag"),
        storage_type="local",
        shader=default,
        uniforms="[]"
    )
    session.add(default)
    # example 2
    circles = ShadersOrm(title='circles', 
        description='Circles shader for showcase',
        author_id=2
    )
    circles_file = ShaderFileOrm(
        type="frag",
        file=_get_absolute_path("circles.frag"),
        storage_type="local",
        shader=circles,
        uniforms="[]"
    )
    session.add(circles)

    #example 3
    plasma = ShadersOrm(title='plasma', 
        description='Plasma shader for showcase',
        author_id=2
    )
    plasma_file = ShaderFileOrm(
        type="frag",
        file=_get_absolute_path("plasma.frag"),
        storage_type="local",
        shader=plasma,
        uniforms="[]"
    )
    session.add(plasma)

    # example 4
    squares = ShadersOrm(title='squares', 
        description='Squares shader for showcase',
        author_id=2
    )
    squares_file = ShaderFileOrm(
        type="frag",
        file=_get_absolute_path("squares.frag"),
        storage_type="local",
        shader=squares,
        uniforms="[]"
    )
    session.add(squares)

    # example 5
    stars = ShadersOrm(title='pixel stars', 
        description='Pixel stars shader for showcase',
        author_id=2
    )
    stars_file = ShaderFileOrm(
        type="frag",
        file=_get_absolute_path("pixel_stars.frag"),
        storage_type="local",
        shader=stars,
        uniforms="[]"
    )
    session.add(stars)

    # example 6
    vortex = ShadersOrm(title='vortex', 
        description='Vortex shader for showcase',
        author_id=2
    )
    vortex_file = ShaderFileOrm(
        type="frag",
        file=_get_absolute_path("vortex.frag"),
        storage_type="local",
        shader=vortex,
        uniforms="[]"
    )
    session.add(vortex)

    await session.commit()

