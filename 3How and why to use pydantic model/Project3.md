
# FastAPI Project: Understanding Pydantic Models

This project introduces **Pydantic Models** in a FastAPI application. It demonstrates their purpose, usage, and how they assist in data validation and conversion.

## Key Objectives

1. **What is a Pydantic Model?**
   - A Pydantic model is a data validation and parsing tool provided by FastAPI to define the structure of data.
   - It ensures that the incoming request data meets the specified requirements.

2. **Why Use Pydantic Models?**
   - Validates the incoming data.
   - Automatically generates documentation in FastAPI.
   - Converts data to the specified types and provides default values if specified.

3. **How to Use Pydantic Models in FastAPI?**
   - Create a Pydantic model by subclassing `BaseModel`.
   - Define attributes with types, default values, or make them optional.
   - Use the model as a parameter in your API endpoints to automatically validate incoming data.

## Code Explanation

### Importing Required Modules

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
```

- `FastAPI`: Framework for building APIs.
- `BaseModel`: Class from Pydantic to define data models.
- `Optional`: Specifies optional fields.

### Defining the FastAPI App

```python
app = FastAPI()
```

- `app` is an instance of `FastAPI`, representing the application.

### Creating a Pydantic Model

```python
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
```

- **Attributes**:
  - `title`: Required string field.
  - `content`: Required string field.
  - `published`: Optional boolean with a default value of `True`.
  - `rating`: Optional integer.

### Root Endpoint

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

- A basic endpoint to verify the application is running.

### `GET /posts` Endpoint

```python
@app.get("/posts")
async def get_posts():
    return {"message": "this is your first post"}
```

- A simple endpoint to fetch posts.

### `POST /createpost` Endpoint

```python
@app.post("/createpost")
async def create_posts(post: Post):
    print(post)  # Example: title='students', content='southern', published=True, rating=77
    print(post.dict())  # Converts the Pydantic model to a dictionary
    return {"message": f"{post}"}
```

- Accepts a `Post` object.
- Demonstrates the benefits of using Pydantic:
  - Converts the model to a dictionary using `post.dict()`.
  - Validates and parses incoming data.

### Testing with Example Request

- **POST `/createpost`**:
  ```json
  {
      "title": "students",
      "content": "southern",
      "published": true,
      "rating": 77
  }
  ```

  Response:
  ```json
  {
      "message": "title='students' content='southern' published=True rating=77"
  }
  ```

## Key Takeaways

- **Pydantic Models** are essential for data validation in FastAPI.
- They ensure the correctness of incoming data and simplify working with request bodies.
- The `dict()` method allows easy conversion of Pydantic objects to dictionaries.

---

### Running the Application

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
3. Test endpoints using **Postman** or visit `http://127.0.0.1:8000/docs`.

---
