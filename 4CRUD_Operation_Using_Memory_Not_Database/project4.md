
# FastAPI CRUD Operations Project

This project demonstrates how to perform CRUD (Create, Read, Update, Delete) operations in a FastAPI application using an in-memory data structure (a Python list). It serves as a step-by-step guide for beginners learning FastAPI.

## Project Overview

- **Framework**: FastAPI
- **Data Storage**: In-memory (Python list)
- **API Testing Tool**: Postman
- **Core Functionality**:
  - Create a post
  - Read all posts
  - Read a single post
  - Update a post
  - Delete a post

## Code Explanation

### 1. Setting Up the Application

```python
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()
```

- **FastAPI**: Framework used for building APIs.
- **Pydantic**: Used for data validation (`BaseModel`).
- **Modules**: `randrange` generates random IDs for posts.

### 2. Defining the Data Model

```python
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
```

- This model defines the structure of a post with fields: `title`, `content`, `published`, and an optional `rating`.

### 3. In-Memory Data Storage

```python
my_posts = [
    {"title": "Southern", "content": "UETM students", "id": 1},
    {"title": "swatian", "content": "UETM students", "id": 2},
    {"title": "swatian", "content": "UETM students", "id": 3}
]
```

- A list of dictionaries is used to simulate a database.

### 4. Helper Functions

```python
def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index
```
- `find_post`: Finds a post by its ID.
- `find_index`: Returns the index of a post by its ID.

### 5. API Endpoints

#### a. Root Endpoint

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

- Basic endpoint to verify the application is running.

#### b. Get All Posts

```python
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}
```

- Retrieves all posts.

#### c. Create a Post

```python
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    new_post = post.dict()
    new_post['id'] = randrange(0, 1000)
    my_posts.append(new_post)
    return {"message": new_post}
```

- Creates a new post using `POST` method.

#### d. Get a Single Post

```python
@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    return {"data": post}
```

- Retrieves a post by its ID. Returns `404` if not found.

#### e. Delete a Post

```python
@app.delete("/posts/{id}")
async def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    my_posts.pop(index)
    return {"message": "post was successfully deleted"}
```

- Deletes a post by ID. Returns `404` if not found.

#### f. Update a Post

```python
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    post_data = post.dict()
    post_data['id'] = id
    my_posts[index] = post_data
    return {"data": my_posts}
```

- Updates an existing post by ID.

## Testing with Postman

1. **GET `/posts`**: Fetch all posts.
2. **POST `/posts`**: Create a new post. Provide the following body:
   ```json
   {
       "title": "New Title",
       "content": "New Content",
       "published": true
   }
   ```
3. **GET `/posts/{id}`**: Fetch a post by ID.
4. **PUT `/posts/{id}`**: Update a post by ID. Provide the updated data in the body.
5. **DELETE `/posts/{id}`**: Delete a post by ID.

## How to Run

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
3. Open `http://127.0.0.1:8000/docs` in your browser to explore the APIs.

## Key Learnings

- FastAPI simplifies the creation of RESTful APIs.
- In-memory data storage can be used for prototyping.
- Pydantic models ensure robust data validation.

---
