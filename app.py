
from dotenv import load_dotenv
load_dotenv()

import os
import re
import sqlite3
import streamlit as st
from google import genai

# Gemini configuration
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY is missing. Check your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Database configuration
DB_PATH = "student.db"


# Generate SQL using Gemini
def get_gemini_response(question):

    prompt = """
    You are an expert Text-to-SQL assistant.

    Database name: STUDENT

    Table: STUDENT

    Columns:
    NAME (VARCHAR)
    CLASS (VARCHAR)
    SECTION (VARCHAR)
    MARKS (INTEGER)

    Rules:
    1. Convert the user's English question into SQLite SQL.
    2. Return ONLY one SQL query.
    3. Do not include markdown or code fences.
    4. Generate SELECT queries only.
    5. Never generate INSERT, UPDATE, DELETE, DROP,
       ALTER, CREATE or other modification queries.
    6. Use the exact table and column names provided.
    """

    try:
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=f"{prompt}\n\nUser question: {question}"
        )

        return response.output_text.strip()

    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return None


# Clean generated SQL
def clean_sql(sql):

    sql = re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE)
    return sql.strip().rstrip(";")


# Execute SQL query safely
def read_sql_query(sql, db):

    conn = None

    try:
        conn = sqlite3.connect(db)

        # Read-only transaction
        conn.execute("PRAGMA query_only = ON")

        cursor = conn.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        return columns, rows

    finally:
        if conn:
            conn.close()


# Streamlit interface
st.set_page_config(
    page_title="Gemini Text-to-SQL",
    page_icon="🗄️",
    layout="centered"
)

st.title("Gemini App To Retrieve SQL Data")

st.write(
    "Ask questions about your student database "
    "using natural language."
)

question = st.text_input(
    "Enter your question:",
    placeholder="Show all students with marks above 80"
)

if st.button("Ask the question", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating SQL query..."):

            response = get_gemini_response(question)

        if response:

            sql = clean_sql(response)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            # Only allow SELECT queries
            if not re.match(r"^\s*SELECT\b", sql, re.IGNORECASE):
                st.error("Only SELECT queries are allowed.")
                st.stop()

            try:

                with st.spinner("Executing SQL query..."):

                    columns, data = read_sql_query(sql, DB_PATH)

                st.subheader("Query Results")

                if data:
                    st.dataframe(
                        [dict(zip(columns, row)) for row in data],
                        use_container_width=True
                    )

                    st.success(f"{len(data)} records found.")

                else:
                    st.info("Query executed successfully. No records found.")

            except sqlite3.Error as e:
                st.error(f"Database Error: {e}")

            except Exception as e:
                st.error(f"Unexpected Error: {e}")

