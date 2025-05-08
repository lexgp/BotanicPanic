from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, ForeignKey, Enum, Integer, String
from app.database import Base
from app.enums.provider_type import ProviderType
import enum

class AlgorithmEnum(str, enum.Enum):
    YOLO = "YOLO"
    ResNet = "ResNet"
    EfficientNet = "EfficientNet"
    DenseNet = "DenseNet"
    MaskRCNN = "Mask R-CNN"
    DeepLab = "DeepLab"
    ViT = "ViT / Swin Transformer"
    Hybrid = "Hybrid CNN-Transformer"
    ImageNet = "ImageNet"
    UNet = "U-Net"

class PlantCulture(Base):
    __tablename__ = "plant_culture"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    photo: Mapped[str]

class Infection(Base):
    __tablename__ = "infection"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    plant_culture_id: Mapped[int] = mapped_column(ForeignKey("plant_culture.id"))
    plant_culture: Mapped["PlantCulture"] = relationship(backref="infections")
    photo: Mapped[str]

class MlModel(Base):
    __tablename__ = "ml_model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True, default='')
    provider_type: Mapped[str] = mapped_column(nullable=True, default=ProviderType.LLM)
    provider_url: Mapped[str] = mapped_column(nullable=True)
    provider_secret_key: Mapped[str] = mapped_column(nullable=True)
    provider_submodel: Mapped[str] = mapped_column(nullable=True)
    map50: Mapped[float] = mapped_column(nullable=True)
    accuracy: Mapped[float]
    f1_score: Mapped[float]
    recall: Mapped[float]
    prediction: Mapped[str]

class Prediction(Base):
    __tablename__ = "prediction"
    id: Mapped[int] = mapped_column(primary_key=True)
    received_photo: Mapped[str]
    marked_photo: Mapped[str]
    avg_confidence: Mapped[float] = mapped_column(nullable=True)
    sectors_count: Mapped[int]
    opinions = relationship(
        "ModelOpinion",
        back_populates="prediction",
        cascade="all, delete-orphan",
        lazy="selectin",  # 👈 важно
    )

class ModelOpinion(Base):
    __tablename__ = "model_opinions"

    id = mapped_column(Integer, primary_key=True)
    prediction_id = mapped_column(ForeignKey("prediction.id", ondelete="CASCADE"))
    disease = mapped_column(String)
    confidence = mapped_column(Float)
    box_x1 = mapped_column(Integer)
    box_y1 = mapped_column(Integer)
    box_x2 = mapped_column(Integer)
    box_y2 = mapped_column(Integer)
    model_name = mapped_column(String)

    prediction = relationship("Prediction", back_populates="opinions")

    @property
    def box(self):
        return [self.box_x1, self.box_y1, self.box_x2, self.box_y2]