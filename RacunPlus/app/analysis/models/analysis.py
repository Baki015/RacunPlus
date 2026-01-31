import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Float, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from RacunPlus.database import Base

class Analysis(Base):
    __tablename__ = 'analysis'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    analysis_type = Column(String, nullable=False)

    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_amount = Column(Float, nullable=False)
    bills_count = Column(Integer, nullable=False)

    prompt = Column(Text, nullable=False)
    ai_response = Column(JSONB, nullable=False)

    model_used = Column(String, default="gemini-1.5-flash", nullable=False)
    tokens_used = Column(Integer, nullable=True)
    status = Column(String, default="completed", nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
