from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import String,Boolean,Integer,Column,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class blog(Base):
    __tablename__='blogs'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)
    userid=Column(Integer,ForeignKey('users.id'))
    creator=relationship("user",back_populates="blogss") #this is how we make relationships

class user(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogss=relationship("blog",back_populates="creator") #this is how we make relationships 