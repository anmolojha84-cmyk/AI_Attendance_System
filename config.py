import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    import streamlit as st
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not GEMINI_API_KEY:
    GEMINI_API_KEY = "AQ.Ab8RN6KIiiq2VrP0WbgZ_RZDqwEuMCBRfzn6X8mXLXGavhRwRw"

if not GEMINI_API_KEY:
    try:
        print("❌ Gemini API Key Not Found")
    except Exception:
        print("[ERROR] Gemini API Key Not Found")
else:
    try:
        print("✅ Gemini API Loaded Successfully")
    except Exception:
        print("[OK] Gemini API Loaded Successfully")
