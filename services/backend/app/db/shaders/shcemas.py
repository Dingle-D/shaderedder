from sqlalchemy import Date, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.postgresql import Base 
from typing import Optional
import datetime

class ShaderOrm(Base):
    __tablename__ = 'Shaders'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    vertex_shader: Mapped[str]
    fragment_shader: Mapped[str]
    preview: Mapped[str]
    description: Mapped[str]
