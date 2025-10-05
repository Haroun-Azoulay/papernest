from fastapi import FastAPI, status, Response
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID, uuid4
from app import schemas, routes, models
from app.database import engine, Base
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    # Url for the frontend without docker
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(routes.router)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


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
