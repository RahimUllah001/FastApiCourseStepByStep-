# schema is also callled pydantic model which actually the class according to  which we will expect coming  request or coming response

from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

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
    owner_id: int       #this will show whime created the post
    
    # As sqlachemy return an objects but pydantic can only work with dictionary so the bewlow two line wil make pydantic able to work with objet of orm/sqlalchemy 
    class config:
        orm_mode = True

# request type for user creation
class CreateUser(BaseModel):
    email: EmailStr
    password: str

# Response on user creation 
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True

# request type for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str 

# Response to login as it give a token in return Token in response
class Token(BaseModel):
    access_token: str 
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    # create_at: datetime

