import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(dotenv_path="../.env")

app = FastAPI()

# Base directory relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(BASE_DIR, "static/index.html"))

@app.post("/start-agent")
async def start_agent():
    # Simulate agent process (e.g., search, data sorting, infographic trigger)
    await asyncio.sleep(2) # Fake "Initializing" delay
    
    # In a real scenario, this could trigger the crewAI script or a subprocess
    return {"status": "success", "message": "Agent workflow initiated."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
