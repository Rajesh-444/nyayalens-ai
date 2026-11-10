from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    text: str
    source: str


@dataclass(frozen=True)
class SearchResult:
    document: Document
    score: float

    @property
    def citation(self) -> str:
        return f"[{self.document.id}] {self.document.title} - {self.document.source}"


class TfidfRetriever:
    """Small, inspectable TF-IDF retriever using cosine similarity."""

    def __init__(self, documents: Iterable[Document]):
        self.documents = list(documents)
        if not self.documents:
            raise ValueError("at least one document is required")

        tokenized = [tokenize(f"{doc.title} {doc.text}") for doc in self.documents]
        document_frequency: Counter[str] = Counter()
        for tokens in tokenized:
            document_frequency.update(set(tokens))

        count = len(self.documents)
        self.idf = {
            token: math.log((1 + count) / (1 + frequency)) + 1
            for token, frequency in document_frequency.items()
        }
        self.vectors = [self._vector(tokens) for tokens in tokenized]

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "TfidfRetriever":
        documents: list[Document] = []
        with Path(path).open(encoding="utf-8") as corpus:
            for line in corpus:
                if line.strip():
                    documents.append(Document(**json.loads(line)))
        return cls(documents)

    def _vector(self, tokens: list[str]) -> dict[str, float]:
        counts = Counter(tokens)
        if not counts:
            return {}
        scale = sum(counts.values())
        return {
            token: (frequency / scale) * self.idf[token]
            for token, frequency in counts.items()
            if token in self.idf
        }

    @staticmethod
    def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
        if not left or not right:
            return 0.0
        numerator = sum(weight * right.get(token, 0.0) for token, weight in left.items())
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0

    def search(self, query: str, limit: int = 3) -> list[SearchResult]:
        if limit < 1:
            raise ValueError("limit must be positive")
        query_vector = self._vector(tokenize(query))
        ranked = [
            SearchResult(document=document, score=self._cosine(query_vector, vector))
            for document, vector in zip(self.documents, self.vectors, strict=True)
        ]
        return sorted(ranked, key=lambda result: (-result.score, result.document.id))[:limit]

