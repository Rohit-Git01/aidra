from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:aidra123@localhost:5432/aidra"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        print("AIDRA database connected successfully!")
except Exception as e:
    print("Connection failed:", e)
    