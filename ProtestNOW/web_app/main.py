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

import subprocess

@app.post("/start-agent")
async def start_agent():
    # Path to the virtual environment python
    root_dir = os.path.dirname(BASE_DIR)
    python_path = os.path.join(root_dir, "venv/bin/python3")
    script_path = os.path.join(root_dir, "crewAI/protest_tracker.py")

    try:
        # Run the crewAI agent script
        # Note: This will block the FastAPI worker for the duration of the search
        result = subprocess.run(
            [python_path, script_path],
            capture_output=True,
            text=True,
            cwd=root_dir
        )
        
        if result.returncode == 0:
            # Save results for NotebookLM phase
            results_file = os.path.join(root_dir, "research_results.md")
            with open(results_file, "w") as f:
                f.write(result.stdout)
                
            return {
                "status": "success", 
                "message": "Research data captured. Finalizing infographic...",
                "output_file": "research_results.md"
            }
        else:
            return {
                "status": "error", 
                "message": "Agent workflow failed.",
                "error": result.stderr
            }
            
    except Exception as e:
        return {"status": "error", "message": f"Execution error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
