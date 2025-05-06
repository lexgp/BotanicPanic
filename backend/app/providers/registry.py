from app.providers.llmtunnel_provider import LLMProvider
from app.providers.yolov8_provider import YOLOv8Provider
from app.enums.provider_type import ProviderType

PROVIDER_REGISTRY = {
    ProviderType.LLM: LLMProvider,
    ProviderType.YOLOv8: YOLOv8Provider,
}
