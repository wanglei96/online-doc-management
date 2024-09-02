from typing import Optional
from pydantic import BaseModel
from sqlalchemy import delete

class UserBase(BaseModel):
    username: str

class UserDelete(BaseModel):
    id: int

class UserCreate(UserBase):
    password: str
    is_admin: int

class UserInfo(UserBase):
    is_admin: int

class User(UserBase):
    id: int
    is_admin: int

    class Config:
        orm_mode = True
        
class File(BaseModel):
    id: int
    filename: str
    file_tag: str

class FileDelete(BaseModel):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
    
class FileTagBase(BaseModel):
    tag_name: str

class FileTagCreate(FileTagBase):
    sort_order: Optional[int] = None
    
class Tags(BaseModel):
    id: int
    tag_name: str
    sort_order: int
    
class deleteTag(BaseModel):
    id: int
    
class EditTag(BaseModel):
    id: int
    new_tag_name: str
    new_sort_order: int