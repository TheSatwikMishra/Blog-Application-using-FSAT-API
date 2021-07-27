from sqlalchemy import create_engine,Column,Integer,String 
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
engine=create_engine( 
    "postgresql://postgres:root@localhost:5432/new_blogs", echo=False
    ) 
Session=sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base=declarative_base()