import streamlit as st
import psycopg2
import pandas as pd
from transformers import pipeline

# --- Hugging Face models ---
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# You can later add a forecasting model here too

# --- Database connection ---
def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        dbname=st.secrets["postgres"]["dbname"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )

# --- Handle query ---
def handle_query(user_input):
    if "summary" in user_input.lower():
        # Summarize most recent emissions data
        query = "SELECT country, year, co2_emission FROM emissions WHERE year >= 2019"
        df = pd.read_sql(query, get_connection())
        text = df.to_string(index=False)
        result = summarizer(text, max_length=120, min_length=50, do_sample=False)
        summary = result[0]['summary_text']
        store_insight("summarization", summary)
        return summary
    
    elif "forecast" in user_input.lower():
        return "⏳ Forecasting module coming in next build."

    else:
        return "❗ Unsupported query. Try asking for a summary or forecast."

# --- Store AI insight in Supabase (optional) ---
def store_insight(task_type, result_text):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ai_insights (task_type, result_text)
        VALUES (%s, %s)
    """, (task_type, result_text))
    conn.commit()
    cur.close()
    conn.close()

# --- Example test run ---
if __name__ == "__main__":
    query = input("Enter your query: ")
    print(handle_query(query))
