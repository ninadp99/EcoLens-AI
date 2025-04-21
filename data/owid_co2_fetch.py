import pandas as pd
import psycopg2
import streamlit as st

# Load CO₂ dataset
df = pd.read_csv("https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv")
df = df[["country", "year", "co2", "co2_per_capita", "population"]]
df = df.dropna(subset=["co2"])

# Connect to Supabase PostgreSQL
conn = psycopg2.connect(
    host=st.secrets["postgres"]["host"],
    dbname=st.secrets["postgres"]["dbname"],
    user=st.secrets["postgres"]["user"],
    password=st.secrets["postgres"]["password"],
    port=st.secrets["postgres"]["port"]
)
cur = conn.cursor()

# Insert data
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO emissions (country, year, co2_emission, co2_per_capita, population)
        VALUES (%s, %s, %s, %s, %s)
    """, (row["country"], int(row["year"]), float(row["co2"]), row["co2_per_capita"], row["population"]))

conn.commit()
cur.close()
conn.close()

print("✅ Data inserted successfully.")
