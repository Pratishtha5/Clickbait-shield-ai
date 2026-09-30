"""
ClickBait Shield AI — One-Click Launcher Script
Run with: python run.py
"""
import sys
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("  ClickBait Shield AI — Explainable ML Forensics Platform")
    print("  Python Engine: Active (Python " + sys.version.split()[0] + ")")
    print("  Server: http://127.0.0.1:8000")
    print("  REST API Docs: http://127.0.0.1:8000/docs")
    print("  Chrome Extension Folder: ./chrome-extension")
    print("=" * 60)
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
