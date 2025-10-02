from snowflake_client import run_query

df = run_query("SELECT * FROM CUSTOMER LIMIT 5;")
print(df)
