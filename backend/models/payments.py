from sqlalchemy import Column, Integer, String, DECIMAL, DATE, ForeignKey
from backend.db_config import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True)

    policy_id = Column(Integer, ForeignKey("policies.policy_id"), nullable=False)

    payment_amount = Column(DECIMAL(12, 2), nullable=False)

    payment_date = Column(DATE, nullable=False)

    payment_method = Column(String(50), nullable=False)

    payment_status = Column(String(20), nullable=False)
