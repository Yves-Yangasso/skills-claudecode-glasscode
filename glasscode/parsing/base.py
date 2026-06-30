"""Parser abstraction (Strategy / Adapter seam).

A parser is an Adapter: it converts a scanner's wire format into our domain
model. Coding against this ABC (not against Semgrep directly) means support for
another scanner is a new class, not an edit to existing code (Open/Closed).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import ScanResult


class ScanResultParser(ABC):
    @abstractmethod
    def parse(self, raw: dict) -> ScanResult:
        """Convert a raw scanner report into a domain `ScanResult`."""
