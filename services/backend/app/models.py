from pydantic import (
    BaseModel,
    EmailStr,
    conint,
    field_validator,
    HttpUrl,
    validator,
    ValidationError
)
from fastapi import Query
from typing import Literal, Optional, TypeVar, Generic, List
from datetime import datetime
import enum 

class Role(int, enum.Enum):
    ADMIN = 1 
    USER = 2

T = TypeVar("T")

class UserBase(BaseModel):
    username: str
    class Config:
        from_attributes=True

class UserLogin(UserBase):
    password: str

class UserRegister(UserLogin):
    email: EmailStr

class UserOauth(UserBase):
    email: EmailStr

class Identifier(BaseModel):
    id: int
    class Config:
        from_attributes=True

class UserView(UserBase):
    id: int
    is_activated: bool
    role: Role
    email: EmailStr

class ShaderBase(BaseModel):
    title: str 
    author: str
    class Config:
        from_attributes=True

class ShaderDescription(BaseModel):
    title: str
    author_id: int
    description: str

class ShaderFileDescription(BaseModel):
    type: Literal['frag', 'ver']
    source: str
    uniforms: str = "[]"

class ShaderView(ShaderBase):
    id: int

class ShaderComplete(ShaderView):
    description: str 

class CollectionBase(BaseModel):
    title: str 
    class Config:
        from_attributes=True 

class CollectionView(CollectionBase):
    id: int 
    tags: list[str]

class PaginationOptions(BaseModel):
    limit: conint(ge=1, le=100) = 10
    offset: conint(ge=0) = 0

    @classmethod 
    def as_query(cls, limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
        return cls(limit=limit, offset=offset)

class PaginationMeta(BaseModel):
    offset: int 
    limit: int 
    total: Optional[int] = None

class PaginationResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta

class Token(BaseModel):
    access_token: str 
    token_type: str = 'bearer'

class EmailData(BaseModel):
    html_content: str
    subject: str

class Message(BaseModel):
    success: bool
    comment: str = ""

class MessageRegister(Message):
    activated: bool

class EmailStatus(BaseModel):
    status_code: int
    status_text: str

class Password(BaseModel):
    password: str

    @validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 symbols in len")
        
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase character")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase character")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[@$!%*?&#]", value):
            raise ValueError("Password must contain at least one of symbols (@$!%*?&#)")
        
        forbidden_pattern = r"[^A-Za-z0-9@$!%*?&#]"
        if re.search(forbidden_pattern, value):
            raise ValueError("Allowed only latin symbols, digits and symbols @$!%*?&#")
        
        return value
