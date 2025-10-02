from fastapi import APIRouter, HTTPException, status
from app import schemas, services
from uuid import uuid4
import httpx

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
async def create_job(addresses: schemas.AddressesIn):
    data = addresses.root
    job_id = uuid4()
    try:
        for idAddress, address in addresses.root.items():
            response = await services.fetch_geocode(address)
            dataCoords = services.parsing_coords_gouv(response)
            dataMobileCoverage = services.read_csv(dataCoords[0], dataCoords[1])
            response = JOBS.setdefault(idAddress, {})
            response.update(dataMobileCoverage)
        return schemas.JobResponse(jobsUUID=job_id, jobs=JOBS)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error network: {e}.")
