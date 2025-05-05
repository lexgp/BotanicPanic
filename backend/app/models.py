from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from app.database import Base
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
    infection_id: Mapped[int] = mapped_column(ForeignKey("infection.id"))
    infection: Mapped["Infection"] = relationship(backref="models")
    algorithm: Mapped[AlgorithmEnum]
    accuracy: Mapped[float]
    f1_score: Mapped[float]
    recall: Mapped[float]
    prediction: Mapped[str]

class Prediction(Base):
    __tablename__ = "prediction"
    id: Mapped[int] = mapped_column(primary_key=True)
    ml_model_id: Mapped[int] = mapped_column(ForeignKey("ml_model.id"))
    ml_model: Mapped["MlModel"] = relationship(backref="predictions")
    received_photo: Mapped[str]
    marked_photo: Mapped[str]
    probability: Mapped[float]
    coord: Mapped[str]
    sectors_count: Mapped[int]
