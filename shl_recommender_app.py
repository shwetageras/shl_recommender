#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st

# === Load Data ===
df = pd.read_csv("shl_data.csv")
df.columns = df.columns.str.strip()

# === Fuzzy Matching Functions ===
def recommend_by_role(user_input, df, threshold=85):
    keywords = [k.strip().lower() for k in user_input.split(',')]
    matches = pd.DataFrame()
    for keyword in keywords:
        filtered = df[df['Job Title'].apply(
            lambda x: isinstance(x, str) and fuzz.partial_ratio(x.lower(), keyword) >= threshold
        )]
        matches = pd.concat([matches, filtered])
    return matches.drop_duplicates()

def recommend_by_competency(user_input, df, threshold=85):
    keywords = [k.strip().lower() for k in user_input.split(',')]
    matches = pd.DataFrame()
    for keyword in keywords:
        filtered = df[df['Skills Measured'].apply(
            lambda x: isinstance(x, str) and fuzz.partial_ratio(x.lower(), keyword) >= threshold
        )]
        matches = pd.concat([matches, filtered])
    return matches.drop_duplicates()

# === Streamlit UI ===
st.title("SHL Assessment Recommender")

search_type = st.radio("Search by:", ["Role", "Skill", "Both"])
user_input = st.text_input("Enter keywords (comma-separated):")

if st.button("Get Recommendations"):
    if not user_input:
        st.warning("Please enter some keywords.")
    else:
        if search_type == "Role":
            results = recommend_by_role(user_input, df)
        elif search_type == "Skill":
            results = recommend_by_competency(user_input, df)
        else:
            results = pd.concat([
                recommend_by_role(user_input, df),
                recommend_by_competency(user_input, df)
            ]).drop_duplicates()

        if not results.empty:
            st.success(f"Found {len(results)} matching assessment(s):")
            st.dataframe(results[['Job Title', 'Duration\n(in minutes)', 'avg_items', 'max_items', 'Skills Measured', 'Remote', 'Adaptive']])
        else:
            st.error("No matching assessments found.")


# In[ ]:




