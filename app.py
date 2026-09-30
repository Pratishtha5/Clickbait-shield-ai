"""
ClickBait Shield AI — Python FastAPI Application
Serving explainable multi-model headline forensics, REST API, print reports, and Chrome extension downloads.
"""
import io
import os
import zipfile
from typing import List
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse

from engine.types_data import HeadlineRequest, BatchHeadlineRequest
from engine.models import evaluate_headline_consensus
from engine.benchmark_data import load_benchmark_metrics
from engine.sample_headlines import SAMPLE_HEADLINES

app = FastAPI(
    title="ClickBait Shield AI",
    description="Explainable Multi-Model Headline Forensic & Verification System",
    version="2.0.0"
)

# Enable CORS for Chrome Extension & local browser communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and template directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, headline: str = ""):
    """Renders the main simple, modern ClickBait Shield AI Web UI."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "prefilled_headline": headline,
            "sample_headlines": SAMPLE_HEADLINES
        }
    )

@app.post("/api/analyze")
async def analyze_headline(req: HeadlineRequest):
    """Analyzes a headline across all 5 models and returns transparent explainability data."""
    text = req.headline.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Headline text cannot be empty")
    verdict = evaluate_headline_consensus(text)
    return verdict

@app.post("/api/batch")
async def batch_analyze(req: BatchHeadlineRequest):
    """Batch analysis endpoint for processing multiple headlines."""
    cleaned = [h.strip() for h in req.headlines if h.strip()]
    if not cleaned:
        raise HTTPException(status_code=400, detail="At least one valid headline required")
    
    results = [evaluate_headline_consensus(h) for h in cleaned[:50]]
    total = len(results)
    clickbait_count = sum(1 for r in results if r.is_clickbait)
    avg_score = round(sum(r.consensus_score for r in results) / max(1, total), 1)

    return {
        "total": total,
        "clickbait_count": clickbait_count,
        "legitimate_count": total - clickbait_count,
        "average_risk_score": avg_score,
        "results": results
    }

@app.get("/api/benchmarks")
async def get_benchmarks():
    """Returns comparative benchmark telemetry across 37,000+ labeled samples."""
    return load_benchmark_metrics()

@app.get("/api/samples")
async def get_samples():
    """Returns curated sample test headlines."""
    return SAMPLE_HEADLINES

@app.get("/api/health")
async def health_check():
    """Health status endpoint."""
    return {
        "status": "healthy",
        "service": "ClickBait Shield AI",
        "version": "2.0.0",
        "engine": "Python 3.14 Multi-Model Neural Consensus",
        "models_active": 5
    }

@app.get("/print", response_class=HTMLResponse)
async def print_report(request: Request, headline: str = "You Won't Believe What She Looked Like After Drinking Celery Juice For 30 Days!"):
    """Renders a dedicated, print-optimized document view for instant printing / PDF export."""
    verdict = evaluate_headline_consensus(headline)
    return templates.TemplateResponse(
        request=request,
        name="print_report.html",
        context={"verdict": verdict}
    )

@app.get("/api/download-extension")
async def download_extension():
    """Dynamically bundles the chrome-extension directory into a zip for immediate 1-click download."""
    ext_dir = os.path.join(BASE_DIR, "chrome-extension")
    if not os.path.exists(ext_dir):
        raise HTTPException(status_code=404, detail="Extension directory not found")

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(ext_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, ext_dir)
                zip_file.write(abs_path, rel_path)

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=clickbait-shield-ai-extension.zip"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
