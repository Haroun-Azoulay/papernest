from pydantic import BaseModel


class ResponseAPI(BaseModel):
    message: str
