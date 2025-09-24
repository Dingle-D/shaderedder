from sqlalchemy import Date, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.postgresql import Base 

from typing import Optional
from app.models import Role
import datetime


class UsersOrm(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_activated: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Role] = mapped_column(default=Role.USER)
    should_reset_token: Mapped[bool] = mapped_column(default=False)

    shaders: Mapped[list["ShadersOrm"]] = relationship(back_populates='author')


class ShadersOrm(Base):
    __tablename__ = 'Shaders'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))

    author: Mapped['UsersOrm'] = relationship(back_populates='shaders')
    shader_files: Mapped[list["ShaderFileOrm"]] = relationship(
        back_populates='shader',
        cascade="all, delete-orphan"
    )


class ShaderFileOrm(Base):
    __tablename__ = 'ShaderFiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    file: Mapped[str]
    uniforms: Mapped[str] # json e.g. [{"name": value}, {"another_name": [value, value]}]
    shader_id: Mapped[int] = mapped_column(ForeignKey('Shaders.id'))

    shader: Mapped['ShadersOrm'] = relationship(back_populates='shader_files')
