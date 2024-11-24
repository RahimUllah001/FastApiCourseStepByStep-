from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool =True
    rating: Optional[int] = None


my_posts = [{"title":"Southern","content":"UETM students","id": 1},
            {"title":"swatian","content":"UETM students","id": 2},
            {"title":"swatian","content":"UETM students","id": 3}
           ]

def find_post(id:int):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for index,post in enumerate(my_posts):
        if post['id'] == id:
            return index


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):  
    print(post)

    new_post = post.dict()
    new_post['id'] = randrange(0,1000)
    my_posts.append(new_post)
    return {"message": new_post}



@app.get("/posts/{id}")
async def get_post(id: int): 
    print(id) 

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    
  
    return {"data": post}


@app.delete("/posts/{id}")
async def delete_post(id: int): 

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    index = find_index(id)
    my_posts.pop(index)
    return {"message":"post was successfully deleted"}

    

@app.put("/posts/{id}")
async def update_post(id: int,post:Post): 
    print(type(id))
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")

    post = post.dict()
    post['id'] = id
    my_posts[index] = post
    
    return {"data": my_posts}