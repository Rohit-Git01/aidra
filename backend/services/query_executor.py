import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import pandas as pd


# ----------------------------------------
# PROJECT ROOT PATH FIX
# ----------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ----------------------------------------
# IMPORT DATABASE ENGINE
# ----------------------------------------

from backend.db_config import engine


# ----------------------------------------
# CREATE DATABASE SESSION
# ----------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ----------------------------------------
# EXECUTE SQL QUERY
# ----------------------------------------

def execute_query(sql_query):

    db = SessionLocal()

    try:

        result = db.execute(
            text(sql_query)
        )

        rows = result.fetchall()

        columns = result.keys()

        formatted_results = []

        for row in rows:

            row_dict = {}

            for column, value in zip(columns, row):

                row_dict[column] = value

            formatted_results.append(row_dict)
            dataframe = pd.DataFrame(formatted_results)

        return {
            "success": True,
            "row_count": len(formatted_results),
            "data": formatted_results,
            "table": dataframe.to_string(index=False)
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        db.close()


# ----------------------------------------
# TEST EXECUTOR
# ----------------------------------------

if __name__ == "__main__":

    sample_sql = """
    SELECT customers.city,
           SUM(claims.claim_amount) AS total_claims
    FROM claims
    JOIN policies
        ON claims.policy_id = policies.policy_id
    JOIN customers
        ON policies.customer_id = customers.customer_id
    GROUP BY customers.city
    ORDER BY total_claims DESC
    LIMIT 5;
    """

    result = execute_query(sample_sql)

    print("\nQUERY EXECUTION RESULT:\n")

    print(result)