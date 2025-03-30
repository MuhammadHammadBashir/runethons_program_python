
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import shutil
import os
from pathlib import Path
from typing import Optional


from performance_analysis_system import PerformanceAnalysisSystem  

app = FastAPI()

# Directory to store uploaded files temporarily
UPLOAD_DIR = Path("./asset/video_upload")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/analyze-performance/")
async def analyze_performance(
    video: UploadFile = File(...), 
    athlete_email: Optional[str] = Form(None),
    report_id: Optional[str] = Form(None)
):
    try:
        # Save uploaded video temporarily
        video_path = UPLOAD_DIR / video.filename
        with video_path.open("wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # Instantiate the PerformanceAnalysisSystem class
        performance_analysis_system = PerformanceAnalysisSystem()
        
        # Call the analyze function
        result = performance_analysis_system.analyze_performance(str(video_path), athlete_email, report_id)

        # Clean up: remove the temporary file
        # os.remove(video_path)

        return {"analyze_performance": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

