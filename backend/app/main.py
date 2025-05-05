from fastapi import FastAPI
from app.routes import mlmodels
from app.routes import prediction
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(mlmodels.router)
app.include_router(prediction.router)
app.mount("/media", StaticFiles(directory="media"), name="media")
