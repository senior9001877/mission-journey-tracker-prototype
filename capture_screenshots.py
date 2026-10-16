"""
capture_screenshots.py

Utility to launch the Streamlit prototype locally and capture static PNG screenshots of key areas
for use in an executive slide deck.

Usage (after installing requirements):
1. Install Playwright browsers: playwright install
2. Run: python capture_screenshots.py

The script will:
- Start the Streamlit app (streamlit_app.py) on port 8501
- Wait until the server is reachable
- Use Playwright to open the page and save a set of screenshots under ./screenshots/
- Stop the Streamlit process

Note: Playwright must be installed and its browsers installed (playwright install). On first run Playwright
may download browser binaries.
"""

import subprocess
import time
import os
import requests
from playwright.sync_api import sync_playwright

STREAMLIT_PORT = 8501
STREAMLIT_URL = f"http://127.0.0.1:{STREAMLIT_PORT}"
SCREENSHOT_DIR = "screenshots"

def start_streamlit():
    # Start Streamlit in a subprocess
    cmd = ["streamlit", "run", "streamlit_app.py", "--server.port", str(STREAMLIT_PORT)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p

def wait_for_server(url, timeout=30):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def capture_screenshots():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto(STREAMLIT_URL, wait_until="networkidle")
        time.sleep(1)
        # Full page screenshot
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "full_page.png"), full_page=True)
        # Try to capture the funnel plot area by selecting the first Plotly figure
        try:
            # streamlit renders plotly charts in <div role="figure"> — capture center area
            page.locator("div[role=figure]").first.screenshot(path=os.path.join(SCREENSHOT_DIR, "funnel.png"))
        except Exception:
            pass
        # Capture right column by cropping center-right region
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "drivers_right.png"), clip={"x": 850, "y": 180, "width": 520, "height": 760})
        # Capture worst step card bottom area by scrolling near bottom and screenshot
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "worst_step.png"))
        browser.close()

if __name__ == '__main__':
    print("Starting Streamlit app...")
    p = start_streamlit()
    print("Waiting for Streamlit to be ready...")
    ok = wait_for_server(STREAMLIT_URL, timeout=40)
    if not ok:
        print("Streamlit did not start in time. Check streamlit installation and that port is free.")
        p.terminate()
        exit(1)
    print("Streamlit is up — capturing screenshots...")
    try:
        capture_screenshots()
        print(f"Screenshots saved to ./{SCREENSHOT_DIR}/")
    finally:
        print("Stopping Streamlit app...")
        p.terminate()
