## Пример запуска проекта (в корне)

1. Установить зависимости:
`pip install -r requirements.txt`

2. Инициализировать alembic:
```
alembic revision --autogenerate -m "init"
alembic upgrade head
```
3. Запустить сервер:
`uvicorn app.main:app --reload`

