from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, TIMESTAMP
from backend.db_config import Base


class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True)

    agent_name = Column(String(100), nullable=False)

    branch_id = Column(Integer, ForeignKey("branches.branch_id"))

    region = Column(String(50))

    commission_rate = Column(DECIMAL(5, 2))

    joining_date = Column(TIMESTAMP, nullable=False)

    agent_status = Column(String(20))
