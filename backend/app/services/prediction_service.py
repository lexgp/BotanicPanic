from app.models import MlModel
from app.database import get_async_session
from fastapi import Depends
from sqlalchemy import select

from app.providers.llmtunnel_provider import LLMProvider
from app.providers.yolov8_provider import YOLOv8Provider
from app.schemas.prediction import ModelOpinion
from typing import List

from app.providers.registry import PROVIDER_REGISTRY
from app.enums.provider_type import ProviderType
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Prediction
from typing import List
from statistics import mean

async def run_prediction(resized_image_path: str, session: AsyncSession) -> List[ModelOpinion]:

    models = await session.execute(select(MlModel))
    # models = mlmodel_query.scalars().all()

    all_opinions: List[ModelOpinion] = []
    for model in models.scalars():
        provider_class = PROVIDER_REGISTRY[ProviderType(model.provider_type)]
        provider = provider_class(model=model)
        raw_opinions = await provider.predict(resized_image_path)
        opinions: List[ModelOpinion] = [
            ModelOpinion(
                disease=op["disease"],
                confidence=op["confidence"],
                box=(op["rect_x1"], op["rect_y1"], op["rect_x2"], op["rect_y2"]),
                model_name=model.name
            )
            for op in raw_opinions
        ]
        all_opinions.extend(opinions)

    return all_opinions

def create_prediction_from_opinions(opinions: List[ModelOpinion], resized_path: str) -> Prediction:
    avg_conf = mean(op.confidence for op in opinions) if opinions else 0.0
    sectors = len(opinions)

    prediction = Prediction(
        received_photo=resized_path,
        marked_photo=resized_path,
        avg_confidence=avg_conf,
        sectors_count=sectors
    )
    return prediction