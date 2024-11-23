# uvicorn main:app --reload
from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 



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

# getting all data from database
@app.get("/posts")
async def get_posts():
    cursor.execute("""select * FROM posts""")
    posts = cursor.fetchall()
    print(posts)

    return {"data": posts}

# creating post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):  
    
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ('{post.title}', '{post.content}', {post.published}) RETURNING *")      #this is not a saf e way it expoits for sql injection
    # new_post = cursor.fetchone()
   
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content, post.published))      #safe way
    new_post = cursor.fetchone()

    conn.commit()
    return {"message": new_post}


# getting post of speciffic id
@app.get("/posts/{id}")
def get_post(id: int): 
    
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))     #here 
    post = cursor.fetchone()
    print(post)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
  
    return {"data": post}


# Delete a post
@app.delete("/posts/{id}")
async def update_post(id: int): 

    cursor.execute("""DELETE  FROM posts WHERE id = %s returning * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()

    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    return {"This post with following detail successfully deleted": post}

    

@app.put("/posts/{id}")
async def update_post(id: int,post:Post): 
   
    cursor.execute("""update posts set title = %s, content = %s, published =  %s where id = %s returning * """, (post.title, post.content, post.published,str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")

    
    return {"Updated post": post}