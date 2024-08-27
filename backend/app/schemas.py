from pydantic import BaseModel

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
    