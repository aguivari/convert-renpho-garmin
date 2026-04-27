import json
import os
import sys
import argparse
import garth
import getpass
from pathlib import Path
from garminconnect import Garmin

# Default file paths
GARMIN_HOME = Path.home() / ".garmin_uploader"
GARMIN_HOME.mkdir(exist_ok=True)
CONFIG_FILE = GARMIN_HOME / "credentials.json"
SESSION_DIR = GARMIN_HOME / "session"

def create_credentials():
    """
    Prompts the user for credentials and saves them to a JSON file.
    """
    print(f"Configuration file not found at {CONFIG_FILE}")
    print("Please enter your Garmin Connect credentials:")
    user = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    
    credentials = {
        "User": user,
        "Password": password
    }
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(credentials, f, indent=2)
        
        # Set restrictive permissions (read/write for owner only) on Unix-like systems
        if os.name == 'posix':
            os.chmod(CONFIG_FILE, 0o600)
            
        print(f"Credentials saved to {CONFIG_FILE}")
        return user, password
    except Exception as e:
        print(f"Error saving credentials: {e}")
        sys.exit(1)

def load_credentials():
    """
    Loads credentials from the JSON file or triggers creation if missing.
    """
    if not CONFIG_FILE.exists():
        return create_credentials()
        
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get('User'), data.get('Password')
    except (json.JSONDecodeError, KeyError):
        print("Error reading credentials file. You might need to delete it and run again.")
        sys.exit(1)

def login_v2(user, password):
    """
    Authenticates using Garth, handling session persistence and MFA.
    """
    try:
        # Tries to resume session from stored directory
        garth.resume(str(SESSION_DIR))
        print("Loaded stored session...")
    except Exception:
        print("Logging into Garmin Connect... This may prompt for MFA if enabled...")
        try:
            # Performs login and saves session tokens to disk
            garth.login(user, password)
            garth.save(str(SESSION_DIR))
            print("New session saved.")
        except Exception as e:
            if "429" in str(e):
                print("\nERROR 429: Too Many Requests.")
                print("Your IP might be temporarily rate-limited.")
                print("Try logging in and out on connect.garmin.com in a web browser first.")
            raise e

def main():
    parser = argparse.ArgumentParser(description="Garmin Connect FIT File Uploader")
    parser.add_argument("file", help="Path to the .fit file to upload")
    args = parser.parse_args()

    # Verify if the data file exists before attempting login
    if not os.path.exists(args.file):
        print(f"Error: Data file {args.file} not found.")
        sys.exit(1)

    user, pwd = load_credentials()
    
    try:
        login_v2(user, pwd)
        
        # Link Garth authenticated client to GarminConnect
        client = Garmin()
        client.garth = garth.client
        
        print(f"Using data file {args.file}...")
        # Uploads the file (works for activities and weight/health FIT files)
        client.upload_activity(args.file)
        print("Successfully uploaded the file!")

    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()