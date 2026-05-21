import re
import sys
from pathlib import Path


# ----------------------------------------
# PROJECT ROOT PATH FIX
# ----------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ----------------------------------------
# IMPORT METADATA LOADERS
# ----------------------------------------

from backend.utils.metadata_loader import (
    load_schema_metadata,
    load_relationship_metadata
)


# ----------------------------------------
# LOAD METADATA
# ----------------------------------------

schema_metadata = load_schema_metadata()

relationship_metadata = load_relationship_metadata()


# ----------------------------------------
# GET VALID TABLES
# ----------------------------------------

def get_valid_tables():

    valid_tables = set()

    for table_data in schema_metadata.values():

        table_name = table_data.get("table_name")

        if table_name:
            valid_tables.add(table_name)

    return valid_tables


# ----------------------------------------
# GET VALID RELATIONSHIPS
# ----------------------------------------

def get_valid_relationships():

    valid_relationships = set()

    relationships = relationship_metadata.get(
        "insurance_relationships",
        {}
    ).get(
        "relationships",
        []
    )

    for relationship in relationships:

        from_side = (
            f"{relationship['from_table']}."
            f"{relationship['from_column']}"
        )

        to_side = (
            f"{relationship['to_table']}."
            f"{relationship['to_column']}"
        )

        valid_relationships.add(
            (from_side, to_side)
        )

    return valid_relationships


# ----------------------------------------
# VALIDATE SELECT ONLY
# ----------------------------------------

def validate_select_only(sql_query):

    sql_upper = sql_query.upper()

    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE"
    ]

    for keyword in forbidden_keywords:

        if keyword in sql_upper:
            return False

    return sql_upper.strip().startswith("SELECT")


# ----------------------------------------
# EXTRACT TABLES
# ----------------------------------------

def extract_tables(sql_query):

    table_pattern = (
        r"(FROM|JOIN)\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*)"
    )

    matches = re.findall(
        table_pattern,
        sql_query,
        re.IGNORECASE
    )

    tables = set()

    for _, table_name in matches:
        tables.add(table_name)

    return tables


# ----------------------------------------
# EXTRACT JOIN CONDITIONS
# ----------------------------------------

def extract_join_conditions(sql_query):

    join_pattern = (
        r"ON\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*"
        r"\.[a-zA-Z_][a-zA-Z0-9_]*)"
        r"\s*=\s*"
        r"([a-zA-Z_][a-zA-Z0-9_]*"
        r"\.[a-zA-Z_][a-zA-Z0-9_]*)"
    )

    matches = re.findall(
        join_pattern,
        sql_query,
        re.IGNORECASE
    )

    extracted_joins = []

    for left_side, right_side in matches:

        extracted_joins.append(
            (
                left_side.strip(),
                right_side.strip()
            )
        )

    return extracted_joins


# ----------------------------------------
# VALIDATE TABLES
# ----------------------------------------

def validate_tables(sql_query):

    extracted_tables = extract_tables(sql_query)

    valid_tables = get_valid_tables()

    invalid_tables = (
        extracted_tables - valid_tables
    )

    return (
        len(invalid_tables) == 0,
        invalid_tables
    )


# ----------------------------------------
# VALIDATE RELATIONSHIPS
# ----------------------------------------

def validate_relationships(sql_query):

    extracted_joins = (
        extract_join_conditions(sql_query)
    )

    valid_relationships = (
        get_valid_relationships()
    )

    invalid_joins = []

    for left_side, right_side in extracted_joins:

        relationship_pair = (
            left_side,
            right_side
        )

        reverse_pair = (
            right_side,
            left_side
        )

        if (
            relationship_pair not in valid_relationships
            and reverse_pair not in valid_relationships
        ):

            invalid_joins.append(
                relationship_pair
            )

    return (
        len(invalid_joins) == 0,
        invalid_joins
    )


# ----------------------------------------
# MAIN SQL VALIDATION
# ----------------------------------------

def validate_sql(sql_query):

    validation_results = {}

    # ----------------------------------------
    # SELECT ONLY VALIDATION
    # ----------------------------------------

    validation_results["select_only"] = (
        validate_select_only(sql_query)
    )

    # ----------------------------------------
    # TABLE VALIDATION
    # ----------------------------------------

    table_validation, invalid_tables = (
        validate_tables(sql_query)
    )

    validation_results["valid_tables"] = (
        table_validation
    )

    validation_results["invalid_tables"] = (
        list(invalid_tables)
    )

    # ----------------------------------------
    # RELATIONSHIP VALIDATION
    # ----------------------------------------

    relationship_validation, invalid_joins = (
        validate_relationships(sql_query)
    )

    validation_results["valid_relationships"] = (
        relationship_validation
    )

    validation_results["invalid_joins"] = (
        invalid_joins
    )

    # ----------------------------------------
    # FINAL VALIDATION STATUS
    # ----------------------------------------

    validation_results["is_valid"] = all([
        validation_results["select_only"],
        validation_results["valid_tables"],
        validation_results["valid_relationships"]
    ])

    return validation_results


# ----------------------------------------
# TEST VALIDATOR
# ----------------------------------------

if __name__ == "__main__":

    sample_sql = """
    SELECT customers.city,
           SUM(claims.claim_amount)
    FROM claims
    JOIN policies
        ON claims.policy_id = policies.policy_id
    JOIN customers
        ON policies.customer_id = customers.customer_id
    GROUP BY customers.city;
    """

    result = validate_sql(sample_sql)

    print("\nValidation Result:\n")

    print(result)