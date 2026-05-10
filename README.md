# Webex Monitoring Bot

A Python-based Webex bot that takes on-demand screenshots of applications and webpages and posts them to a Webex chatroom. Built for monitoring workflows in operations and production support environments.

---

## Features

- **On-demand window screenshots** — capture any open application by name
- **On-demand webpage screenshots** — capture any URL using headless Chromium
- **Posts to Webex group room** — screenshots delivered directly to your team's chatroom
- **Command interface via Direct Message** — send commands privately, results appear in group room

---

## Architecture

```
User (DM) ──► Bot polls DM ──► Executes command ──► Posts result to Group Room
```

### Why polling over webhooks?
Webhooks require a publicly accessible URL to receive events. Since this bot runs locally without a hosted server, polling is used instead — the bot makes outbound API calls every 5 seconds to check for new commands. In a production deployment, this would be replaced with webhooks for lower latency and fewer API calls.

### Why Direct Message for commands?
Webex restricts bots from reading group room messages via polling (returns 403). Commands are sent via DM to the bot, and results are posted to the group room — clean separation between input and output.

---

## Tech Stack

| Component | Library |
|---|---|
| Webex API | `requests` |
| Window screenshots | `mss` + `pygetwindow` |
| Webpage screenshots | `playwright` (headless Chromium) |
| Scheduling | `schedule` |
| Config management | `python-dotenv` |

---

## Project Structure

```
webex-monitoring-bot/
├── bot.py            — main loop, command router
├── config.py         — loads environment variables
├── webex.py          — Webex API: send/receive messages
├── screenshots.py    — window and browser screenshot logic
├── .env.example      — template for environment variables
└── screenshots/      — auto-created, stores captured images
```

---

## Setup

### 1. Clone the repo
```
git clone https://github.com/lonewolfbhanu/webex-monitoring-bot.git
cd webex-monitoring-bot
```

### 2. Install dependencies
```
pip install requests Pillow pygetwindow pywin32 mss schedule playwright python-dotenv
playwright install chromium
```

### 3. Create a Webex Bot
- Go to [developer.webex.com](https://developer.webex.com)
- Sign in → My Webex Apps → Create a Bot
- Copy the **Bot Access Token**

### 4. Get Room IDs
Add the bot to your Webex rooms, then run:
```python
import requests
r = requests.get("https://webexapis.com/v1/rooms", headers={"Authorization": "Bearer YOUR_TOKEN"})
print(r.json())
```

### 5. Configure environment
```
cp .env.example .env
```
Fill in your `.env`:
```
BOT_TOKEN=your_bot_token_here
GROUP_ROOM_ID=your_group_room_id_here
DIRECT_ROOM_ID=your_direct_room_id_here
POLL_INTERVAL=5
SCREENSHOT_INTERVAL=300
```

### 6. Run
```
python bot.py
```

---

## Commands

Send these via **Direct Message** to the bot:

| Command | Description |
|---|---|
| `ping` | Health check — bot replies `pong` in group room |
| `screenshot window Notepad` | Screenshots any open app window by name |
| `screenshot window Brave` | Works for GPU-rendered apps (Chromium, VS Code, etc.) |
| `screenshot web https://example.com` | Screenshots any URL in headless browser |

---

## Screenshot Implementation Notes

### Window capture — why `mss` over `win32gui`?
Modern applications like VS Code and Brave use GPU compositing — they render directly to the GPU and bypass GDI entirely. Standard Windows capture APIs (`BitBlt`, `PrintWindow`) operate at the GDI layer and return blank images for these apps. `mss` captures the screen buffer directly, which includes GPU-rendered content and works for all application types.

### Webpage capture — why Playwright over requests?
`requests` fetches raw HTML only. Modern dashboards (Airflow, Grafana, etc.) are JavaScript-rendered — the content doesn't exist in raw HTML. Playwright runs a real headless Chromium instance, executes JavaScript, and screenshots the fully rendered page.

---

## Planned Upgrades

- [ ] **Webhooks** — replace polling with event-driven webhooks via ngrok for group room command support
- [ ] **Scheduler** — periodic automatic screenshots at configurable intervals
- [ ] **Email alerts** — Gmail IMAP monitoring, forward alerts to Webex group room

---

## Requirements

- Windows (screenshot capture uses Windows APIs)
- Python 3.8+
- Webex account (personal or enterprise)
- Outlook or Gmail account (for email alert feature — coming soon)
