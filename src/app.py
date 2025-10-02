import sys

import streamlit as st

from agent import ask


def run_cli():
    """Run the agent via CLI."""
    question = " ".join(sys.argv[1:])
    if question:
        answer = ask(question)
        print(answer)
    else:
        print("Usage: python app.py 'Your question here'")


def run_streamlit():
    """Run the agent via Streamlit."""

    st.markdown("# SnowQuery")
    st.markdown("### _Your Snowflake SQL AI Assistant_")
    question = st.text_input("Ask a question about your database:")

    st.markdown(
        """
        <style>
        /* Style the Streamlit button */
        div.stButton > button {
            background-color: #5890e5;  /* normal color */
            color: white;
            border-radius: 6px;
            padding: 0.5em 1.2em;
            font-weight: bold;
            border: none;
            transition: background-color 0.2s ease, transform 0.1s ease;
        }

        /* Hover color */
        div.stButton > button:hover {
            background-color: #4178c0;  /* darker blue on hover */
            transform: translateY(-1px); /* optional subtle lift effect */
        }

        /* Active / click color */
        div.stButton > button:active {
            background-color: #2d5790;  /* even darker when pressed */
            transform: translateY(0);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Run"):
        answer = ask(question)
        st.write(answer)


if __name__ == "__main__":
    # If arguments are provided, run CLI
    if len(sys.argv) > 1:
        run_cli()
    else:
        # Otherwise, assume Streamlit is running this script
        run_streamlit()
