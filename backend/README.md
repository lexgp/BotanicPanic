## Requirements
- Python >= 3.9

## Пример запуска проекта (в корне)

1. Установить зависимости:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

2. Инициализировать alembic:
```bash
# alembic init alembic

PYTHONPATH=. alembic revision --autogenerate -m "init"
PYTHONPATH=. alembic upgrade head
```
3. Запустить сервер:
`uvicorn app.main:app --reload`

