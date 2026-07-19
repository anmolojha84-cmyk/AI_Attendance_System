import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = "AQ.Ab8RN6LQyiTqq7YpPVJo8uLjmcde2y9mR3fWPSe_p-jEXZ3F3Q"

if not GEMINI_API_KEY:
    print("❌ Gemini API Key Not Found")
else:
    print("✅ Gemini API Loaded Successfully")