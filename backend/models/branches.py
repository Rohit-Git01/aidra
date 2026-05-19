from sqlalchemy import Column, Integer, String
from backend.db_config import Base


class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(Integer, primary_key=True)

    branch_name = Column(String(100), nullable=False)

    city = Column(String(50), nullable=False)

    state = Column(String(50), nullable=False)

    region = Column(String(50), nullable=False)

    manager_name = Column(String(100))

    branch_status = Column(String(20), nullable=False)