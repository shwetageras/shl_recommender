from fastapi import FastAPI, Query
from typing import List
import pandas as pd
from fuzzywuzzy import fuzz
import uvicorn

app = FastAPI()

# Load data
df = pd.read_csv("shl_data.csv")
df.columns = df.columns.str.strip()

# Fuzzy match functions
def fuzzy_match(df, column, keywords, threshold=85):
    matches = pd.DataFrame()
    for keyword in keywords:
        filtered = df[df[column].apply(lambda x: isinstance(x, str) and fuzz.partial_ratio(x.lower(), keyword) >= threshold)]
        matches = pd.concat([matches, filtered])
    return matches.drop_duplicates()

# Recommendation endpoint
@app.get("/recommend")
def recommend(query: str = Query(..., description="Role or skill to match")):
    keywords = [k.strip().lower() for k in query.split(',')]
    results = pd.concat([
        fuzzy_match(df, 'Job Title', keywords),
        fuzzy_match(df, 'Skills Measured', keywords)
    ]).drop_duplicates().head(10)

    response = []
    for _, row in results.iterrows():
        response.append({
            "assessment_name": row['Job Title'],
            "remote_testing": row['Remote'],
            "adaptive_irt": row['Adaptive'],
            "duration": row['Duration\n(in minutes)'],
            "test_type": row['max_items'],  # replace if you have a better test_type column
        })
    return response