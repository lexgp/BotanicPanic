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

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from typing import Tuple


async def run_prediction(prediction_in_url: str, image_size: Tuple[int, int], session: AsyncSession) -> List[ModelOpinion]:

    models = await session.execute(select(MlModel))

    all_opinions: List[ModelOpinion] = []
    for model in models.scalars():
        provider_class = PROVIDER_REGISTRY[ProviderType(model.provider_type)]
        provider = provider_class(model=model)
        raw_opinions = await provider.predict(prediction_in_url, image_size)
        opinions: List[ModelOpinion] = [
            ModelOpinion(
                disease=op["disease"],
                confidence=op["confidence"],
                box=(
                    int(op["rect_x1"]),
                    int(op["rect_y1"]),
                    int(op["rect_x2"]),
                    int(op["rect_y2"])
                ),
                model_name=model.name
            )
            for op in raw_opinions
        ]
        all_opinions.extend(opinions)

    return all_opinions

def create_prediction_from_opinions(opinions: List[ModelOpinion], prediction_in_url: str, prediction_out_url: str) -> Prediction:
    avg_conf = mean(op.confidence for op in opinions) if opinions else 0.0
    sectors = len(opinions)

    prediction = Prediction(
        received_photo=prediction_in_url,
        marked_photo=prediction_out_url,
        avg_confidence=avg_conf,
        sectors_count=sectors
    )
    return prediction

async def prediction_preview(prediction_in_url: str, opinions: list) -> tuple[str, str]:
    COLORS = [
        (255, 0, 0, 255),      # красный
        (0, 255, 0, 255),      # зелёный
        (0, 0, 255, 255),      # синий
        (255, 255, 0, 255),    # жёлтый
        (255, 0, 255, 255),    # пурпурный
        (0, 255, 255, 255),    # голубой
        (255, 165, 0, 255),    # оранжевый
        (128, 0, 128, 255),    # фиолетовый
        (0, 128, 128, 255),    # бирюзовый
        (128, 128, 0, 255)     # оливковый
    ]

    # Скачиваем исходное изображение
    response = requests.get(prediction_in_url)
    image = Image.open(BytesIO(response.content)).convert("RGBA")

    # Рисуем прозрачные прямоугольники
    overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("fonts/DejaVuSans.ttf", size=32)
    except:
        font = ImageFont.load_default()

    # Получаем размер картинки
    width, height = image.size
    
    for i, op in enumerate(opinions):
        x1, y1, x2, y2 = op.box
        # Урезаем координаты в пределах изображения
        x1 = max(0, min(x1, width - 1))
        x2 = max(0, min(x2, width - 1))
        y1 = max(0, min(y1, height - 1))
        y2 = max(0, min(y2, height - 1))

        # Упорядочиваем координаты, чтобы x1 <= x2, y1 <= y2
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        color = COLORS[i % len(COLORS)]
        draw.rectangle([x1, y1, x2, y2], outline=color, width=4)
        draw.text((x1 + 3, y1 + 3), op.disease, fill=color, font=font)

    # Объединяем с оригинальным изображением
    combined = Image.alpha_composite(image, overlay)

    # Сохраняем в буфер
    buffer = BytesIO()
    combined.convert("RGB").save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer
