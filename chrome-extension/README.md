# ClickBait Shield AI — Chrome Extension (Manifest V3)

Real-time, explainable AI clickbait detection directly in your web browser.

## Features
- **Instant Popup Scanner**: Analyze any headline or auto-grab the current browser tab title.
- **In-Page Real-Time Badge**: Automatically detects sensational headlines on YouTube, Reddit, and news sites, adding a discreet risk badge (`⚠️ 94% BAIT`).
- **Right-Click Context Menu**: Select any text on any webpage -> Right-click -> *Analyze Clickbait with Shield AI*.
- **Direct Connection to Local Python Engine**: Connects to the FastAPI backend at `http://localhost:8000/api/analyze`.
- **Offline Resilient**: Automatically falls back to lightweight edge heuristic scoring if the local Python server is temporarily offline.

## Installation Instructions (Takes 30 Seconds)
1. Open Google Chrome (or Microsoft Edge / Brave).
2. Navigate to `chrome://extensions` in the address bar.
3. In the top-right corner, toggle on **Developer mode**.
4. Click the **Load unpacked** button in the top-left corner.
5. Select this `chrome-extension` folder.
6. The ClickBait Shield AI icon will now appear in your browser toolbar! Pin it for quick access.
