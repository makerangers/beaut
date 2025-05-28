import os
import pandas as pd
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@st.cache_data
def load_data():
    return pd.read_csv("EYES_analysis_final_cleaned.csv")

df = load_data()

st.title("E.Y.E.S Code Makeup Recommender")

user_input = st.text_area("Describe your makeup style and concerns")

if st.button("Analyze and Recommend"):
    if not openai.api_key:
        st.error("OPENAI_API_KEY not set in .env")
    elif not user_input.strip():
        st.error("Please enter some details.")
    else:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a beauty expert. "
                    "Classify the user's description into a 4-letter E.Y.E.S code "
                    "based on Pointy, Long-lasting, Pencil, Flexible and similar attributes. "
                    "Respond with only the 4-letter code."
                ),
            },
            {"role": "user", "content": user_input},
        ]
        with st.spinner("Analyzing with GPT..."):
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0,
                )
                code = resp["choices"][0]["message"]["content"].strip().upper()[:4]
            except Exception as e:
                st.error(f"OpenAI API error: {e}")
                code = ""
        if code:
            st.success(f"Predicted EYES code: {code}")
            recs = df[df["EYES_code"].str.upper() == code].head(5)
            if recs.empty:
                st.info("No products found for this code.")
            else:
                for _, row in recs.iterrows():
                    st.subheader(row["clean_name"])
                    st.write(row["summary"])
                    st.write(f"[Buy here]({row['url']})")
