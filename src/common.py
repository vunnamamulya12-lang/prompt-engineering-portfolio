import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env (expects GEMINI_API_KEY)
load_dotenv()
API_KEY = os.getenv("AIzaSyCVbzpRk54g_wRnqmBldTAUUvbvvyzomzI")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Create a .env file (from .env.example) "
        "and set GEMINI_API_KEY=AIzaSyCVbzpRk54g_wRnqmBldTAUUvbvvyzomzI"
    )

# Configure Gemini
genai.configure(api_key=API_KEY)

# Create a reusable model instance (adjust model name if needed)
MODEL_NAME = "gemini-2.5-pro"

def get_model():
    return genai.GenerativeModel(MODEL_NAME)