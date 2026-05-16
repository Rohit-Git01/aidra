project name : AIDRA

day 1 :
 installed python and postgresql-- created database in postgre and tried connecting python and database using sqlalchemy

DB_URL = "postgresql://postgres:aidra123@localhost:5432/aidra"

engine = create_engine(DB_URL)

used create_engine from sqlalchemy and gave the above DB_URL, engine.connect() as conn