import sys
from pathlib import Path
import pandas as pd


# ----------------------------------------
# PROJECT ROOT PATH FIX
# ----------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ----------------------------------------
# IMPORT SERVICES
# ----------------------------------------

# Service imports are done inside `run_aidra_pipeline` to avoid
# import-time issues (ensures project root is on sys.path first).


# ----------------------------------------
# MAIN AIDRA PIPELINE
# ----------------------------------------

def run_aidra_pipeline(user_question):

    # Import services here to avoid import-time failures
    from backend.services.ai_query_engine import generate_sql
    from backend.services.query_executor import execute_query
    # Some service modules may not expose named attributes when imported
    # via the package system in certain environments. Load them directly
    # from their file paths to ensure the module code is executed.
    import importlib.util

    rs_path = ROOT_DIR / "backend" / "services" / "result_summarizer.py"
    spec = importlib.util.spec_from_file_location(
        "backend.services.result_summarizer",
        str(rs_path)
    )
    result_summarizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result_summarizer)

    cg_path = ROOT_DIR / "backend" / "services" / "chart_generator.py"
    spec2 = importlib.util.spec_from_file_location(
        "backend.services.chart_generator",
        str(cg_path)
    )
    chart_generator = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(chart_generator)

    # ----------------------------------------
    # GENERATE SQL
    # ----------------------------------------

    generated_sql = generate_sql(user_question)

    # ----------------------------------------
    # VALIDATION FAILURE
    # ----------------------------------------

    if not generated_sql["success"]:

        return {
            "success": False,
            "error": "SQL validation failed",
            "validation": generated_sql["validation"]
        }

    # ----------------------------------------
    # EXECUTE SQL
    # ----------------------------------------

    execution_result = execute_query(
        generated_sql["sql_query"]
    )

    # ----------------------------------------
    # EXECUTION FAILURE
    # ----------------------------------------

    if not execution_result["success"]:

        return {
            "success": False,
            "error": execution_result["error"]
        }

    # ----------------------------------------
    # CREATE DATAFRAME
    # ----------------------------------------

    data = execution_result.get("data", [])

    dataframe = pd.DataFrame(data)

    # ----------------------------------------
    # GENERATE SUMMARY
    # ----------------------------------------

    summary = result_summarizer.summarize_results(
        user_question,
        execution_result.get("table", "")
    )

    # ----------------------------------------
    # GENERATE CHART
    # ----------------------------------------

    chart_path = chart_generator.generate_bar_chart(
        dataframe
    )

    # ----------------------------------------
    # FINAL RESPONSE
    # ----------------------------------------

    return {

        "success": True,

        "question": user_question,

        "sql_query": generated_sql["sql_query"],

        "table": execution_result["table"],

        "summary": summary,

        "chart_path": chart_path
    }


# ----------------------------------------
# TEST PIPELINE
# ----------------------------------------

if __name__ == "__main__":

    question = (
        "Show top 5 customer cities with highest claim amounts"
    )

    result = run_aidra_pipeline(question)

    print("\nAIDRA FINAL RESULT:\n")

    print(result)