from sqlalchemy import Column, String, DateTime, Integer, Boolean, func
from uuid import uuid4
from app.database import Base


class JobResponse(Base):
    __tablename__ = "job_responses"

    uuid = Column(
        String(36), primary_key=True, default=lambda: str(uuid4()), index=True
    )
    timestamp_in = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    timestamp_out = Column(DateTime(timezone=True), nullable=True)
    duration = Column(String(12), nullable=False)
    query = Column(Integer, nullable=False)
    state = Column(Boolean, nullable=False, default=False)
