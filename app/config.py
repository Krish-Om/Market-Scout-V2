from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


class Config:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    ORIGINS = os.environ.get(
        "ORIGINS", "http://localhost,http://localhost:8000,http://localhost:3000"
    ).split(",")
