from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from typing import Dict, Any
import shutil
import os
import uuid
import pandas as pd
from app.services.validation_engine import process_file, validate_dataframe
from app.schemas.validation import RuleConfig, ValidationResult, ValidationResultSummary

router = APIRouter()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# In-memory store for demo purposes (replace with DB for persistent metadata)
file_metadata = {}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate preview
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path, nrows=10)
        elif file.filename.endswith('.json'):
            df = pd.read_json(file_path) # JSON usually loaded fully, but let's try
            df = df.head(10)
        else:
            return {"error": "Unsupported file type"}
            
        preview = df.to_dict(orient='records')
        columns = list(df.columns)
        
        file_metadata[file_id] = {
            "filename": file.filename,
            "path": file_path,
            "columns": columns
        }
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "preview": preview,
            "columns": columns
        }
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate/{file_id}")
async def validate_data(file_id: str, config: RuleConfig):
    if file_id not in file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
        
    path = file_metadata[file_id]["path"]
    filename = file_metadata[file_id]["filename"]
    
    try:
        # Read full file
        with open(path, "rb") as f:
            content = f.read()
            df = process_file(content, filename)
            
        summary, sample_errors = validate_dataframe(df, config)
        
        run_id = str(uuid.uuid4())
        # Store results in memory for export (in real app, use DB)
        file_metadata[run_id] = {
            "type": "result",
            "summary": summary.dict(),
            "sample_errors": sample_errors,
            "original_file_id": file_id
        }
        
        return ValidationResult(
            run_id=run_id,
            summary=summary,
            sample_errors=sample_errors
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/{run_id}")
async def export_results(run_id: str, format: str = "json"):
    if run_id not in file_metadata:
         # Try to see if it is a file_id? No, spec says export validation reports.
         raise HTTPException(status_code=404, detail="Validation run not found")
    
    data = file_metadata[run_id]
    if data.get("type") != "result":
        raise HTTPException(status_code=400, detail="Not a validation run")

    if format == "json":
        return data
    elif format == "csv":
        # Create a simple CSV report
        # Summary rows + Errors
        summary = data["summary"]
        
        # We'll return the error rows as CSV for now
        errors = data["sample_errors"]
        output = io.StringIO()
        if errors:
            pd.DataFrame(errors).to_csv(output, index=False)
        else:
            output.write("No errors found.")
            
        output.seek(0)
        return fastapi.responses.StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=report_{run_id}.csv"}
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
        
import io
import fastapi.responses
