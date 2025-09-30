from pydantic import BaseModel, RootModel, Field
from typing import Dict
from uuid import UUID


class ResponseAPI(BaseModel):
    message: str


class AddressesIn(RootModel[Dict[str, str]]):
    pass


class Coverage(BaseModel):
    two_g: bool = Field(alias="2G")
    three_g: bool = Field(alias="3G")
    four_g: bool = Field(alias="4G")


class JobResponse(BaseModel):
    jobsUUID: UUID
    jobs: Dict[str, Dict[str, Coverage]]
