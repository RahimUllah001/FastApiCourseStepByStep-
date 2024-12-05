from fastapi import FastAPI, Response, status,HTTPException,Depends,APIRouter
import models
import schemas      #this are the file names in the same folder
from sqlalchemy.orm import Session
from database import engine,get_db
from typing import List,Optional
import oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
# getting all data from database
@router.get("/",response_model=List[schemas.PostResponse])        #List[schemas.PostResponse] here i use the list function because the post repisne is for ine post and we are reicevng multiple post usually o  should make the reposne alos of list so that multiple repsonses models for reponses 
async def get_posts(db:Session = Depends(get_db), limit: int = 10, skip: int = 0, search : Optional[str] = ""):     # {{URL}}posts?limit=11&search=ibraim ==> will pass such querry parameters
    
    print(limit)
    print(skip)
    print(search)

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# creating post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):  
    
    print(current_user.email)
    print(current_user.id)
    # sql alchemy orm
    new_post = models.Post(owner_id=current_user.id,**post.dict())       #here i am sending owner_id to the db as owner_id is nullable - flase which is actually here the current user 

    db.add(new_post)
    db.commit()
    db.refresh(new_post)        #this line is for retirving out new post as we use returning keyword in sql alchemy

    return new_post


# getting post of speciffic id
@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id: int,db:Session = Depends(get_db)): 
    
    post = db.query(models.Post).filter(models.Post.id == id).first() # ==>corresponding sql querry but when first( is not written) ==>SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts WHERE posts.id = %(id_1)s
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
  
    return post


# Delete a post
@router.delete("/{id}")
async def delete_post(id: int, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)): 
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    deleted_post = post

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"You are not authorized to delete this post")


    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return deleted_post

    
# updating post
@router.put("/{id}",response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.UpdatePost, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)): 
   
    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post = post_querry.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"post with {id} was not found")
    
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"You are not authorized to update this post")

    post_querry.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    
    return post_querry.first()

