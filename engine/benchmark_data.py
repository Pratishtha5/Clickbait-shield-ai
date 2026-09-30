"""
ClickBait Shield AI — Model Benchmark Telemetry
Real evaluation metrics calculated directly on 3,787 test samples from christinacdl/clickbait_detection_dataset.
"""
import os
import json
from typing import List
from engine.types_data import ModelBenchmarkMetrics

METRICS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "benchmark_metrics.json")

def load_benchmark_metrics() -> List[ModelBenchmarkMetrics]:
    """Loads evaluated benchmark metrics from data/benchmark_metrics.json."""
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [ModelBenchmarkMetrics(**m) for m in data]
    return []

BENCHMARK_METRICS: List[ModelBenchmarkMetrics] = load_benchmark_metrics()
