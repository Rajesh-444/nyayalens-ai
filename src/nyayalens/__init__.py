"""Explainable retrieval primitives for NyayaLens AI."""

from .retriever import Document, SearchResult, TfidfRetriever
from .guardrails import SafetyDecision, SafetyGate
from .triage import TriageResult, UrgencyTriage

__all__ = [
    "Document",
    "SafetyDecision",
    "SafetyGate",
    "SearchResult",
    "TfidfRetriever",
    "TriageResult",
    "UrgencyTriage",
]

