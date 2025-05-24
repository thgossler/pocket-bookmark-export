#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pocket to Browser Bookmarks Exporter
====================================

This script exports your saved articles from Pocket to your browser bookmarks.
The bookmarks will be organized in a 'Pocket-Export' folder in your browser.

Setup Instructions:
------------------

1. Create and activate a virtual environment:
   cd /path/to/PocketExport
   python3 -m venv .
   source bin/activate  # On macOS/Linux
   # or: .\\Scripts\\activate  # On Windows

2. Install required packages:
   pip install requests

3. Get your Pocket API Consumer Key:
   - Go to: https://getpocket.com/developer/apps/new
   - Create a new application with 'Retrieve' permissions
   - Copy the Consumer Key (you'll be prompted for it when running the script)

4. Run the script:
   python main.py

Requirements:
------------
- Python 3.6+
- requests library
- A Pocket account with saved articles
- Supported browsers: Microsoft Edge, Google Chrome, Mozilla Firefox

The script will:
- Prompt you for your Pocket Consumer Key
- Guide you through the OAuth authorization process
- Detect your operating system and suggest a default browser
- Create a backup of your current bookmarks
- Export all your Pocket items to a new 'Pocket-Export' folder
"""

# Import standard and third-party libraries
import os
import time
import json
import shutil
import requests
import platform
import webbrowser
from pathlib import Path

# ====== Configuration ======
# Pocket API consumer key - will be set during runtime
CONSUMER_KEY  = ""  # Pocket Consumer Key
# Pocket API access token, will be set after authentication
ACCESS_TOKEN  = ""  # Pocket Access Token
# Default Edge profile path for macOS
EDGE_PROFILE  = Path.home() / "Library" / "Application Support" / "Microsoft Edge" / "Default"
# Default bookmarks file and backup file for Edge
BOOKMARKS_FILE = EDGE_PROFILE / "Bookmarks"
BACKUP_FILE    = EDGE_PROFILE / "Bookmarks.bak"

# ====== Helper for Chrome and Edge timestamps ======
# Chrome and Edge use microseconds since 1601-01-01 UTC as their timestamp format
EPOCH_OFFSET = 11644473600000000

def get_pocket_consumer_key():
    """
    Prompts the user to enter their Pocket Consumer Key with instructions.
    """
    print("\n" + "="*60)
    print("🔑 POCKET API CONSUMER KEY REQUIRED")
    print("="*60)
    print("To use this script, you need a Pocket API Consumer Key.")
    print("\nWhat is a Consumer Key?")
    print("• It's a unique identifier that allows this app to access Pocket's API")
    print("• It's free and takes just a few minutes to obtain")
    print("\nHow to get your Consumer Key:")
    print("1. Go to: https://getpocket.com/developer/apps/new")
    print("2. Fill out the form:")
    print("   • Application Name: 'Pocket Bookmark Exporter' (or any name)")
    print("   • Application Description: 'Export Pocket items to browser bookmarks'")
    print("   • Permissions: Select 'Retrieve'")
    print("   • Platforms: Select 'Desktop (other)'")
    print("3. Click 'Create Application'")
    print("4. Copy the 'Consumer Key' from the app details page")
    print("\n" + "="*60)
    
    while True:
        consumer_key = input("Please enter your Pocket Consumer Key: ").strip()
        if consumer_key:
            return consumer_key
        print("❌ Consumer Key cannot be empty. Please try again.")

def get_pocket_access_token(consumer_key):
    # Step 1: Request a request token from Pocket
    req_token_url = "https://getpocket.com/v3/oauth/request"
    headers = {"X-Accept": "application/json"}
    data = {
        "consumer_key": consumer_key,
        "redirect_uri": "https://getpocket.com/connected_accounts"
    }
    resp = requests.post(req_token_url, headers=headers, data=data)
    resp.raise_for_status()
    request_token = resp.json()["code"]

    # Step 2: Direct the user to authorize the app in their browser
    auth_url = (
        f"https://getpocket.com/auth/authorize?request_token={request_token}"
        f"&redirect_uri=https://getpocket.com/connected_accounts"
    )
    print("📝 Please authorize this application in your browser...")
    print("🌐 Opening authorization page...")
    webbrowser.open(auth_url)

    # Step 3: Poll for the access token until the user has authorized
    access_token_url = "https://getpocket.com/v3/oauth/authorize"
    data = {
        "consumer_key": consumer_key,
        "code": request_token
    }
    print("⏳ Waiting for authorization... (you can close the browser after authorizing)")
    import time
    while True:
        try:
            resp = requests.post(access_token_url, headers=headers, data=data)
            if resp.status_code == 200:
                access_token = resp.json()["access_token"]
                return access_token
        except Exception:
            pass
        time.sleep(2)  # Try again every 2 seconds

# Returns the current timestamp in Chrome microseconds format as a string
def now_chrome_ts():
    us = int(time.time() * 1_000_000) + EPOCH_OFFSET
    return str(us)

# ====== 1. Fetch Pocket items =====
def fetch_pocket_items():
    # Fetches all items from the user's Pocket account using the API
    url = "https://getpocket.com/v3/get"
    params = {
        "consumer_key": CONSUMER_KEY,
        "access_token": ACCESS_TOKEN,
        "state": "all",
        "detailType": "simple",
        "count": 5000  # Maximum number of items to fetch
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    return list(data.get("list", {}).values())

# ====== 2. Load and backup bookmarks JSON =====
def load_and_backup_bookmarks():
    # Loads the bookmarks file and creates a backup before modifying
    if BOOKMARKS_FILE is None or BACKUP_FILE is None:
        raise ValueError("Bookmarks or backup file path is not set.")
    if not BOOKMARKS_FILE.exists():
        raise FileNotFoundError(f"Bookmarks file not found: {BOOKMARKS_FILE}")
    # Create a backup of the bookmarks file
    shutil.copy2(str(BOOKMARKS_FILE), str(BACKUP_FILE))
    # Load the bookmarks JSON
    with open(str(BOOKMARKS_FILE), "r", encoding="utf-8") as f:
        return json.load(f)

# ====== 3. Create Pocket export folder in bookmarks =====
def create_pocket_folder(bookmarks_json, entries):
    # Inserts a new folder named 'Pocket-Export' into the bookmarks, removing any previous one
    other = bookmarks_json["roots"]["other"]
    # Get or create the list of children (folders and bookmarks)
    children = other.setdefault("children", [])
    # Remove any existing 'Pocket-Export' folder and its bookmarks
    children[:] = [child for child in children if not (child.get("type") == "folder" and child.get("name") == "Pocket-Export")]
    # Create a new folder for Pocket export
    pocket_folder = {
        "type": "folder",
        "name": "Pocket-Export",
        "children": [],
        "date_added": now_chrome_ts(),
        "id": str(int(now_chrome_ts()))  # ID must be unique
    }
    # Add each Pocket item as a bookmark in the new folder
    for item in entries:
        title = item.get("resolved_title") or item.get("given_title") or item.get("item_id")
        url   = item.get("resolved_url") or item.get("given_url")
        if not url:
            continue
        bm = {
            "type": "url",
            "name": title,
            "url": url,
            "date_added": now_chrome_ts(),
            "id": str(int(now_chrome_ts()))
        }
        pocket_folder["children"].append(bm)
    # Add the new Pocket-Export folder to the bookmarks
    children.append(pocket_folder)

# ====== 4. Save updated bookmarks back to file =====
def save_bookmarks(bookmarks_json):
    # Writes the updated bookmarks JSON back to the bookmarks file
    if BOOKMARKS_FILE is None:
        raise ValueError("Bookmarks file path is not set.")
    with open(str(BOOKMARKS_FILE), "w", encoding="utf-8") as f:
        json.dump(bookmarks_json, f, indent=2, ensure_ascii=False)

# ====== Browser selection and OS detection =====
def select_browser():
    # Prompts the user to select which browser to export bookmarks for
    print("Please select the browser for export:")
    print("1) Microsoft Edge")
    print("2) Google Chrome")
    print("3) Mozilla Firefox")
    while True:
        choice = input("Your choice (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")

def detect_os_and_browser():
    # Detects the user's operating system and suggests a browser based on the OS
    os_name = platform.system().lower()
    
    # Determine default browser based on OS
    if "darwin" in os_name:
        # macOS
        print("Detected operating system: macOS")
        default_choice = "1"  # Microsoft Edge
        default_browser = "Microsoft Edge"
    elif "win" in os_name:
        # Windows
        print("Detected operating system: Windows")
        default_choice = "1"  # Microsoft Edge
        default_browser = "Microsoft Edge"
    elif "linux" in os_name:
        # Linux
        print("Detected operating system: Linux")
        default_choice = "2"  # Google Chrome
        default_browser = "Google Chrome"
    else:
        print("Operating system not recognized.")
        return select_browser()
    
    # Ask user to confirm or choose a different browser
    print(f"Recommended browser for your system: {default_browser}")
    print("Please select the browser for export:")
    print("1) Microsoft Edge")
    print("2) Google Chrome")
    print("3) Mozilla Firefox")
    print(f"Press Enter for default ({default_browser}) or choose 1/2/3:")
    
    while True:
        choice = input("Your choice: ").strip()
        if choice == "":
            # User pressed Enter, use default
            return default_choice
        elif choice in ("1", "2", "3"):
            return choice
        else:
            print("Invalid input. Please enter 1, 2, 3, or press Enter for default.")

# ====== Main execution flow ======
def main():
    print("="*60)
    print("🚀 POCKET TO BROWSER BOOKMARKS EXPORTER")
    print("="*60)
    print("This script exports your Pocket saved articles to your browser bookmarks.")
    print("Your bookmarks will be organized in a 'Pocket-Export' folder.")
    print("="*60)
    
    # Step 0a: Get Pocket consumer key (interactive)
    global CONSUMER_KEY
    if not CONSUMER_KEY:
        CONSUMER_KEY = get_pocket_consumer_key()
        print("✅ Consumer Key received successfully!")
    
    # Step 0b: Get Pocket access token (interactive)
    global ACCESS_TOKEN
    if not ACCESS_TOKEN:
        print("\n🔐 Authenticating with Pocket...")
        try:
            ACCESS_TOKEN = get_pocket_access_token(CONSUMER_KEY)
            print("✅ Access Token obtained successfully!")
        except requests.exceptions.HTTPError as e:
            if "400" in str(e) or "403" in str(e):
                print("❌ Invalid Consumer Key. Please check your Consumer Key and try again.")
                print("   Make sure you copied the entire Consumer Key from the Pocket developer page.")
                return
            else:
                print(f"❌ HTTP Error: {e}")
                return
        except Exception as e:
            print(f"❌ Error obtaining access token: {e}")
            return

    # Step 1: Fetch items from Pocket
    print("Fetching items from Pocket...")
    items = fetch_pocket_items()
    print(f"Fetched {len(items)} items from Pocket.")

    # Step 2: Load and backup current bookmarks
    print("Loading and backing up current bookmarks...")
    global BOOKMARKS_FILE, BACKUP_FILE
    browser_choice = detect_os_and_browser()
    if browser_choice == "1":
        # Microsoft Edge
        BOOKMARKS_FILE = EDGE_PROFILE / "Bookmarks"
        BACKUP_FILE    = EDGE_PROFILE / "Bookmarks.bak"
    elif browser_choice == "2":
        # Google Chrome
        if platform.system().lower() == "darwin":
            # macOS
            BOOKMARKS_FILE = Path.home() / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Bookmarks"
        else:
            # Linux/Windows
            BOOKMARKS_FILE = Path.home() / ".config" / "google-chrome" / "Default" / "Bookmarks"
        BACKUP_FILE    = BOOKMARKS_FILE.with_suffix(".bak")
    elif browser_choice == "3":
        # Mozilla Firefox
        BOOKMARKS_FILE = Path.home() / ".mozilla" / "firefox" / "*.default-release" / "bookmarks.json"
        BACKUP_FILE    = BOOKMARKS_FILE.with_suffix(".bak")
    else:
        print("Invalid browser choice. Exiting.")
        return

    try:
        bookmarks_json = load_and_backup_bookmarks()
    except Exception as e:
        print(f"Error loading bookmarks: {e}")
        return

    # Step 3: Create Pocket export folder in bookmarks
    print("Creating Pocket export folder in bookmarks...")
    try:
        create_pocket_folder(bookmarks_json, items)
    except Exception as e:
        print(f"Error creating Pocket folder: {e}")
        return

    # Step 4: Save updated bookmarks back to file
    print("Saving updated bookmarks...")
    try:
        save_bookmarks(bookmarks_json)
    except Exception as e:
        print(f"Error saving bookmarks: {e}")
        return

    print("✅ Pocket items exported to browser bookmarks successfully!")
    print("Restart the browser now to reload the bookmarks.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(5)  # Pause before exiting
