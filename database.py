"""MongoDB database operations for candidate data storage."""

from pymongo import MongoClient
from datetime import datetime, timezone
from typing import Optional
import config


def get_database():
    """Get MongoDB database connection."""
    client = MongoClient(config.MONGODB_URI)
    return client[config.DATABASE_NAME]


def save_candidate(candidate_data: dict) -> str:
    """
    Save candidate data to MongoDB.
    
    Args:
        candidate_data: Dictionary containing candidate information
        
    Returns:
        Inserted document ID as string
    """
    db = get_database()
    collection = db[config.CANDIDATES_COLLECTION]
    
    # Add timestamp
    candidate_data["created_at"] = datetime.now(timezone.utc)
    candidate_data["updated_at"] = datetime.now(timezone.utc)
    
    result = collection.insert_one(candidate_data)
    return str(result.inserted_id)


def get_candidate(candidate_id: str) -> Optional[dict]:
    """Retrieve a candidate by ID."""
    from bson import ObjectId
    db = get_database()
    collection = db[config.CANDIDATES_COLLECTION]
    return collection.find_one({"_id": ObjectId(candidate_id)})


def update_candidate(candidate_id: str, update_data: dict) -> bool:
    """Update candidate data."""
    from bson import ObjectId
    db = get_database()
    collection = db[config.CANDIDATES_COLLECTION]
    
    update_data["updated_at"] = datetime.now(timezone.utc)
    result = collection.update_one(
        {"_id": ObjectId(candidate_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0
