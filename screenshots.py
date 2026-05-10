# screenshots.py

import pygetwindow as gw
import mss
import mss.tools
import asyncio
from playwright.async_api import async_playwright
import time
import os

SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def screenshot_window(window_name):
    windows = gw.getWindowsWithTitle(window_name)

    if not windows:
        return None, f"No window found with name '{window_name}'"

    window = windows[0]

    if window.isMinimized:
        window.restore()
        time.sleep(0.5)

    window.maximize()
    time.sleep(0.5)

    webex_windows = gw.getWindowsWithTitle("Webex")
    for w in webex_windows:
        try:
            w.minimize()
        except:
            pass

    try:
        window.activate()
    except:
        pass

    time.sleep(1.5)

    windows = gw.getWindowsWithTitle(window_name)
    window = windows[0]

    with mss.mss() as sct:
        monitor = {
            "top": window.top,
            "left": window.left,
            "width": window.width,
            "height": window.height
        }
        screenshot = sct.grab(monitor)
        filename = f"{SCREENSHOTS_DIR}/{window_name.replace(' ', '_')}_{int(time.time())}.png"
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)

    for w in webex_windows:
        try:
            w.restore()
        except:
            pass

    return filename, None

async def screenshot_webpage(url, filter_input=None, filter_selector=None):
    filename = f"{SCREENSHOTS_DIR}/web_{int(time.time())}.png"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        await page.goto(url, wait_until="networkidle")

        if filter_input and filter_selector:
            await page.fill(filter_selector, filter_input)
            await page.wait_for_timeout(1500)

        await page.screenshot(path=filename, full_page=True)
        await browser.close()

    return filename, None

def take_screenshot(target, url=None, filter_input=None, filter_selector=None):
    if target == "web":
        return asyncio.run(screenshot_webpage(url, filter_input, filter_selector))
    else:
        return screenshot_window(target)