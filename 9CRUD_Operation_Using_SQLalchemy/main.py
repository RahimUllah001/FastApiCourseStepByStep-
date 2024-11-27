# uvicorn main:app --reload
from fastapi import FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

import models
from database import engine,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

# this is the 3rd approach to see that whya type os sql querry has been generated from the pythonic code
'''
import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


'''


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool =True

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
@app.get("/posts")
async def get_posts(db:Session = Depends(get_db)):
   
    # Raw sql
    cursor.execute("""select * FROM posts""")
    posts = cursor.fetchall()
    
    # Sql alchemy ORM

    posts = db.query(models.Post).all()
    return {"data through sql alchemy":posts}

# creating post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post,db:Session = Depends(get_db)):  
    '''Raw sql

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content, post.published))      #safe way
    new_post = cursor.fetchone()

    conn.commit()   '''
    # sql alchemy orm
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)      #but instead of this line we use dictionary unpacking appraoch so that we will not write every comoumn individuallybut wil extract from scema by itself
    new_post = models.Post(**post.dict())       #using dcitionary unpacking to extract data to new post ==> this is equilent to==> new_post = models.Post(title="My Title", content="My Content", published=True) means values are the actual values 


    db.add(new_post)
    db.commit()
    db.refresh(new_post)        #this line is for retirving out new post as we use returning keyword in sql alchemy

    return {"message": new_post}


# getting post of speciffic id
@app.get("/posts/{id}")
def get_post(id: int,db:Session = Depends(get_db)): 
    
    '''
    # Raw SQL
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),)) 
    post = cursor.fetchone()
    '''
    post = db.query(models.Post).filter(models.Post.id == id).first() # ==>corresponding sql querry but when first( is not written) ==>SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts WHERE posts.id = %(id_1)s
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
  
    return {"data": post}


# Delete a post
@app.delete("/posts/{id}")
async def delete_post(id: int, db:Session = Depends(get_db)): 
    '''
    cursor.execute("""DELETE  FROM posts WHERE id = %s returning * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()
    '''
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    deleted_post = post

    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return {"This post with following detail successfully deleted": deleted_post}

    

@app.put("/posts/{id}")
async def update_post(id: int,updated_post:Post,db:Session = Depends(get_db)): 
    '''
    cursor.execute("""update posts set title = %s, content = %s, published =  %s where id = %s returning * """, (post.title, post.content, post.published,str(id)))
    post = cursor.fetchone()
    conn.commit()

    '''
    # ORM
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post = post_querry.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    
    post_querry.update(updated_post.dict(),synchronize_session=False)

    db.commit()
    
    return {"Updated post": post_querry.first()}