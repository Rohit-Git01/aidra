from backend.db_config import engine, Base

from backend.models.customers import Customer
from backend.models.policies import Policy
from backend.models.claims import Claim
from backend.models.payments import Payment
from backend.models.agents import Agent
from backend.models.branches import Branch


print("Creating AIDRA database tables...")


Base.metadata.create_all(bind=engine)


print("All tables created successfully!")