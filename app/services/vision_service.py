from app.config import Config
import google.generativeai as genai

from app.config import Config

genai.configure(
    api_key=Config.GEMINI_API_KEY
)