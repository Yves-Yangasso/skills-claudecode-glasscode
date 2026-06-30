"""Renderer abstraction (Strategy pattern).

Output format is a swappable policy: a colored console report for humans, JSON
for CI gates, Markdown for a PR comment... Each is a `ReportRenderer`, added
without modifying the service that drives them (Open/Closed, Liskov).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import ScanResult, Score


class ReportRenderer(ABC):
    @abstractmethod
    def render(self, result: ScanResult, score: Score) -> None:
        """Emit the report to this renderer's destination."""
