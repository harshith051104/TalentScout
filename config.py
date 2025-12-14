"""Configuration for TalentScout Hiring Assistant."""

import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI") 
DATABASE_NAME = "talentscout"
CANDIDATES_COLLECTION = "candidates"

# Exit keywords that end the conversation
EXIT_KEYWORDS = ["bye", "exit", "quit", "goodbye", "thank you", "thanks", "end"]

# Model configuration
GEMINI_MODEL = "gemini-2.0-flash"
