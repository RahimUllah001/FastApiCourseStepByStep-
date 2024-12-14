from fastapi import status, HTTPException, Depends, APIRouter
import models
import schemas  # this are the file names in the same folder
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import oauth2
from sqlalchemy import func
from utils import map_post_to_response,map_posts_to_response

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# getting all data from database
@router.get("/", response_model=List[schemas.PostWithLike])
async def get_posts(db: Session = Depends(get_db)):
    # Query to get posts and the number of likes
    posts_with_likes = (
        db.query(models.Post, func.count(models.Like.post_id).label("likes"))
        .join(models.Like, models.Like.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .all()
    )

    return map_posts_to_response(posts_with_likes)
        # return posts_with_likes



# creating post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    print(current_user.email)
    print(current_user.id)
    # sql alchemy orm
    # here i am sending owner_id to the db as owner_id is nullable - flase which is actually here the current user
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    # this line is for retirving out new post as we use returning keyword in sql alchemy
    db.refresh(new_post)

    return new_post


# getting post of speciffic id
@router.get("/{id}", response_model=schemas.PostWithLike)
def get_post(id: int, db: Session = Depends(get_db)):

    post_with_likes = (
        db.query(models.Post, func.count(models.Like.post_id).label("likes"))
        .join(models.Like, models.Like.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )
    
    if not post_with_likes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")

    post, likes = post_with_likes  # Unpack the tuple

    # Construct the response
    return map_post_to_response(post, likes)



# Delete a post
@router.delete("/{id}")
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    deleted_post = post

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to delete this post")

    # post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    return deleted_post


# updating post
@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post_querry = db.query(models.Post).filter(models.Post.id == id)
    post = post_querry.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorized to update this post")

    post_querry.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_querry.first()
