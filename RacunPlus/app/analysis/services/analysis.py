from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from RacunPlus.settings import settings
from RacunPlus.app.analysis.models.analysis import Analysis
from RacunPlus.app.analysis.services.ai_service import GeminiAIService
from RacunPlus.app.analysis.services.data_aggregator import fetch_user_bills
from RacunPlus.app.analysis.exceptions.analysis import RateLimitExceededError, NoBillsFoundError


def count_user_analyses_today(db: Session, user_id: str) -> int:
    today = date.today()
    count = db.query(func.count(Analysis.id)).filter(
        Analysis.user_id == user_id,
        func.date(Analysis.created_at) == today,
        Analysis.status == "completed"
    ).scalar()
    return count or 0


def generate_analysis(
    db: Session,
    user_id: str,
    analysis_type: str,
    days: int,
):
    today_count = count_user_analyses_today(db, user_id)
    if today_count >= settings.ANALYSIS_RATE_LIMIT:
        raise RateLimitExceededError("Daily analysis limit reached")

    bills, start, end = fetch_user_bills(db, user_id, days)

    if not bills:
        raise NoBillsFoundError("No bills found for this period")

    total_amount = sum(b['amount'] for b in bills)

    ai = GeminiAIService()
    
    if analysis_type == "monthly":
        ai_response = ai.generate_monthly_analysis(bills)
    elif analysis_type == "category":
        ai_response = ai.generate_category_analysis(bills)
    else:
        raise HTTPException(status_code=400, detail="Invalid analysis type")

    analysis = Analysis(
        user_id=user_id,
        analysis_type=analysis_type,
        period_start=start,
        period_end=end,
        total_amount=total_amount,
        bills_count=len(bills),
        prompt="",
        ai_response=ai_response,
        status="completed"
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def analysis_to_response(analysis: Analysis) -> dict:
    return {
        "analysis_id": str(analysis.id),
        "analysis_type": analysis.analysis_type,
        "period_start": analysis.period_start.isoformat(),
        "period_end": analysis.period_end.isoformat(),
        "total_amount": analysis.total_amount,
        "bills_count": analysis.bills_count,
        "insights": analysis.ai_response,
        "created_at": analysis.created_at.isoformat(),
    }
