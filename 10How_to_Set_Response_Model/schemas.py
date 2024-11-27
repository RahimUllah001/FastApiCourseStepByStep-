# schema is also callled pydantic model which actually the class according to  which we will expect coming  request or coming response

from pydantic import BaseModel
from datetime import datetime

# Base class or base model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool =True 

# model for creating post how type data it should expct whne creating a post  
class CreatePost(PostBase):
    pass

# model for updating post how type data it should expct whne updating a post  

class UpdatePost(PostBase):
    pass

# what type of data it will giv ein repsonse
class PostResponse(PostBase):
    
    id: int 
    created_at: datetime
    
    # As sqlachemy return an objects but pydantic can only work with dictionary so the bewlow two line wil make pydantic able to work with objet of orm/sqlalchemy 
    class config:
        orm_mode = True
