"""
ClickBait Shield AI — Explainable Multi-Model Headline Forensic Engine
"""
from engine.types_data import (
    TokenSaliency,
    LexicalMetrics,
    ModelResult,
    ExplicableAnalysis,
    ConsensusVerdict,
    ModelBenchmarkMetrics,
    HeadlineRequest,
    BatchHeadlineRequest
)
from engine.models import evaluate_headline_consensus
from engine.benchmark_data import BENCHMARK_METRICS
from engine.sample_headlines import SAMPLE_HEADLINES

__all__ = [
    "TokenSaliency",
    "LexicalMetrics",
    "ModelResult",
    "ExplicableAnalysis",
    "ConsensusVerdict",
    "ModelBenchmarkMetrics",
    "HeadlineRequest",
    "BatchHeadlineRequest",
    "evaluate_headline_consensus",
    "BENCHMARK_METRICS",
    "SAMPLE_HEADLINES"
]
