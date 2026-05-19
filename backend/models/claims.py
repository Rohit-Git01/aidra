from sqlalchemy import Column, Integer, String, DECIMAL, DATE, Boolean, ForeignKey
from backend.db_config import Base


class Claim(Base):
    __tablename__ = "claims"

    claim_id = Column(Integer, primary_key=True)

    policy_id = Column(Integer, ForeignKey("policies.policy_id"), nullable=False)

    claim_amount = Column(DECIMAL(12, 2), nullable=False)

    settlement_amount = Column(DECIMAL(12, 2))

    claim_reason = Column(String(255))

    claim_status = Column(String(20), nullable=False)

    claim_date = Column(DATE, nullable=False)

    settlement_date = Column(DATE)

    fraud_flag = Column(Boolean, nullable=False)
