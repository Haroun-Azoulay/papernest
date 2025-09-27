from fastapi import FastAPI, status
from uuid import UUID, uuid4
from app import schemas

app = FastAPI()

# app.include_router(routes.router)


@app.get(
    "/ping",
    response_model=schemas.ResponseAPI,
    status_code=status.HTTP_200_OK,
    tags=["Monitoring"],
    summary="Health check",
    description="Check if the API is alive.",
    responses={
        status.HTTP_200_OK: {"model": schemas.ResponseAPI},
    },
)
def ping() -> schemas.ResponseAPI:
    """Check that the API is alive"""
    return schemas.ResponseAPI(message="pong")
