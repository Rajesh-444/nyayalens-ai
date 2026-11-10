from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TriageResult:
    label: str
    matched_signals: tuple[str, ...]


class UrgencyTriage:
    """Transparent keyword signals; never presented as a legal conclusion."""

    SIGNALS = {
        "urgent": ("immediate danger", "threat", "violence", "arrested", "missing child"),
        "time_sensitive": ("deadline", "summons", "hearing", "eviction", "account hacked"),
    }

    def classify(self, text: str) -> TriageResult:
        normalized = re.sub(r"\s+", " ", text.lower()).strip()
        for label in ("urgent", "time_sensitive"):
            matches = tuple(signal for signal in self.SIGNALS[label] if signal in normalized)
            if matches:
                return TriageResult(label=label, matched_signals=matches)
        return TriageResult(label="standard", matched_signals=())

