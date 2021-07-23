from .database import Base
from sqlalchemy import String,Boolean,Integer,Column
from .database import Base

class blog(Base):
    __tablename__='blogs'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)