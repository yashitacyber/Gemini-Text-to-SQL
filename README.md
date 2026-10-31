# Gemini Text-to-SQL

A Natural Language to SQL application built using Python, Streamlit, SQLite, and Google Gemini API.

## About the Project
This application allows users to interact with a student database using simple English questions. Google Gemini converts natural language questions into SQL queries, executes them on the SQLite database, and displays the results.

## Tech Stack
- Python
- Google Gemini API
- Streamlit
- SQLite
- SQL

## Features
- Natural Language to SQL conversion
- AI-powered SQL generation
- SQLite database integration
- Query result visualization
- SELECT-only query restriction
- Secure API key management using environment variables

## Project Setup

1. Clone the repository.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Create a `.env` file in the project folder:

   `GOOGLE_API_KEY=your_api_key_here`

4. Run the application:

   `streamlit run app.py`

## Note
You need your own Google Gemini API key to run this project.

Never upload your actual API key to GitHub.