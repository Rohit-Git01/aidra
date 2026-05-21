import sys
from pathlib import Path
import re
import ollama


# ----------------------------------------
# PROJECT ROOT PATH FIX
# ----------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from backend.services.sql_validator import (validate_sql)


# ----------------------------------------
# IMPORT METADATA LOADERS
# ----------------------------------------

from backend.utils.metadata_loader import (
    load_schema_metadata,
    load_relationship_metadata,
    load_glossary_metadata
)


# ----------------------------------------
# LOAD METADATA
# ----------------------------------------

schema_metadata = load_schema_metadata()

relationship_metadata = load_relationship_metadata()

glossary_metadata = load_glossary_metadata()


# ----------------------------------------
# FORMAT SCHEMA METADATA
# ----------------------------------------

def format_schema_metadata(schema_metadata):

    formatted_text = ""

    for table_name, table_data in schema_metadata.items():

        actual_table_name = table_data.get("table_name", table_name)

        formatted_text += f"\nTABLE: {actual_table_name}\n"

        columns = table_data.get("columns", [])

        formatted_text += "COLUMNS:\n"

        for column in columns:
            formatted_text += f"- {column['column_name']}\n"

    return formatted_text


# ----------------------------------------
# FORMAT RELATIONSHIP METADATA
# ----------------------------------------

def format_relationship_metadata(relationship_metadata):

    formatted_text = "\nRELATIONSHIPS:\n"

    relationships = relationship_metadata.get(
        "insurance_relationships",
        {}
    ).get(
        "relationships",
        []
    )

    for relationship in relationships:

        formatted_text += (
            f"- "
            f"{relationship['from_table']}.{relationship['from_column']} "
            f"-> "
            f"{relationship['to_table']}.{relationship['to_column']}\n"
        )

    return formatted_text


# ----------------------------------------
# FORMAT GLOSSARY METADATA
# ----------------------------------------

def format_glossary_metadata(glossary_metadata):

    formatted_text = "\nBUSINESS TERMS:\n"

    business_terms = glossary_metadata.get(
        "business_terms",
        {}
    ).get(
        "business_terms",
        []
    )

    for term in business_terms:

        formatted_text += (
            f"- {term['term']} "
            f"maps to "
            f"{term['table']}.{term['mapped_column']}\n"
        )

    return formatted_text


# ----------------------------------------
# BUILD AI PROMPT
# ----------------------------------------

def build_prompt(user_question):

    formatted_schema = format_schema_metadata(schema_metadata)

    formatted_relationships = format_relationship_metadata(
        relationship_metadata
    )

    formatted_glossary = format_glossary_metadata(
        glossary_metadata
    )

    prompt = f"""
ROLE:
You are an expert PostgreSQL SQL query generator.

YOUR TASK:
Generate ONLY valid PostgreSQL SELECT queries.

--------------------------------------------------
DATABASE RULES
--------------------------------------------------

- Generate ONLY SELECT queries
- Use PostgreSQL syntax only
- Return ONLY raw SQL
- Do not explain anything
- Do not generate markdown
- Do not generate comments

--------------------------------------------------
SCHEMA RULES
--------------------------------------------------

- Use ONLY tables listed below
- Use ONLY columns listed below
- Never invent tables
- Never invent columns

--------------------------------------------------
RELATIONSHIP RULES
--------------------------------------------------

- Use ONLY relationships listed below
- Never assume direct relationships
- Use intermediate tables when necessary
- Never invent foreign keys

--------------------------------------------------
SPECIAL NOTES
--------------------------------------------------

- No cities table exists
- No city_id column exists
- customers.city contains city directly

--------------------------------------------------
SCHEMA METADATA
--------------------------------------------------

{formatted_schema}

--------------------------------------------------
RELATIONSHIP METADATA
--------------------------------------------------

{formatted_relationships}

--------------------------------------------------
BUSINESS GLOSSARY
--------------------------------------------------

{formatted_glossary}

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{user_question}

--------------------------------------------------
RETURN ONLY VALID PostgreSQL SQL QUERY
--------------------------------------------------
"""

    return prompt


# ----------------------------------------
# EXTRACT SQL FROM LLM RESPONSE
# ----------------------------------------

def extract_sql(response_text):

    sql_pattern = r"SELECT[\s\S]*?;"

    match = re.search(
        sql_pattern,
        response_text,
        re.IGNORECASE
    )

    if match:
        return match.group(0).strip()

    return None


# ----------------------------------------
# GENERATE SQL USING MISTRAL
# ----------------------------------------

def generate_sql(user_question):

    prompt = build_prompt(user_question)

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw_response = response["message"]["content"]

    sql_query = extract_sql(raw_response)

    if sql_query is None:
        return {
            "success": False,
            "sql_query": None,
            "validation": {
                "is_valid": False,
                "error": "No SQL query could be extracted from the model response.",
                "response": raw_response
            }
        }

    validation_result = validate_sql(sql_query)

    if validation_result["is_valid"]:
        return{
            "success": True,
            "sql_query": sql_query,
            "validation": validation_result
        }
    else:
        return {
            "success": False,
            "sql_query": sql_query,
            "validation": validation_result
        }


# ----------------------------------------
# TEST ENGINE
# ----------------------------------------

if __name__ == "__main__":

    question = "Show top 5 cities with highest claim amounts"

    result = generate_sql(question)

    print("\nAIDRA RESULT:\n")

    print(result)