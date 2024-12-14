
# FastAPI Project: Demonstrating Basic HTTP Methods (GET and POST)

This project introduces students to the **GET** and **POST** methods in FastAPI. It uses simple examples to explain how these methods work and how to handle request payloads. Testing is done using **Postman**.

## Key Features

1. **GET Method**: Fetch data from the server.
2. **POST Method**: Send data to the server.
3. Explanation of how to define request bodies and specify required parameters.

## Code Explanation

### Importing Required Modules

```python
from fastapi import FastAPI
from fastapi.params import Body
```

- `FastAPI`: Framework for building APIs.
- `Body`: Used to define request body parameters.

### Defining the FastAPI Application

```python
app = FastAPI()
```

- Creates an instance of the FastAPI application.

### Root Endpoint (`GET /`)

```python
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

- A basic endpoint that returns a welcome message to verify the application is running.

### Fetch Posts (`GET /posts`)

```python
@app.get("/posts")
async def get_posts():
    return {"message": "this is your first post"}
```

- Demonstrates the **GET** method.
- This endpoint retrieves a simple message.

### Create Post (`POST /createpost`)

```python
@app.post("/createpost")
async def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": f"{payload}"}
```

#### Explanation of the Code

- **Endpoint**: `/createpost`
- **HTTP Method**: POST
- **Request Parameter**: `payload`
  - **Type**: `dict` (A dictionary is expected as the input.)
  - **Body(...)**: 
    - Specifies that the parameter should come from the request body.
    - The `...` indicates that this parameter is required (equivalent to `required=True`).
- **Functionality**:
  - Logs the incoming payload to the console using `print()`.
  - Returns the payload as a response.

#### Example Usage in Postman

1. **Request**:
   - **Method**: POST
   - **URL**: `http://127.0.0.1:8000/createpost`
   - **Body (JSON)**:
     ```json
     {
         "title": "FastAPI Basics",
         "content": "Understanding GET and POST"
     }
     ```

2. **Response**:
   ```json
   {
       "message": {
           "title": "FastAPI Basics",
           "content": "Understanding GET and POST"
       }
   }
   ```

### Testing the Application

- Install dependencies:
  ```bash
  pip install fastapi uvicorn
  ```
- Run the application:
  ```bash
  uvicorn main:app --reload
  ```
- Test endpoints using **Postman** or visit `http://127.0.0.1:8000/docs`.

## Key Takeaways

1. **GET Method**: Used to retrieve data from the server.
2. **POST Method**: Used to send data to the server.
3. **Body(...)**:
   - Specifies that a parameter should come from the request body.
   - `...` indicates that the parameter is required.
4. **Postman**: A powerful tool to test API endpoints.

---
