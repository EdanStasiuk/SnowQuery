import os

import pandas as pd
from dotenv import load_dotenv

from snowflake_client import run_query

load_dotenv()

"""
mcp_context.py

Fetches Snowflake schema metadata and formats it into a structured context
suitable for use with an MCP-based AI agent.
"""


def get_schema_metadata() -> pd.DataFrame:
    """
    Fetches schema metadata from Snowflake's INFORMATION_SCHEMA.

    Reads the target schema from the environment variable SNOWFLAKE_SCHEMA
    and retrieves all table names, column names, and data types within that schema.

    Returns:
        pd.DataFrame: A DataFrame with columns ['TABLE_NAME', 'COLUMN_NAME', 'DATA_TYPE'].
    """
    sql = f"""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = '{os.getenv("SNOWFLAKE_SCHEMA")}'
    ORDER BY table_name, ordinal_position;
    """
    df = run_query(sql)
    return df


def format_schema_context():
    """
    Converts the schema metadata into a structured dictionary for agent use.

    Groups columns by table name to provide a simple mapping of:
        table_name -> list of column names

    Returns:
        dict: Dictionary mapping tbale names to lists of column names.
    """
    df = get_schema_metadata()
    context = {}
    for table, group in df.groupby("TABLE_NAME"):
        context[table] = list(group["COLUMN_NAME"])
    return context


if __name__ == "__main__":
    schema = format_schema_context()
    print(schema)
