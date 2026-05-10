import time
import requests
from config import HEADERS, BASE_URL, POLL_INTERVAL, GROUP_ROOM_ID, DIRECT_ROOM_ID
from webex import get_messages, send_message
from screenshots import take_screenshot

def get_bot_email():
    response = requests.get(f"{BASE_URL}/people/me", headers=HEADERS)
    return response.json().get("emails", [None])[0]

def handle_command(room_id, text):
    text = text.lower().strip()

    if text == "ping":
        send_message(room_id, "pong")

    elif text.startswith("screenshot window"):
        window_name = text.replace("screenshot window", "").strip()
        print(f"Taking screenshot of: {window_name}")
        filename, error = take_screenshot(window_name)
        print(f"Filename: {filename}, Error: {error}")
        if error:
            send_message(room_id, f"Error: {error}")
        else:
            print("Sending file...")
            status = send_message(room_id, file_path=filename)
            print(f"Send status: {status}")

    elif text.startswith("screenshot web"):
        url = text.replace("screenshot web", "").strip()
        filename, error = take_screenshot("web", url=url)
        if error:
            send_message(room_id, f"Error: {error}")
        else:
            send_message(room_id, file_path=filename)

    else:
        send_message(room_id, "Unknown command.")

def main():
    print("Bot starting...")
    bot_email = get_bot_email()
    print(f"Bot email: {bot_email}")

    last_message_id = None
    messages = get_messages(DIRECT_ROOM_ID)
    if messages:
        last_message_id = messages[0]["id"]

    print("Listening for commands...")

    while True:
        new_messages = get_messages(DIRECT_ROOM_ID, last_message_id)
        if new_messages:
            last_message_id = new_messages[0]["id"]
            for msg in reversed(new_messages):
                # skip bot's own messages
                if msg.get("personEmail") == bot_email:
                    continue
                text = msg.get("text", "")
                print(f"Received: {text}")
                handle_command(GROUP_ROOM_ID, text)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()