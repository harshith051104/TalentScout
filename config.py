import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MONGODB_URI = os.getenv("MONGODB_URI") 
DATABASE_NAME = "talentscout"
CANDIDATES_COLLECTION = "candidates"

EXIT_KEYWORDS = ["bye", "exit", "quit", "goodbye", "thank you", "thanks", "end"]

GEMINI_MODEL = "gemini-2.0-flash"
