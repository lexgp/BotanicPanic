from app.database import get_async_session
from app.models import Prediction, ModelOpinion
from app.schemas.prediction import PredictionOut
from app.utils.image_utils import resize_image, save_to_media, get_file_s3name, get_image_size
from app.services.prediction_service import create_prediction_from_opinions
from app.services.prediction_service import run_prediction
from app.services.prediction_service import prediction_preview
from app.services.s3_service import S3Service
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

router = APIRouter()

@router.post("/predict/", response_model=PredictionOut)
async def predict(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    if not file:
        raise HTTPException(status_code=400, detail="Файл не загружен")
    
    image_size = get_image_size(file.file)
    s3_service = S3Service()
    prediction_in_name = get_file_s3name(file)
    prediction_in_url = await s3_service.upload_file(file.file, prediction_in_name)
    opinions = await run_prediction(prediction_in_url, image_size, session)
    prediction_out_file = await prediction_preview(prediction_in_url, opinions)
    prediction_out_name = prediction_in_name.replace(".", "_predicted.")
    await s3_service.upload_file(prediction_out_file, prediction_out_name)
    prediction = create_prediction_from_opinions(opinions, prediction_in_name, prediction_out_name)
    session.add(prediction)
    await session.flush()

    opinion_models = [
        ModelOpinion(
            prediction_id=prediction.id,
            disease=op.disease,
            confidence=op.confidence,
            box_x1=op.box[0],
            box_y1=op.box[1],
            box_x2=op.box[2],
            box_y2=op.box[3],
            model_name=op.model_name,
        )
        for op in opinions
    ]
    session.add_all(opinion_models)
    await session.commit()
    await session.refresh(prediction)

    return PredictionOut.from_orm_with_signed_urls(prediction)


@router.get("/predictions/", response_model=List[PredictionOut])
async def get_predictions(
    limit: int = Query(12, le=100),
    offset: int = Query(0),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(Prediction).order_by(Prediction.id.desc()).limit(limit).offset(offset)
    )
    predictions = result.scalars().all()
    return [PredictionOut.from_orm_with_signed_urls(p) for p in predictions]
