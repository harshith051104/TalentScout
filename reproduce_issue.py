
import os
import sys


# Add current directory to path
sys.path.append(os.getcwd())

import signal
import sys

# Fix for Windows where some signals are not defined
if sys.platform.startswith('win'):
    for sig in ['SIGHUP', 'SIGTSTP', 'SIGCONT']:
        if not hasattr(signal, sig):
            setattr(signal, sig, signal.SIGTERM)

from crew_agent import TalentScoutCrew
import traceback

def test_agent():
    print("Initializing TalentScoutCrew...")
    try:
        crew = TalentScoutCrew()
        print("Agent initialized.")
        
        print("Running simple prompt...")
        response = crew.run("Hello, who are you?")
        print("\nResponse from Agent:")
        print(response)
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_agent()
