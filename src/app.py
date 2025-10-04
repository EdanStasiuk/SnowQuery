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


def make_chart(df):
    """Build an interactive Altair chart with user-selected axes and chart type."""
    if df.empty:
        st.info("No data available for visualization.")
        return

    all_cols = df.columns.tolist()

    st.markdown("### Chart Visualization")

    with st.expander("Customize chart"):
        col1, col2 = st.columns(2)
        x_axis = col1.selectbox("X-axis", all_cols)
        y_axis = col2.selectbox("Y-axis", all_cols)
        chart_type = st.radio(
            "Chart type",
            ["Bar", "Line", "Scatter"],
            horizontal=True,
        )

    if x_axis and y_axis:
        # pick chart type properly (use Altair methods, not mark definitions)
        if chart_type == "Bar":
            chart = alt.Chart(df).mark_bar(color="#5890e5")
        elif chart_type == "Line":
            chart = alt.Chart(df).mark_line(color="#5890e5")
        else:
            chart = alt.Chart(df).mark_circle(color="#5890e5", size=60)

        chart = chart.encode(
            x=alt.X(x_axis, title=x_axis),
            y=alt.Y(y_axis, title=y_axis),
            tooltip=all_cols,
        ).properties(width=700, height=400)

        st.markdown("<br>", unsafe_allow_html=True)

        st.altair_chart(chart, use_container_width=True)


def run_streamlit():
    """Run the agent via Streamlit with interactive tables and charts."""
    st.set_page_config(page_title="SnowQuery", layout="wide")

    st.markdown("# SnowQuery")
    st.markdown("### _Your Snowflake SQL AI Assistant_")

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

    # Initialize session state variables
    if "df" not in st.session_state:
        st.session_state.df = None
    if "sql" not in st.session_state:
        st.session_state.sql = None

    # Run query
    if st.button("Run"):
        with st.spinner("Generating SQL and fetching results..."):
            sql, df = ask(question)
        st.session_state.sql = sql
        st.session_state.df = df

    # Display results if available
    if st.session_state.df is not None and not st.session_state.df.empty:
        st.markdown("### Generated SQL")
        st.code(st.session_state.sql, language="sql")

        st.markdown("### Query Results")
        st.dataframe(st.session_state.df, width="stretch")

        make_chart(st.session_state.df)


if __name__ == "__main__":
    # If arguments are provided, run CLI
    if len(sys.argv) > 1:
        run_cli()
    else:
        # Otherwise, assume Streamlit is running this script
        run_streamlit()
