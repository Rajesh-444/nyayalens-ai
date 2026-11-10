from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    sanitized_text: str
    reasons: tuple[str, ...]


class SafetyGate:
    """Deterministic input controls applied before retrieval or triage."""

    MAX_QUERY_CHARS = 1_000
    INJECTION_PATTERNS = (
        re.compile(r"ignore (all |any )?(previous|prior) instructions", re.IGNORECASE),
        re.compile(r"reveal (the )?(system|developer) prompt", re.IGNORECASE),
        re.compile(r"bypass (the )?(safety|guardrails|policy)", re.IGNORECASE),
        re.compile(r"act as if you have no restrictions", re.IGNORECASE),
    )
    REDACTIONS = (
        (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE), "[EMAIL]"),
        (re.compile(r"(?<!\d)(?:\+91[ -]?)?[6-9]\d{9}(?!\d)"), "[PHONE]"),
        (re.compile(r"(?<!\d)\d{4}[ -]?\d{4}[ -]?\d{4}(?!\d)"), "[ID_NUMBER]"),
    )

    def evaluate(self, text: str) -> SafetyDecision:
        normalized = " ".join(text.split())
        if not normalized:
            return SafetyDecision(False, "", ("query is empty",))
        if len(normalized) > self.MAX_QUERY_CHARS:
            return SafetyDecision(False, "", (f"query exceeds {self.MAX_QUERY_CHARS} characters",))

        injection_matches = tuple(
            pattern.pattern for pattern in self.INJECTION_PATTERNS if pattern.search(normalized)
        )
        if injection_matches:
            return SafetyDecision(False, "", ("prompt-injection pattern detected",))

        sanitized = normalized
        redacted: list[str] = []
        for pattern, replacement in self.REDACTIONS:
            sanitized, count = pattern.subn(replacement, sanitized)
            if count:
                redacted.append(replacement.strip("[]").lower())
        reasons = (f"redacted: {', '.join(redacted)}",) if redacted else ()
        return SafetyDecision(True, sanitized, reasons)

