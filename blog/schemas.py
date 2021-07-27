from pydantic import BaseModel
from typing import Optional,List
# we store all the classes into this folder
# ye iss class ke parameters kp requestr body me bhejne ke kaam aata hai

class BlogBase(BaseModel):
    title : str
    body : str

class Blog(BlogBase):
    class Config:
        orm_mode=True

class user(BaseModel):
    name: str
    email : str
    password : str

class showuser(BaseModel):
    name: str
    email :str
    blogss : List[Blog]
    class Config:
        orm_mode=True

class showblog(BaseModel):
    title : str
    body : str
    creator : showuser
    class Config:
        orm_mode=True

class login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None