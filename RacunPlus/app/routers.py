from fastapi import APIRouter
from RacunPlus.app.analysis.api.analysis import router as analysis_router
from RacunPlus.database import SessionLocal
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from RacunPlus.routers import get_db
from RacunPlus.security import get_current_user_id
from RacunPlus.app.analysis.schemas.analysis import AnalysisGenerateRequest
from RacunPlus.app.analysis.services.analysis import generate_analysis, analysis_to_response
from RacunPlus.app.analysis.database.analysis import get_latest_analysis,get_analysis_history,get_analysis_by_id,delete_analysis_by_id

from RacunPlus.app.analysis.exceptions.analysis import RateLimitExceededError, NoBillsFoundError

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate")
async def generate(
    payload: AnalysisGenerateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    try:
        data = await generate_analysis(db, user_id, payload.analysis_type, payload.days)
        return {"success": True, "data": data}
    except RateLimitExceededError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except NoBillsFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/latest")
async def latest(
    analysis_type: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    item = await get_latest_analysis(db, user_id, analysis_type)
    if not item:
        raise HTTPException(status_code=404, detail="No analysis found")
    return {"success": True, "data": analysis_to_response(item)}


@router.get("/history")
async def history(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    items, total = await get_analysis_history(db, user_id, limit, offset)
    return {
        "success": True,
        "data": {
            "analyses": [analysis_to_response(a) for a in items],
            "total": total,
        },
    }


@router.get("/{id}")
async def get_by_id(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    item = await get_analysis_by_id(db, user_id, id)
    if not item:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"success": True, "data": analysis_to_response(item)}


@router.delete("/{id}")
async def delete_by_id(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    ok = await delete_analysis_by_id(db, user_id, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"success": True, "data": {"deleted": True}}

