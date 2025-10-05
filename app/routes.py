from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, services, database
from uuid import uuid4
import httpx
from sqlalchemy.orm import sessionmaker, Session
import datetime
import json
from app.models import JobResponse as JobRow
from app.metrics import (
    job_duration_seconds,
    job_requests_total,
    job_items_processed_total,
)


router = APIRouter()

# Redis memory
JOBS = {}


@router.post(
    "/job-submission",
    tags=["Job"],
    status_code=status.HTTP_200_OK,
    summary="Create Job",
    description="Check if the cover is present on the address.",
    responses={
        status.HTTP_200_OK: {"model": schemas.JobResponse},
    },
)
async def create_job(
    addresses: schemas.AddressesIn,
    db: Session = Depends(database.get_db),
):
    job_id = uuid4()
    results: dict[str, dict] = {}
    timeIn = datetime.datetime.now()
    query = len(addresses.root)
    state = False

    try:
        for idaddress, address in addresses.root.items():
            response = await services.fetch_geocode(address)
            dataCoords = services.parsing_coords_gouv(response)
            dataMobileCoverage = services.read_csv(dataCoords[0], dataCoords[1])
            results[idaddress] = dataMobileCoverage
        state = True
        return schemas.JobResponse(jobsUUID=job_id, jobs=results)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error network: {e}.")
    finally:
        timeOut = datetime.datetime.now()
        deltaInOut = timeOut - timeIn
        totalMs = int(deltaInOut.total_seconds() * 1000)
        h, m, s, ms = services.convert_ms(totalMs)
        db_data = JobRow(
            uuid=str(job_id),
            timestamp_in=timeIn,
            timestamp_out=timeOut,
            duration=f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}",
            query=query,
            state=state,
        )
        db.add(db_data)
        job_duration_seconds.observe(totalMs / 1000.0)
        job_requests_total.labels(result="ok" if state else "error").inc()
        if query:
            job_items_processed_total.inc(query)
        db.commit()
        db.refresh(db_data)
