import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Prediction
from app.schemas.prediction import PredictionOut
from app.utils.image_utils import resize_image, save_to_media
from app.services.prediction_service import create_prediction_from_opinions
from app.services.prediction_service import run_prediction

router = APIRouter()

@router.post("/predict/", response_model=PredictionOut)
async def predict(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    saved_path = save_to_media(file, 'prediction_in')
    resized_path = resize_image(saved_path)
    opinions = await run_prediction(resized_path, session)
    prediction = create_prediction_from_opinions(opinions, str(Path(resized_path)))
    session.add(prediction)
    await session.commit()
    await session.refresh(prediction)
    return prediction
