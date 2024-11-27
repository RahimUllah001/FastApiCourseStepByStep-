# uvicorn main:app --reload
from fastapi import FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

import schemas      #this are the file names in the same folder
import models
from database import engine,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Ali_wazir1',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("databse connection successfull")
        break

    except Exception as error:
        print("databse connection fail")
        print("Error:",error)
        time.sleep(2)




@app.get("/")
async def root():
    return {"message": "Hello World"}



# getting all data from database
@app.get("/posts",response_model=List[schemas.PostResponse])        #List[schemas.PostResponse] here i use the list function because the post repisne is for ine post and we are reicevng multiple post usually o  should make the reposne alos of list so that multiple repsonses models for reponses 
async def get_posts(db:Session = Depends(get_db)):
   
    posts = db.query(models.Post).all()
    return posts

# creating post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.CreatePost, db:Session = Depends(get_db)):  
    
    # sql alchemy orm
    new_post = models.Post(**post.dict())       #using dcitionary unpacking to extract data to new post ==> this is equilent to==> new_post = models.Post(title="My Title", content="My Content", published=True) means values are the actual values 

    db.add(new_post)
    db.commit()
    db.refresh(new_post)        #this line is for retirving out new post as we use returning keyword in sql alchemy

    return new_post


# getting post of speciffic id
@app.get("/posts/{id}",response_model=schemas.PostResponse)
def get_post(id: int,db:Session = Depends(get_db)): 
    
    
    post = db.query(models.Post).filter(models.Post.id == id).first() # ==>corresponding sql querry but when first( is not written) ==>SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts WHERE posts.id = %(id_1)s
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
  
    return post


# Delete a post
@app.delete("/posts/{id}")
async def delete_post(id: int, db:Session = Depends(get_db)): 
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    deleted_post = post

    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return deleted_post

    
# updating post
@app.put("/posts/{id}",response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.UpdatePost, db:Session = Depends(get_db)): 
   
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post = post_querry.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    
    post_querry.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
    return post_querry.first()