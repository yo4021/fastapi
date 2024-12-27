from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    details: Optional[str] = None

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed: bool

    class Config:
        from_attributes = True

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True