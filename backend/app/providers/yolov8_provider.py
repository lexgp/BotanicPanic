from app.providers.base import Provider
from app.models import MlModel

class YOLOv8Provider(Provider):
    def __init__(self, model: MlModel):
        self.model = model

    async def predict(self, image_path: str):
        ...