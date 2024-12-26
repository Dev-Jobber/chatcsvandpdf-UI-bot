import time
from fastapi import FastAPI
import app as llm_service # Assuming `app.llm_generator(query)` is defined in this module

app = FastAPI()

@app.get('/chat/{query}')
def test(query: str):
    start_time = time.time()  # Start the timer

    response = llm_service.llm_generator(query)  # Your LLM generation logic

    end_time = time.time()  # End the timer
    duration = end_time - start_time  # Calculate how much time it took

    return {
        "query": query,
        "response": response,
        "time_taken_seconds": duration
    }
