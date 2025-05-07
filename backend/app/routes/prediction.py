import os
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Prediction
from app.schemas.prediction import PredictionOut
from app.utils.image_utils import resize_image, save_to_media, get_file_s3name
from app.services.prediction_service import create_prediction_from_opinions
from app.services.prediction_service import run_prediction
import boto3
from boto3 import client as S3Client
from dotenv import load_dotenv
load_dotenv()

YANDEX_ACCESS_KEY_ID = os.getenv("YANDEX_ACCESS_KEY_ID")
YANDEX_SECRET_ACCESS_KEY = os.getenv("YANDEX_SECRET_ACCESS_KEY")
YANDEX_ENDPOINT = os.getenv("YANDEX_ENDPOINT")
BUCKET_NAME = os.getenv("BUCKET_NAME")

s3_client = S3Client(
    's3',
    endpoint_url=YANDEX_ENDPOINT,
    aws_access_key_id=YANDEX_ACCESS_KEY_ID,
    aws_secret_access_key=YANDEX_SECRET_ACCESS_KEY,
    region_name='ru-central1'
)

router = APIRouter()

@router.post("/predict/", response_model=PredictionOut)
async def predict(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    if not file:
        raise HTTPException(status_code=400, detail="Файл не загружен")
    
    # TODO: наверное вынести работу с файлами в утилиты
    object_name = get_file_s3name(file)
    presigned_url = None
    try:
        # Загружаем файл в бакет
        s3_client.upload_fileobj(file.file, BUCKET_NAME, object_name)
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при загрузке файла: {str(e)}")
    
    opinions = await run_prediction(presigned_url, session)
    prediction = create_prediction_from_opinions(opinions, presigned_url)
    session.add(prediction)
    await session.commit()
    await session.refresh(prediction)
    return prediction
