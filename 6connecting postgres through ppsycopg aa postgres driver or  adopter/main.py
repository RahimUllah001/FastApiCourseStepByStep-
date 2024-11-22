from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 



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
