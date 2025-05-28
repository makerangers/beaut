# Beauty Recommender

This project provides a simple Streamlit app that analyzes a user's makeup description, predicts an **E.Y.E.S** code with GPT-4o-mini, and recommends matching products from `EYES_analysis_final_cleaned.csv`.

## Setup

1. Create a `.env` file based on `.env.example` and add your OpenAI API key.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```bash
   streamlit run app.py
   ```

## Files
- `app.py` – Streamlit interface.
- `EYES_analysis_final_cleaned.csv` – Dataset of products with E.Y.E.S codes.
