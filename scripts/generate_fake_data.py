from faker import Faker
import random
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.db_config import SessionLocal

from backend.models.branches import Branch
from backend.models.agents import Agent
from backend.models.customers import Customer
from backend.models.policies import Policy
from backend.models.payments import Payment
from backend.models.claims import Claim


fake = Faker()

def safe_str(value, max_length):
    return str(value)[:max_length] if value is not None else None


db = SessionLocal()


# -----------------------------
# GENERATE BRANCHES
# -----------------------------

regions = ["South", "North", "East", "West"]

branches = []

for i in range(1, 11):

    branch = Branch(
        branch_id=i,
        branch_name=f"{fake.city()} Insurance Branch",
        city=safe_str(fake.city(), 50),
        state=safe_str(fake.state(), 50),
        region=safe_str(random.choice(regions), 50),
        manager_name=safe_str(fake.name(), 100),
        branch_status=random.choice(["Active", "Active", "Active", "Inactive"])
    )

    branches.append(branch)

db.add_all(branches)
db.commit()

print("Branches inserted successfully!")


# -----------------------------
# GENERATE AGENTS
# -----------------------------

agents = []

for i in range(1, 51):

    agent = Agent(
        agent_id=i,
        agent_name=safe_str(fake.name(), 100),
        branch_id=random.randint(1, 10),
        region=safe_str(random.choice(regions), 50),
        commission_rate=round(random.uniform(2.0, 12.0), 2),
        joining_date=fake.date_between(start_date="-5y", end_date="today"),
        agent_status=safe_str(random.choice(["Active", "Active", "Inactive"]), 20)
    )

    agents.append(agent)

db.add_all(agents)
db.commit()

print("Agents inserted successfully!")


# -----------------------------
# GENERATE CUSTOMERS
# -----------------------------

occupations = [
    "Engineer",
    "Doctor",
    "Teacher",
    "Lawyer",
    "Business",
    "Driver",
    "Student",
    "Manager"
]

customers = []

for i in range(1, 1001):

    customer = Customer(
        customer_id=i,
        full_name=fake.name(),
        gender=random.choice(["Male", "Female"]),
        age=random.randint(18, 75),
        city=safe_str(fake.city(), 50),
        state=safe_str(fake.state(), 50),
        phone_number=safe_str(fake.phone_number(), 20),
        email=safe_str(fake.email(), 100),
        occupation=safe_str(random.choice(occupations), 50),
        annual_income=round(random.uniform(300000, 3000000), 2),
        customer_status=random.choice(
            ["Active", "Active", "Active", "Inactive"]
        ),
        created_date=fake.date_time_between(start_date="-3y", end_date="now")
    )

    customers.append(customer)

db.add_all(customers)
db.commit()

print("Customers inserted successfully!")


# -----------------------------
# GENERATE POLICIES
# -----------------------------

policy_types = [
    "Health",
    "Life",
    "Vehicle",
    "Home",
    "Travel"
]

policies = []

for i in range(1, 2001):

    premium = round(random.uniform(5000, 50000), 2)

    coverage = premium * random.randint(20, 200)

    start_date = fake.date_between(start_date="-3y", end_date="today")

    end_date = start_date + timedelta(days=365)

    policy = Policy(
        policy_id=i,
        customer_id=random.randint(1, 1000),
        policy_type=random.choice(policy_types),
        premium_amount=premium,
        coverage_amount=coverage,
        policy_status=random.choice(
            ["Active", "Active", "Active", "Expired", "Cancelled"]
        ),
        start_date=start_date,
        end_date=end_date,
        agent_id=random.randint(1, 50),
        created_date=fake.date_time_between(start_date="-3y", end_date="now")
    )

    policies.append(policy)

db.add_all(policies)
db.commit()

print("Policies inserted successfully!")


# -----------------------------
# GENERATE PAYMENTS
# -----------------------------

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash"
]

payments = []

for i in range(1, 5001):

    payment = Payment(
        payment_id=i,
        policy_id=random.randint(1, 2000),
        payment_amount=round(random.uniform(2000, 50000), 2),
        payment_date=fake.date_between(start_date="-2y", end_date="today"),
        payment_method=random.choice(payment_methods),
        payment_status=random.choice(
            ["Success", "Success", "Success", "Pending", "Failed"]
        )
    )

    payments.append(payment)

db.add_all(payments)
db.commit()

print("Payments inserted successfully!")


# -----------------------------
# GENERATE CLAIMS
# -----------------------------

claim_reasons = [
    "Accident",
    "Medical Emergency",
    "Natural Disaster",
    "Fire Damage",
    "Vehicle Theft",
    "Hospitalization"
]

claims = []

for i in range(1, 1001):

    claim_amount = round(random.uniform(10000, 1000000), 2)

    settlement_amount = claim_amount * random.uniform(0.5, 1.0)

    claim_date = fake.date_between(start_date="-2y", end_date="today")

    settlement_date = claim_date + timedelta(days=random.randint(5, 60))

    claim = Claim(
        claim_id=i,
        policy_id=random.randint(1, 2000),
        claim_amount=claim_amount,
        settlement_amount=round(settlement_amount, 2),
        claim_reason=random.choice(claim_reasons),
        claim_status=random.choice(
            ["Approved", "Approved", "Approved", "Pending", "Rejected"]
        ),
        claim_date=claim_date,
        settlement_date=settlement_date,
        fraud_flag=random.choice(
            [False, False, False, False, False, False, False, False, True]
        )
    )

    claims.append(claim)

db.add_all(claims)
db.commit()

print("Claims inserted successfully!")

db.close()


print("\nAIDRA synthetic insurance dataset generated successfully!")