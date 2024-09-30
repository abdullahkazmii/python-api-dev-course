from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        # orm_mode = True
        orm_mode = True


class PostOut(PostBase):
    title: str
    content: str
    publish: bool = True
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int  
    dir: conint(le = 1)

    model_config = {
        'arbitrary_types_allowed': True
    }

