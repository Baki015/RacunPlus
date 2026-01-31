from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from RacunPlus.database import Base

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    merchant_name = Column(String, nullable=False)
    transaction_date = Column(Date, nullable=False)
    status = Column(String, default="Not_completed")

