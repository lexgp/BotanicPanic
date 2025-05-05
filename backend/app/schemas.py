from pydantic import BaseModel
from typing import Optional
from app.models import AlgorithmEnum

class PredictionOut(BaseModel):
    id: int
    received_photo: str
    marked_photo: str
    probability: float
    coord: str
    sectors_count: int
    class Config:
        orm_mode = True
