from abc import ABC, abstractmethod
from typing import List
from app.schemas.prediction import ModelOpinion
from app.models import MlModel

class Provider(ABC):

    def __init__(self, model: MlModel):
        self.model = model

    @abstractmethod
    async def predict(self, image_path: str) -> List[ModelOpinion]:
        pass
