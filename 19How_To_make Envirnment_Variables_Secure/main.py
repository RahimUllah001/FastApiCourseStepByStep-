from fastapi import FastAPI
from database import engine
from routers import post, user,auth
import models
from config import settings

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# this three lines show the path appication ==>  Api Router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


