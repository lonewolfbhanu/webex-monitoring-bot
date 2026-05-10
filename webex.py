# webex.py

import requests
from config import HEADERS, BASE_URL

def get_messages(room_id, last_message_id=None):
    params = {
        "roomId": room_id,
        "max": 10
    }
    response = requests.get(f"{BASE_URL}/messages", headers=HEADERS, params=params)
    messages = response.json().get("items", [])
    
    if last_message_id:
        # only return messages newer than last seen
        new_messages = []
        for msg in messages:
            if msg["id"] == last_message_id:
                break
            new_messages.append(msg)
        return new_messages
    
    return messages

import os

def send_message(room_id, text=None, file_path=None):
    if file_path:
        with open(file_path, "rb") as f:
            files = {
                "files": (os.path.basename(file_path), f, "image/png")
            }
            data = {"roomId": room_id}
            headers = {"Authorization": HEADERS["Authorization"]}
            response = requests.post(f"{BASE_URL}/messages", headers=headers, data=data, files=files)
            print(f"File upload response: {response.json()}")
    else:
        payload = {"roomId": room_id, "text": text}
        response = requests.post(f"{BASE_URL}/messages", headers=HEADERS, json=payload)

    return response.status_code
    
    return response.status_code

def get_room_id(room_name):
    response = requests.get(f"{BASE_URL}/rooms", headers=HEADERS)
    rooms = response.json().get("items", [])
    print(f"Rooms found: {[r['title'] for r in rooms]}")
    for room in rooms:
        if room_name.lower() in room["title"].lower():
            return room["id"]
    return None