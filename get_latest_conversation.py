
import config
from database import get_database
import pprint

def print_latest_conversation():
    print("Connecting to MongoDB...")
    try:
        db = get_database()
        collection = db[config.CANDIDATES_COLLECTION]
        
        # Get latest candidate by created_at desc
        latest = collection.find_one(sort=[("created_at", -1)])
        
        if not latest:
            print("No conversations found in database.")
            return

        print(f"\nLast Session ID: {latest.get('_id')}")
        print(f"Candidate: {latest.get('full_name')} ({latest.get('email')})")
        print("-" * 50)
        
        history = latest.get("conversation_history", [])
        if not history:
            print("No conversation history found.")
        
        for msg in history:
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")
            print(f"[{role}]: {content}")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error retrieving conversation: {e}")

if __name__ == "__main__":
    print_latest_conversation()
