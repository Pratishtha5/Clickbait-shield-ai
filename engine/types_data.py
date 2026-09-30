"""
ClickBait Shield AI - Data Models and Types
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class TokenSaliency(BaseModel):
    token: str
    clean_token: str
    score: float  # -1.0 (strongly factual) to +1.0 (strongly clickbait)
    category: str  # 'high_clickbait' | 'moderate_clickbait' | 'neutral' | 'factual'
    attribution_percent: int
    matched_trigger: Optional[str] = None
    explanation: Optional[str] = None

class LexicalMetrics(BaseModel):
    word_count: int
    char_count: int
    exclamation_count: int
    question_count: int
    uppercase_ratio: float
    digit_count: int
    emotional_valence: float
    has_number_list_bait: bool
    has_curiosity_gap: bool
    has_demonstrative_pronouns: bool

class ModelResult(BaseModel):
    id: str
    name: str
    model_type: str
    score: float  # 0.0 to 1.0
    percentage: float  # 0.0 to 100.0%
    prediction: str  # 'Clickbait' | 'Legitimate'
    latency_ms: float
    confidence: str  # 'High' | 'Moderate' | 'Low'
    architecture_info: str
    weight_in_consensus: float
    key_factors: List[str]

class ExplicableAnalysis(BaseModel):
    primary_summary: str
    psychological_levers: List[str]
    syntactic_signals: List[str]
    factual_anchors: List[str]
    actionable_verdict: str

class ConsensusVerdict(BaseModel):
    id: str
    headline: str
    timestamp: str
    consensus_score: float  # 0.0 to 100.0
    threat_level: str  # 'CRITICAL CLICKBAIT' | 'HIGH CONFIDENCE CLICKBAIT' | 'MODERATE RISK' | 'LOW RISK' | 'SAFE'
    is_clickbait: bool
    ensemble_latency_ms: float
    model_results: List[ModelResult]
    tokens: List[TokenSaliency]
    lexical_metrics: LexicalMetrics
    top_triggers_found: List[str]
    explicable_analysis: ExplicableAnalysis

class ModelBenchmarkMetrics(BaseModel):
    id: str
    name: str
    category: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    latency_ms: float
    roc_auc: float
    mcc: float
    specificity: float
    confusion_matrix: Dict[str, int]
    strengths: str
    weaknesses: str
    hyperparameters: Dict[str, Any]

class HeadlineRequest(BaseModel):
    headline: str

class BatchHeadlineRequest(BaseModel):
    headlines: List[str]
