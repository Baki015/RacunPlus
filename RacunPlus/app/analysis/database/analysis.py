from RacunPlus.app.analysis.models.analysis import Analysis
from datetime import date
from typing import Optional, List, Tuple
from uuid import UUID

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession



async def create_analysis(db: AsyncSession, analysis: Analysis) -> Analysis:
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def get_analysis_by_id(db: AsyncSession, user_id: int, analysis_id: UUID) -> Optional[Analysis]:
    stmt = select(Analysis).where(Analysis.user_id == user_id, Analysis.id == analysis_id)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def delete_analysis_by_id(db: AsyncSession, user_id: int, analysis_id: UUID) -> bool:
    stmt = delete(Analysis).where(Analysis.user_id == user_id, Analysis.id == analysis_id)
    res = await db.execute(stmt)
    await db.commit()
    return res.rowcount > 0


async def get_latest_analysis(
    db: AsyncSession,
    user_id: int,
    analysis_type: Optional[str] = None,
) -> Optional[Analysis]:
    stmt = select(Analysis).where(Analysis.user_id == user_id)
    if analysis_type:
        stmt = stmt.where(Analysis.analysis_type == analysis_type)
    stmt = stmt.order_by(Analysis.created_at.desc()).limit(1)

    res = await db.execute(stmt)
    return res.scalar_one_or_none()


async def get_analysis_history(
    db: AsyncSession,
    user_id: int,
    limit: int = 10,
    offset: int = 0,
) -> Tuple[List[Analysis], int]:
    base = select(Analysis).where(Analysis.user_id == user_id).order_by(Analysis.created_at.desc())
    count_stmt = select(func.count()).select_from(base.subquery())

    total = (await db.execute(count_stmt)).scalar_one()

    stmt = base.limit(limit).offset(offset)
    items = (await db.execute(stmt)).scalars().all()
    return items, total


async def count_user_analyses_today(db: AsyncSession, user_id: int) -> int:
    stmt = select(func.count()).where(Analysis.user_id == user_id,func.date(Analysis.created_at) == date.today())
    return (await db.execute(stmt)).scalar_one()
