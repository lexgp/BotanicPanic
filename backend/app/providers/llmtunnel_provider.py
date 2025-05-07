import re
import time
import json
from openai import OpenAI
from app.providers.base import Provider
from app.models import MlModel
from typing import Union
from app.schemas.prediction import ModelOpinion
from typing import List

class LLMProvider(Provider):

    MAX_TOKENS = 50000

    def __init__(self, model: MlModel):
        self.model = model

    async def predict(self, image_url: str):
        client = OpenAI(
            api_key=self.model.provider_secret_key,
            base_url=self.model.provider_url,
        )
        
        photo_result = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """А на этом фото есть признаки заболеваний растения? Каких? С какой вероятностью?
Ответ выдай массивом в формате json вида:
[
    {
        disease: str,
        confidence: float,
        rect_x1: int,
        rect_y1: int,
        rect_x2: int,
        rect_y2: int
    },
    ... ещё если есть...
]
Если заболеваний не найдено, то массив будет пустым [].
disease - название предполагаемой болезни на русском языке. confidence - уровень уверенности.
rect_x1, rect_y1, rect_x2, rect_y2 - координаты диагонали прямоугольника, в которой ты видишь заражение, учитывай при расчёте размер предоставленного фото, и старайся чтобы в прямоугольник попадало всё заражение, но при этом его размер был минимально достаточным.
Не надо давать больше никаких текстовых пояснений, только чистая json."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": "auto"
                        }}
                ]
            }],
            model=self.model.provider_submodel,
            max_tokens=LLMProvider.MAX_TOKENS,
        )
        # В прошлый раз с этой api были баги, если не поставить задержку
        # TODO: разобраться в чём была проблема
        time.sleep(0.1)
        results = []
        try:
            response_message = photo_result.choices[0].message.content
            print('response_message', response_message)
            results = LLMProvider.extract_json_from_llm_output(response_message)
            if not isinstance(results, list):
                raise ValueError("Ожидался массив результатов")
        except Exception as e:
            print(f"Ошибка при выполнении запроса к GPT: {e}")

        return results

    @staticmethod
    def extract_json_from_llm_output(text: str) -> Union[dict, list]:
        try:
            # Попробуем найти JSON-блок в тексте
            json_str = re.search(r'({.*?}|\[.*?\])', text, re.DOTALL).group(1)
            return json.loads(json_str)
        except (AttributeError, json.JSONDecodeError):
            raise ValueError("Не удалось извлечь корректный JSON из ответа модели.")