"""
ClickBait Shield AI — CLI Prediction Tool
Predict whether a headline is Clickbait or Legitimate directly from the terminal.
Usage:
    python predict.py "Your headline text here"
"""
import sys
from engine.models import evaluate_headline_consensus

def main():
    if len(sys.argv) > 1:
        headline = " ".join(sys.argv[1:])
    else:
        headline = input("Enter headline to inspect: ").strip()

    if not headline:
        print("Please enter a non-empty headline.")
        return

    verdict = evaluate_headline_consensus(headline)

    print("\n" + "=" * 65)
    print(f"  HEADLINE: \"{verdict.headline}\"")
    print("=" * 65)
    print(f"  CONSENSUS SCORE : {verdict.consensus_score:.1f}%")
    print(f"  VERDICT         : {verdict.threat_level}")
    print(f"  IS CLICKBAIT    : {'YES' if verdict.is_clickbait else 'NO'}")
    print(f"  LATENCY         : {verdict.ensemble_latency_ms} ms")
    print("-" * 65)
    print("  MODEL BREAKDOWN:")
    for m in verdict.model_results:
        print(f"    - {m.name:<30}: {m.prediction:<10} ({m.percentage:.1f}%) [{m.confidence} confidence]")
    print("-" * 65)
    print("  TOKEN ATTRIBUTION (SALIENCY):")
    for t in verdict.tokens:
        if t.category != "neutral":
            sign = "+" if t.score > 0 else ""
            print(f"    - {t.token:<15} [{t.category:<18}]: {sign}{t.score:.2f} ({t.explanation})")
    print("-" * 65)
    print(f"  SUMMARY: {verdict.explicable_analysis.primary_summary}")
    print(f"  GUIDANCE: {verdict.explicable_analysis.actionable_verdict}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
