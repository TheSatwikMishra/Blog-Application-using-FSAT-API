import pdb
from os import name
from fastapi import FastAPI,status,HTTPException#always done
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.sql.elements import Null
from . import schemas,models,token,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .database import engine,Session as ss #ye Session alag hai ye database wala hai
from sqlalchemy.orm import Session  #ye Session alag hai ye main.py wala h
from passlib.context import CryptContext


app=FastAPI()

models.Base.metadata.create_all(engine) #'''Jab Jab server chl rha h tb tb naya database bn rha h kya'''

def get_db():
  db=ss()   #we imported this session from the database and not from sqlalchemy
  try:
   yield db
  finally:
   db.close()

@app.post('/blog',tags=['blogs'])
# Now we are linking our database with FastAPI and lets see how that happens
# We did successfully added data to our tsble using the syntax below
def create(blog : schemas.Blog, db: Session=Depends(get_db),status_code=status.HTTP_201_CREATED):#the session used here is from sqlalchemy and not from database
    new_blog=models.blog(title=blog.title,body=blog.body,userid=32)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return(new_blog)


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blogs'])
def update(id,request : schemas.Blog,db: Session=Depends(get_db)):
    blogg=db.query(models.blog).filter(models.blog.id==id)
    if not  blogg.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'the blog with id {id} is not found')
    else:
     blogg.update({models.blog.title:request.title,models.blog.body:request.body},synchronize_session=False)
    db.commit()
    return('UPDATED')

 #after creating a blog we need to get the blog form db
@app.get('/all_blogs',tags=['blogs'])
def show(db: Session=Depends(get_db),get_current_user:schemas.user = Depends(oauth2.get_current_user)):
    blog=db.query(models.blog).all()   
    return(blog)

@app.get('/blog/{id}',tags=['blogs'],response_model=schemas.showblog)
def by_id(id,db: Session=Depends(get_db)):
    blog = db.query(models.blog).filter(models.blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The blog with id {id} is not found')
    return(blog)


#this is the simple query to delete a blog from our database
@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def destroy(id,db: Session=Depends(get_db)):
    blogg=db.query(models.blog).filter(models.blog.id==id)
    if not  blogg.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'the blog with id {id} is not found')
    else:
     blogg.delete(synchronize_session=False)
    db.commit()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#yha ek hashed password generate kia hai
@app.post('/create_user', response_model=schemas.showuser,tags=['users'])
def createuser(new_user:schemas.user,db: Session=Depends(get_db)):
    hashed_password=pwd_context.hash(new_user.password) #hashed password ko normal password se link kia hai
    new_use=models.user(name=new_user.name,email=new_user.email,password=hashed_password)
    db.add(new_use)
    db.commit()
    return(new_use)



@app.post('/login',tags=['Authentication'])
def login(log:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(get_db)):
   user=db.query(models.user).filter(models.user.email==log.username).first()
   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')
   if not pwd_context.verify(log.password,user.password):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Incorrect Password')
       #generate JWT and return it
   access_token = token.create_access_token(data={"sub": user.email})
   return {"access_token": access_token, "token_type": "bearer"}



@app.get('/showuser/{id}',response_model=schemas.showuser,tags=['users'])
def showuser(id,db :Session=Depends(get_db)):
    user = db.query(models.user).filter(models.user.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The blog with id {id} is not found')
    return(user)

