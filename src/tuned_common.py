# tuned_common.py
from typing import Optional
import os, time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AIzaSyCVbzpRk54g_wRnqmBldTAUUvbvvyzomzI")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in .env")
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-pro"

# You can tweak these defaults per experiment
DEFAULT_CFG = {
    "temperature": 0.5,          # lower = more deterministic
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 512,
}

def get_model(cfg: Optional[dict] = None):
    cfg = cfg or DEFAULT_CFG
    return genai.GenerativeModel(MODEL_NAME, generation_config=cfg)

def safe_generate(model, prompt, retries=2, backoff=1.5):
    """Simple retry wrapper for transient errors/rate limits."""
    for attempt in range(retries + 1):
        try:
            return model.generate_content(prompt).text
        except Exception as e:
            if attempt == retries:
                raise
            time.sleep(backoff ** attempt)