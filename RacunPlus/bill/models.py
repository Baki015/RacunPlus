from sqlalchemy import Column, String, Float, Date, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from RacunPlus.database import Base

class Bill(Base):
    __tablename__ = "bills"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    beneficiary_name = Column(String, nullable=False)
    reference_date = Column(Date, nullable=False)
    status = Column(String, default="paid", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now(), nullable=False)