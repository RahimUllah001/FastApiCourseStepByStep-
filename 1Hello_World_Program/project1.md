# FastAPI Hello World Application Documentation

## Overview
This is a simple FastAPI application that implements a basic "Hello World" endpoint. The application serves as an introduction to FastAPI framework and demonstrates its basic setup and usage.

## Prerequisites
- Python 3.6+
- FastAPI
- Uvicorn (ASGI server)

## Installation
1. First, create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install fastapi uvicorn
   ```

## Code Explanation
```python
from fastapi import FastAPI

app = FastAPI()     # Create FastAPI instance

@app.get("/")       # Route decorator for root endpoint
async def root():   # Async function for handling requests
    return {"message": "Hello World"}
```

### Code Breakdown:
* `from fastapi import FastAPI`: Imports the FastAPI class
* `app = FastAPI()`: Creates an instance of the FastAPI application
* `@app.get("/")`: Decorator that creates a route for GET requests to the root path
* `async def root()`: Asynchronous function that handles the request
* `return {"message": "Hello World"}`: Returns a JSON response

## Running the Application
1. Save the code in a file (e.g., `main.py`)
2. Run the server using uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

## Testing the API
Once the server is running, you can test the API in several ways:

1. **Web Browser**:
   - Visit `http://localhost:8000`

2. **cURL**:
   ```bash
   curl http://localhost:8000
   ```

3. **Interactive API Documentation**:
   - Swagger UI: Visit `http://localhost:8000/docs`
   - ReDoc: Visit `http://localhost:8000/redoc`

## Expected Response
```json
{
    "message": "Hello World"
}
```


## Resources
* [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
* [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi)