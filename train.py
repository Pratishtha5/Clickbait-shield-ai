"""
ClickBait Shield AI — Model Training Pipeline
Trains 5 distinct ML/DL architectures on christinacdl/clickbait_detection_dataset:
1. Linear Regression (Regularized L2 Ridge Regression)
2. Logistic Regression (L2-calibrated maximum likelihood baseline)
3. K-Means Clustering (Centroid Prototype Clustering)
4. Random Forest (Ensemble of Decision Trees)
5. 1D Convolutional Neural Network (Spatial n-gram Conv1D + Max-Pooling + Dense Sigmoid)
"""
import os
import re
import json
import time
import urllib.request
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.cluster import MiniBatchKMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, matthews_corrcoef, confusion_matrix
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
TRAIN_URL = "https://huggingface.co/datasets/christinacdl/clickbait_detection_dataset/raw/main/train.json"
TEST_URL = "https://huggingface.co/datasets/christinacdl/clickbait_detection_dataset/raw/main/test.json"

TRAIN_FILE = os.path.join(DATA_DIR, "train.json")
TEST_FILE = os.path.join(DATA_DIR, "test.json")
MODEL_FILE = os.path.join(DATA_DIR, "model_bundle.joblib")
METRICS_FILE = os.path.join(DATA_DIR, "benchmark_metrics.json")


from engine.custom_models import Conv1DModel, KMeansClassifier, clean_tokenize


def download_dataset():
    """Downloads dataset from Hugging Face if not already present."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path, url in [(TRAIN_FILE, TRAIN_URL), (TEST_FILE, TEST_URL)]:
        if not os.path.exists(path):
            print(f"Downloading {os.path.basename(path)} from Hugging Face...")
            urllib.request.urlretrieve(url, path)
            print(f"Saved {path}")


def load_data():
    """Loads train and test splits."""
    download_dataset()
    with open(TRAIN_FILE, "r", encoding="utf-8") as f:
        train_data = json.load(f)
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    X_train = [d["text"] for d in train_data]
    y_train = [int(d["label"]) for d in train_data]
    X_test = [d["text"] for d in test_data]
    y_test = [int(d["label"]) for d in test_data]

    return X_train, y_train, X_test, y_test


def train_and_evaluate():

    """Trains the 5 user-requested architectures on the real dataset."""
    print("=" * 70)
    print("ClickBait Shield AI — Multi-Model Training Pipeline")
    print("Architectures: Linear Regression, Logistic Regression, KMeans, Random Forest, 1D CNN")
    print("Dataset: christinacdl/clickbait_detection_dataset (Hugging Face)")
    print("=" * 70)

    X_train, y_train, X_test, y_test = load_data()
    print(f"Loaded: {len(X_train):,} train headlines, {len(X_test):,} test headlines")

    # 1. Feature Extraction: TF-IDF
    t0 = time.time()
    vec = TfidfVectorizer(ngram_range=(1, 2), max_features=25000, sublinear_tf=True)
    X_tr = vec.fit_transform(X_train)
    X_te = vec.transform(X_test)
    print(f"TF-IDF fitted in {time.time() - t0:.2f}s ({len(vec.vocabulary_):,} vocabulary features)")

    # 2. Build Vocabulary for 1D CNN
    counts = {}
    for text in X_train:
        for w in clean_tokenize(text):
            counts[w] = counts.get(w, 0) + 1

    cnn_vocab = {"<pad>": 0, "<unk>": 1}
    for w, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:8000]:
        cnn_vocab[w] = len(cnn_vocab)

    # 3. Instantiate Models
    models = {
        "linear_reg": {
            "name": "Linear Regression",
            "category": "Regularized Linear (Ridge)",
            "model": Ridge(alpha=1.0, random_state=42),
            "is_custom": False,
            "strengths": "Direct squared error minimization; fast linear regression hyperplane boundary.",
            "weaknesses": "Unbounded predictions requiring range clipping to [0, 1].",
            "hyperparameters": {"alpha": 1.0, "solver": "auto", "loss": "squared_error"}
        },
        "logistic_reg": {
            "name": "Logistic Regression",
            "category": "Maximum Likelihood Linear",
            "model": LogisticRegression(C=2.5, max_iter=1000, random_state=42),
            "is_custom": False,
            "strengths": "Well-calibrated log-odds, transparent feature attribution coefficients.",
            "weaknesses": "Assumes linear additivity among input word features.",
            "hyperparameters": {"C": 2.5, "max_iter": 1000, "solver": "lbfgs"}
        },
        "kmeans": {
            "name": "K-Means Clustering",
            "category": "Centroid Prototype Clustering",
            "model": KMeansClassifier(n_clusters=2, random_state=42),
            "is_custom": True,
            "strengths": "Geometric prototype alignment; non-parametric centroid proximity scoring.",
            "weaknesses": "Sensitive to cluster center initialization and high-dimensional sparsity.",
            "hyperparameters": {"n_clusters": 2, "metric": "cosine_centroid", "batch_size": 2048}
        },
        "random_forest": {
            "name": "Random Forest",
            "category": "Tree Ensemble",
            "model": RandomForestClassifier(n_estimators=50, max_depth=15, n_jobs=-1, random_state=42),
            "is_custom": False,
            "strengths": "Bagging ensemble resistant to overfitting; captures non-linear word interactions.",
            "weaknesses": "Requires higher memory footprint to serialize multiple decision trees.",
            "hyperparameters": {"n_estimators": 50, "max_depth": 15, "criterion": "gini"}
        },
        "1d_cnn": {
            "name": "1D Convolutional Neural Network",
            "category": "Deep Learning (Conv1D + Pooling)",
            "model": Conv1DModel(vocab=cnn_vocab, embedding_dim=32, num_filters=48, max_len=20),
            "is_custom": True,
            "strengths": "Spatial sequence n-gram convolutions with global max-pooling over word order.",
            "weaknesses": "Fixed maximum token sequence length truncation.",
            "hyperparameters": {"embedding_dim": 32, "filter_size": 2, "num_filters": 48, "max_len": 20}
        }
    }

    trained_models = {}
    benchmark_metrics = []
    y_test_arr = np.array(y_test)

    print("-" * 70)
    print(f"{'Model':<32} | {'Acc (%)':<8} | {'F1 (%)':<8} | {'Latency':<8}")
    print("-" * 70)

    for mid, cfg in models.items():
        clf = cfg["model"]
        t_start = time.time()

        if mid == "1d_cnn":
            clf.fit(X_train, y_train)
        elif mid == "kmeans":
            clf.fit(X_tr, y_train)
        else:
            clf.fit(X_tr, y_train)

        fit_time = time.time() - t_start

        # Inference on test set
        t_infer = time.time()
        if mid == "1d_cnn":
            probs = clf.predict_proba(X_test)[:, 1]
            preds = (probs >= 0.5).astype(int)
        elif mid == "kmeans":
            probs = clf.predict_proba(X_te)[:, 1]
            preds = (probs >= 0.5).astype(int)
        elif mid == "linear_reg":
            raw_preds = clf.predict(X_te)
            probs = np.clip(raw_preds, 0.01, 0.99)
            preds = (probs >= 0.5).astype(int)
        else:
            probs = clf.predict_proba(X_te)[:, 1]
            preds = clf.predict(X_te)

        infer_latency_ms = round(((time.time() - t_infer) / len(X_test)) * 1000, 3)

        acc = float(accuracy_score(y_test_arr, preds)) * 100
        prec = float(precision_score(y_test_arr, preds, zero_division=0)) * 100
        rec = float(recall_score(y_test_arr, preds, zero_division=0)) * 100
        f1 = float(f1_score(y_test_arr, preds, zero_division=0)) * 100
        auc = float(roc_auc_score(y_test_arr, probs))
        mcc = float(matthews_corrcoef(y_test_arr, preds))

        cm = confusion_matrix(y_test_arr, preds)
        tn, fp, fn, tp = cm.ravel()
        specificity = float((tn / (tn + fp)) * 100) if (tn + fp) > 0 else 0.0

        trained_models[mid] = clf

        metric_record = {
            "id": mid,
            "name": cfg["name"],
            "category": cfg["category"],
            "accuracy": round(acc, 2),
            "precision": round(prec, 2),
            "recall": round(rec, 2),
            "f1_score": round(f1, 2),
            "latency_ms": max(0.5, infer_latency_ms),
            "roc_auc": round(auc, 3),
            "mcc": round(mcc, 3),
            "specificity": round(specificity, 2),
            "confusion_matrix": {
                "tp": int(tp),
                "fp": int(fp),
                "fn": int(fn),
                "tn": int(tn),
                "total": int(len(y_test))
            },
            "strengths": cfg["strengths"],
            "weaknesses": cfg["weaknesses"],
            "hyperparameters": cfg["hyperparameters"]
        }
        benchmark_metrics.append(metric_record)

        print(f"{cfg['name']:<32} | {acc:<8.2f} | {f1:<8.2f} | {infer_latency_ms:<8.3f} ms")

    # Logistic Regression feature weights for saliency
    lr_model = trained_models["logistic_reg"]
    feature_names = np.array(vec.get_feature_names_out())
    coefs = lr_model.coef_[0]

    # Save artifacts
    bundle = {
        "vectorizer": vec,
        "models": trained_models,
        "feature_names": feature_names,
        "lr_coefs": coefs,
        "model_configs": models,
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "dataset": "christinacdl/clickbait_detection_dataset"
    }

    joblib.dump(bundle, MODEL_FILE, compress=3)
    print("-" * 70)
    print(f"Saved model bundle: {MODEL_FILE}")

    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(benchmark_metrics, f, indent=2)
    print(f"Saved benchmark metrics: {METRICS_FILE}")
    print("=" * 70)
    print("Training complete! Linear Regression, Logistic Regression, KMeans, Random Forest & 1D CNN active.")


if __name__ == "__main__":
    train_and_evaluate()
