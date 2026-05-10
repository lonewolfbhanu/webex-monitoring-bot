# config.py
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ROOM_ID = os.getenv("GROUP_ROOM_ID")
DIRECT_ROOM_ID = os.getenv("DIRECT_ROOM_ID")

HEADERS = {
    "Authorization": f"Bearer {BOT_TOKEN}",
    "Content-Type": "application/json"
}

BASE_URL = "https://webexapis.com/v1"
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 5))
SCREENSHOT_INTERVAL = int(os.getenv("SCREENSHOT_INTERVAL", 300))