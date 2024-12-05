from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
import utils        # utils is the file name in same folder and i want to acces their intances 
import schemas      #this are the file names in the same folder
import models
from sqlalchemy.orm import Session
from database import engine,get_db


router = APIRouter(
    prefix="/users",
    tags=['Users']

)

# Creating user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db:Session = Depends(get_db)): 

    # hash the password - user.password

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

   
# get user by id
@router.get("/{id}", response_model=schemas.UserResponse)
def create_user(id: int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"user with id {id} was not found")


    return user