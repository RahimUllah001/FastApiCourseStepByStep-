from fastapi import FastAPI
from fastapi.params import Body 
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/posts")
async def get_posts():
    return {"message": "this is your first post"}


@app.post("/createpost")
async def create_posts(payload: dict = Body(...)):      #The type hint dict indicates that payload is expected to be a dictionary body(...) is a function in FastAPI used to specify that the payload parameter should be pulled from the body of an HTTP request By passing ... as an argument inside body(...), you indicate that payload is a required parameter. This is similar to setting required=True 
    print(payload)
    return {"message": f"{payload}"}


