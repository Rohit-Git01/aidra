from sqlalchemy import Column, Integer, String, DECIMAL, DATE, TIMESTAMP, ForeignKey
from backend.db_config import Base


class Policy(Base):
    __tablename__ = "policies"

    policy_id = Column(Integer, primary_key=True)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)

    policy_type = Column(String(50), nullable=False)

    premium_amount = Column(DECIMAL(12, 2), nullable=False)

    coverage_amount = Column(DECIMAL(12, 2), nullable=False)

    policy_status = Column(String(20), nullable=False)

    start_date = Column(DATE, nullable=False)

    end_date = Column(DATE, nullable=False)

    agent_id = Column(Integer, ForeignKey("agents.agent_id"))

    created_date = Column(TIMESTAMP, nullable=False)
