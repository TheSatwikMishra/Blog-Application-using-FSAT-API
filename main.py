from typing import Optional
from fastapi import FastAPI  #import
from typing import Optional
from pydantic import BaseModel
app=FastAPI() #instantiate

@app.get('/')  #decorate
def index():   #function
    return({'data':{'name':'satwik'}})
#learnt about query parameters(the arguments passed in this function)
@app.get('/blog')
def show(limit=10,published: bool=True):
    #fetch blog with id=id
     return( f' {limit} {published}')  
#learnt what is post method and have doubt about how this is working
#by generating these kind of classes we can in take data from the user and  bring it here to python
# isiko hum schemas.py file me bhi daal skte
class Blog(BaseModel):
    title: str
    body: str
    published : Optional[bool]
@app.post('/blog')
def create_blog(blog:Blog):
    return(f'blog with title {blog.title} is created')

