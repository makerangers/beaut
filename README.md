# Streamlit Makeup Chatbot

This repository provides a simple Streamlit app that chats with users about makeup products. The chatbot uses OpenAI's API to generate responses and can search the sample dataset `EYES_analysis_final_cleaned.csv` for product recommendations.

## Requirements

- Python 3.8+
- `streamlit`
- `openai`
- `python-dotenv`

## Setup

1. Install dependencies:

```bash
pip install streamlit openai python-dotenv
```

2. Create a `.env` file in the project root containing your OpenAI API key:

```bash
OPENAI_API_KEY=sk-...
```

## Running the App

Start the Streamlit application locally:

```bash
streamlit run server.py
```

The app will load the product data and present a chat interface. It uses the `gpt-4o-mini` model for responses and searches the dataset when you request recommendations using an E.Y.E.S code.
