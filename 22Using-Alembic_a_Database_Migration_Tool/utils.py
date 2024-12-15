# here we define utility function ==> are thoose functions which are reusable adn are not hardly tied with program e.g hasihng password str validation 
from typing import List,Tuple
import schemas,models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# for all posts
def map_posts_to_response(posts_with_likes: List[Tuple[models.Post, int]]) -> List[schemas.PostWithLike]:
    response = []
    for post, likes in posts_with_likes:
        response.append(
            schemas.PostWithLike(
                post=schemas.PostResponse(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                    published=post.published,
                    created_at=post.created_at,
                    owner_id=post.owner_id,
                    owner=schemas.UserResponse(
                        id=post.owner.id,
                        email=post.owner.email,
                        created_at=post.owner.created_at,
                    ),
                ),
                likes=likes,
            )
        )
    return response


# for spercific or single post
# helper function to handle the conversion of a models.Post instance to a schemas.PostResponse.
def map_post_to_response(post: models.Post, likes: int) -> schemas.PostWithLike:
    return schemas.PostWithLike(
        post=schemas.PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner_id=post.owner_id,
            owner=schemas.UserResponse(
                id=post.owner.id,
                email=post.owner.email,
                created_at=post.owner.created_at,
            ),
        ),
        likes=likes,
    )
