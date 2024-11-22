from fastapi import FastAPI

app = FastAPI()     #instance of fastapi

@app.get("/")       #decorator to root function
async def root():       #root function 
    return {"message": "Hello World"}       #return message