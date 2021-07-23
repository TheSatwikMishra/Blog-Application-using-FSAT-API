from pydantic import BaseModel
from typing import Optional
# we store all the classes into this folder
# ye iss class ke parameters kp requestr body me bhejne ke kaam aata hai

class Blog(BaseModel):
    title : str
    body : str
    published :Optional[bool]