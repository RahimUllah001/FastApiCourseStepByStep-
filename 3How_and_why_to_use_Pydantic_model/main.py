from fastapi import FastAPI
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool =True
    rating: Optional[int] = None



@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
async def get_posts():
    return {"message": "this is your first post"}


@app.post("/createpost")
async def create_posts(post: Post):  

    print(post)    # pydantic .model ==. title='students' content='southern' published=True rating=77
    print(post.dict())    #to conevert pydantic model to dictionary  ==>{'title': 'students', 'content': 'southern', 'published': True, 'rating': 77}
    return {"message": f"{post}"}


