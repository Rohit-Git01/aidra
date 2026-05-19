from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from backend.db_config import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    
    full_name = Column(String(100), nullable=False)

    gender = Column(String(10))

    age = Column(Integer)

    city = Column(String(50))

    state = Column(String(50))

    phone_number = Column(String(20))

    email = Column(String(100))

    occupation = Column(String(50))

    annual_income = Column(DECIMAL(12, 2))

    customer_status = Column(String(20), nullable=False)

    created_date = Column(TIMESTAMP, nullable=False)