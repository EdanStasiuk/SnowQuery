import sys

import altair as alt
import streamlit as st

from agent import ask


def run_cli():
    """Run the agent via CLI."""
    question = " ".join(sys.argv[1:])
    if question:
        sql, df = ask(question)
        print("Generated SQL:\n", sql)
        if df is not None:
            print(df.head())
    else:
        print("Usage: python app.py 'Your question here'")


def run_streamlit():
    """Run the agent via Streamlit with interactive tables and charts."""

    st.set_page_config(page_title="SnowQuery", layout="wide")

    # Page title
    st.markdown("# SnowQuery")
    st.markdown("### _Your Snowflake SQL AI Assistant_")

    # Input box
    question = st.text_input("Ask a question about your database:")

    # Button styling
    st.markdown(
        """
        <style>
        div.stButton > button {
            background-color: #5890e5;
            color: white;
            border-radius: 6px;
            padding: 0.5em 1.2em;
            font-weight: bold;
            border: none;
            transition: background-color 0.2s ease, transform 0.1s ease;
        }
        div.stButton > button:hover {
            background-color: #4178c0;
            transform: translateY(-1px);
        }
        div.stButton > button:active {
            background-color: #2d5790;
            transform: translateY(0);
        }
        """,
        unsafe_allow_html=True,
    )

    if st.button("Run"):
        with st.spinner("Generating SQL and fetching results..."):
            sql, df = ask(question)

        if df.empty:
            st.info("No results to display or SQL did not match schema.")

        st.markdown("### Generated SQL")
        st.code(sql, language="sql")

        if df is not None and not df.empty:
            st.markdown("### Query Results")
            st.dataframe(df, width="stretch")

            # Create chart if a numeric column exists
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                col_x = df.columns[0]  # first column as x-axis
                col_y = numeric_cols[0]  # first numeric column as y-axis
                chart = (
                    alt.Chart(df)
                    .mark_bar(color="#5890e5")
                    .encode(
                        x=alt.X(f"{col_x}:N", title=col_x),
                        y=alt.Y(f"{col_y}:Q", title=col_y),
                        tooltip=df.columns.tolist(),
                    )
                    .properties(width=700, height=400)
                )
                st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    # If arguments are provided, run CLI
    if len(sys.argv) > 1:
        run_cli()
    else:
        # Otherwise, assume Streamlit is running this script
        run_streamlit()
