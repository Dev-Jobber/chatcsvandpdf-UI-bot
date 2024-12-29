import time
from fastapi import FastAPI, HTTPException, Request
import app as llm_service # Assuming `app.llm_generator(query)` is defined in this module
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# set cors policy

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/ping')
def ping():
    return {"message": "pong"}


EXPECTED_BEARER_TOKEN = "1234"

@app.get('/chat/{query}')
async def test(query: str, request: Request):
    # Extract the Authorization header
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # Check if the token starts with 'Bearer ' and then get the token
    token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else None

    if token != EXPECTED_BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    start_time = time.time()  # Start the timer

    response = llm_service.llm_generator(query)  # Your LLM generation logic

    end_time = time.time()  # End the timer
    duration = end_time - start_time  # Calculate how much time it took

    return {
        "query": query,
        "response": response,
        "time_taken_seconds": duration
    }
