# SnowQuery

An AI-powered assistant that turns natural language into Snowflake queries using MCP and agentic reasoning.

## Project directory setup

```
SnowQuery/
│── src/
│ ├── agent.py # Main agent logic (MCP + LLM + orchestration)
│ ├── snowflake_client.py # Connects & queries Snowflake
│ ├── mcp_context.py # MCP integration (schemas, metadata provider)
│ └── app.py # CLI or Streamlit web interface
│
│── requirements.txt # deps (snowflake-connector-python, openai, streamlit, mcp)
|–– .env # Snowflake + API credentials (you will need to create this file to run SnowQuery––sorry, credits cost $$$)
│── README.md
```

## How to use

You can run this app easily from the CLI or through a web interface:

### CLI

```
python3 app.py "<Enter your prompt here>"
```

#### Example:

```
python3 app.py "Show me top 5 customers by revenue"
```

### Streamlit web app

```
streamlit run app.py
```
