from fastapi import FastAPI,status,HTTPException#always done
from fastapi.params import Depends
from pydantic import BaseModel
from . import schemas,models
from .database import engine,Session as ss #ye Session alag hai ye database wala hai
from sqlalchemy.orm import Session  #ye Session alag hai ye main.py wala h


app=FastAPI()

models.Base.metadata.create_all(engine) #'''Jab Jab server chl rha h tb tb naya database bn rha h kya'''

def get_db():
  db=ss()   #we imported this session from the database and not from sqlalchemy
  try:
   yield db
  finally:
   db.close()

@app.post('/blog')
# Now we are linking our database with FastAPI and lets see how that happens
# We did successfully added data to our tsble using the syntax below
def create(blog : schemas.Blog, db: Session=Depends(get_db),status_code=status.HTTP_201_CREATED):#the session used here is from sqlalchemy and not from database
    new_blog=models.blog(title=blog.title,body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return(new_blog)



 #after creating a blog we nweed to get the blog form db
@app.get('/showall')
def show(db: Session=Depends(get_db)):
    blog=db.query(models.blog).all()   
    return(blog)

@app.get('/blog/{id}')
def by_id(id,db: Session=Depends(get_db)):
    blog = db.query(models.blog).filter(models.blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The blog with id {id} is not found')

    return(blog)