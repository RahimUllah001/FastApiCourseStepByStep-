# uvicorn main:app --reload
from fastapi import FastAPI, Response, status,HTTPException,Depends
from fastapi.params import Body 
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
import models
from database import engine,get_db
from sqlalchemy.orm import Session

from routers import post, user

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

# this two lines show the path appication 
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


