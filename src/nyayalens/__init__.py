"""Explainable retrieval primitives for NyayaLens AI."""

from .retriever import Document, SearchResult, TfidfRetriever
from .triage import TriageResult, UrgencyTriage

__all__ = ["Document", "SearchResult", "TfidfRetriever", "TriageResult", "UrgencyTriage"]

