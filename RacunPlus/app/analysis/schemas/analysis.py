from datetime import date, datetime
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


AnalysisType = Literal["monthly", "category"]


class AnalysisGenerateRequest(BaseModel):
    analysis_type: AnalysisType
    days: int = Field(default=30, ge=1, le=365)


class MonthlyBreakdownItem(BaseModel):
    provider: str
    category: str
    amount: float


class MonthlyInsights(BaseModel):
    summary: str
    total_amount: float
    breakdown: List[MonthlyBreakdownItem]
    recommendations: List[str]


class CategoryItem(BaseModel):
    name: str
    total_amount: float
    percentage: float
    insight: str


class CategoryInsights(BaseModel):
    summary: str
    categories: List[CategoryItem]
    recommendations: List[str]


InsightsUnion = Union[MonthlyInsights, CategoryInsights]


class AnalysisResponseData(BaseModel):
    analysis_id: str
    analysis_type: AnalysisType
    period_start: date
    period_end: date
    total_amount: float
    bills_count: int
    insights: Dict[str, Any]
    created_at: datetime


class SuccessResponse(BaseModel):
    success: bool = True
    data: Any


class HistoryResponseData(BaseModel):
    analyses: List[AnalysisResponseData]
    total: int


class HistoryResponse(BaseModel):
    success: bool = True
    data: HistoryResponseData


class AnalysisORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: int
    analysis_type: str
    period_start: date
    period_end: date
    total_amount: float
    bills_count: int
    prompt: str
    ai_response: Dict[str, Any]
    model_used: str
    tokens_used: Optional[int] = None
    status: str
    error_message: Optional[str] = None
    created_at: datetime
