# Screenshots & Mockups — Mission Journey Tracker

This folder contains a Streamlit prototype and a small utility script to produce PNG mockups for an executive slide deck.

Files included:
- streamlit_app.py — Streamlit prototype (UI wireframe with placeholder data)
- capture_screenshots.py — script that starts the Streamlit app and captures screenshots using Playwright
- requirements.txt — Python dependencies

How to produce the static PNG mockups
1. Clone the repo locally (or use the GitHub web UI to download files).
2. Create a Python venv (recommended) and install dependencies:
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
3. Install Playwright browsers (one-time):
   playwright install

4. Run the capture script (it will start the Streamlit app and save screenshots into ./screenshots/):
   python capture_screenshots.py

5. Inspect the PNGs in the screenshots folder. Use these images in your executive slide deck.

Notes & tips
- If port 8501 is in use, change STREAMLIT_PORT in capture_screenshots.py to an available port.
- For higher-fidelity slides, run the Streamlit app in your browser and use your OS's screenshot tool to capture exactly the layout you prefer.
- To produce translation of comments or redact PII, add cleaning steps in the app code before rendering.

If you want, I can push sample exported PNGs to the repo after you run the script and share the screenshots, or I can create slide-ready PNGs myself and add them to the repo if you give me permission to run the app and capture images remotely.