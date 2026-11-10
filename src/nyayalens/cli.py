from __future__ import annotations

import argparse
from pathlib import Path

from .guardrails import SafetyGate
from .retriever import TfidfRetriever
from .triage import UrgencyTriage


def main() -> None:
    parser = argparse.ArgumentParser(description="Search a synthetic legal-reference corpus")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    corpus = Path(__file__).resolve().parents[2] / "data" / "sample_corpus.jsonl"
    retriever = TfidfRetriever.from_jsonl(corpus)
    safety = SafetyGate().evaluate(args.query)
    if not safety.allowed:
        print(f"Request blocked: {', '.join(safety.reasons)}")
        print("Educational output only - not legal advice.")
        raise SystemExit(2)
    if safety.reasons:
        print(f"Safety: {', '.join(safety.reasons)}")
    triage = UrgencyTriage().classify(safety.sanitized_text)

    print(f"Triage: {triage.label}")
    if triage.matched_signals:
        print(f"Signals: {', '.join(triage.matched_signals)}")
    print("\nEvidence:")
    for result in retriever.search(safety.sanitized_text, args.limit):
        print(f"- {result.citation} (score={result.score:.3f})")
        print(f"  {result.document.text}")
    print("\nEducational output only - not legal advice.")


if __name__ == "__main__":
    main()

