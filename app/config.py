import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    DB_NAME = os.getenv("DB_NAME", "contracts_db")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    HIGH_RISK_TERMS = os.getenv("HIGH_RISK_TERMS", "indemnity,liability,termination,damages,breach").split(",")
    USE_AI = os.getenv("USE_AI", "false").lower() == "true"
    USE_FREQUENT_TERMS = os.getenv("USE_FREQUENT_TERMS", "false").lower() == "true"
    USE_SUPERVISED_MODEL = os.getenv("USE_SUPERVISED_MODEL", "false").lower() == "true"
