from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Prediction
from app.schemas import PredictionOut
import uuid
import os

router = APIRouter()

@router.post("/predict/", response_model=PredictionOut)
async def predict(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    filename = f"media/{uuid.uuid4()}.jpg"
    with open(filename, "wb") as f:
        f.write(await file.read())

    # Заглушка под YOLO
    result = {
        "model_id": 1,
        "marked_path": filename,
        "prob": 0.95,
        "coord": "x1,y1,x2,y2",
        "sectors": 5
    }

    prediction = Prediction(
        ml_model_id=result["model_id"],
        received_photo=filename,
        marked_photo=result["marked_path"],
        probability=result["prob"],
        coord=result["coord"],
        sectors_count=result["sectors"]
    )
    session.add(prediction)
    await session.commit()
    await session.refresh(prediction)
    return prediction
