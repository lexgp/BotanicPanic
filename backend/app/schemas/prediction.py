from pydantic import BaseModel
from app.models import AlgorithmEnum
from typing import Optional
from typing import Tuple
from typing import List
from app.services.s3_service import S3Service
from app.models import Prediction


class ModelOpinion(BaseModel):
    disease: str
    confidence: float
    box: Tuple[int, int, int, int]  # x1, y1, x2, y2
    model_name: str
    class Config:
        orm_mode = True


class ModelOpinionOut(BaseModel):
    disease: str
    confidence: float
    box: Tuple[int, int, int, int]
    model_name: str

    model_config = {
        "from_attributes": True
    }

class PredictionOut(BaseModel):
    id: int
    received_photo: str
    marked_photo: Optional[str]
    avg_confidence: float
    sectors_count: int
    opinions: List[ModelOpinionOut]

    @classmethod
    def from_orm_with_signed_urls(cls, obj: Prediction) -> "PredictionOut":
        s3_service = S3Service()
        return cls(
            id=obj.id,
            received_photo=s3_service.get_presigned_url(obj.received_photo),
            marked_photo=s3_service.get_presigned_url(obj.marked_photo) if obj.marked_photo else None,
            avg_confidence=obj.avg_confidence,
            sectors_count=obj.sectors_count,
            opinions=[ModelOpinionOut.model_validate(op) for op in obj.opinions],
        )

    model_config = {
        "from_attributes": True
    }