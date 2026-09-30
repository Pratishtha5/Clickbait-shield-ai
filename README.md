# ClickBait Shield AI 🛡️

A simple, lightweight, and explainable **Python Machine Learning & Deep Learning system** that detects clickbait headlines and extracts mathematical token saliency in real time.

Trained and evaluated on the real **[`christinacdl/clickbait_detection_dataset`](https://huggingface.co/datasets/christinacdl/clickbait_detection_dataset)** from Hugging Face (**37,870 labeled samples**).

---

## 🤖 5 Model Architectures

1. **Linear Regression (Regularized Ridge)**: Fast, continuous hyperplane scoring minimizing squared error (`95.35%` test accuracy).
2. **Logistic Regression**: Maximum-likelihood estimation with calibrated odds ratios and transparent feature attribution coefficients (`94.93%` test accuracy).
3. **K-Means Clustering**: Prototype cluster centroid alignment measuring cosine similarity against clickbait vs legitimate cluster centroids (`65.49%` test accuracy).
4. **Random Forest Ensemble**: Non-linear bagging ensemble of decision trees capturing complex multi-word correlations (`88.49%` test accuracy).
5. **1D Convolutional Neural Network (1D CNN)**: Word embeddings with spatial bigram convolutions, ReLU activations, global max-pooling, and dense Sigmoid classifier (`94.22%` test accuracy).

---

## 🧩 Complete Chrome Extension (Manifest V3)

The `chrome-extension/` directory is a production-ready browser extension:

- **Interactive Popup Scanner**:
  - Auto-grabs the active tab's headline.
  - Live breakdown showing predictions from **Linear Regression, Logistic Regression, KMeans, Random Forest, and 1D CNN**.
  - Visual token saliency heatmap highlighting clickbait triggers vs factual anchors.
  - Test presets to verify headlines with one click.
  - Direct link to open the Full Forensic Studio and print export.
  - Offline-resilient fallback if the local Python server is offline.
- **In-Page Real-Time Scanner (`content.js`)**:
  - Automatically identifies headlines on YouTube, Reddit, X (Twitter), News sites, and Medium.
  - Injects discreet risk badges (`🛡️ 94% BAIT` or `🛡️ 95% SAFE`).
  - Automatically verifies against the local Python server when active.
  - MutationObserver handles dynamic infinite-scroll feeds.
- **Background Worker (`background.js`)**:
  - Right-click context menu: highlight any text on any page -> *🛡️ Analyze Clickbait with Shield AI*.
  - Dynamic badge counter on the extension icon indicating the number of clickbaits detected on the current tab.

### Loading the Extension
1. Open Chrome / Edge / Brave and go to `chrome://extensions/`.
2. Enable **Developer mode** (top right toggle).
3. Click **Load unpacked** and select the `chrome-extension/` folder in this repository.
4. Pin the Shield AI icon to your toolbar!

---

## 📁 Project Structure

```
clickbait-shield-ai/
├── app.py                     # FastAPI web server and REST API
├── run.py                     # One-click launcher script
├── train.py                   # Self-contained training script for the 5 models
├── predict.py                 # Terminal CLI headline predictor
├── requirements.txt           # Minimal Python dependencies
├── data/
│   ├── train.json             # Cached Hugging Face training set (30,296 items)
│   ├── test.json              # Cached Hugging Face test set (3,787 items)
│   ├── model_bundle.joblib    # Persisted trained models & vectorizer
│   └── benchmark_metrics.json # Real test evaluation metrics
├── engine/
│   ├── models.py              # Multi-model inference & consensus engine
│   ├── custom_models.py       # 1D CNN & KMeansClassifier architectures
│   ├── saliency.py            # Mathematical token attribution
│   ├── tokenizer.py           # Lexical & syntactic feature extractor
│   ├── benchmark_data.py      # Benchmark loader
│   ├── sample_headlines.py    # Curated test presets
│   └── types_data.py          # Pydantic schemas
├── templates/
│   ├── index.html             # Web dashboard
│   └── print_report.html      # Print dossier
├── static/
│   ├── css/style.css
│   └── js/app.js
└── chrome-extension/          # Ready-to-load Chrome browser extension
    ├── manifest.json          # Manifest V3 configuration
    ├── popup.html             # Extension popup UI
    ├── popup.css              # Popup styling
    ├── popup.js               # Popup controller
    ├── content.js             # In-page feed scanner & badge injector
    ├── content.css            # In-page badge styling
    ├── background.js          # Service worker & context menu
    └── icons/                 # Extension icons (16px, 48px, 128px)
```

---

## ⚡ Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Models (Linear, Logistic, KMeans, RF, 1D CNN)
```bash
python train.py
```

### 3. Terminal Prediction
```bash
python predict.py "15 Shocking Secrets Flight Attendants Don't Want You To Know"
python predict.py "Federal Reserve Cuts Benchmark Interest Rates by 25 Basis Points"
```

### 4. Launch Web Studio
```bash
python run.py
```
- **Web App**: http://127.0.0.1:8000
- **Swagger API Docs**: http://127.0.0.1:8000/docs
- **1-Click Extension Zip Download**: http://127.0.0.1:8000/api/download-extension
