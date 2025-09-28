from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from app import schemas
router = APIRouter()

# Redis memory
JOBS = {}

@router.post("/job-submission", tags=["Job"])
async def create_job(job: schemas.JobCreate): 
    

    data = {
        "id": job.address
    }

    return job

