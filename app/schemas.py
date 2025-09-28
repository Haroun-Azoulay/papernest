from pydantic import BaseModel


class ResponseAPI(BaseModel):
    message: str


class JobCreate(BaseModel):
    address: str
