from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import MlModel

router = APIRouter()

@router.get("/models/")
async def list_models(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(MlModel))
    return result.scalars().all()
