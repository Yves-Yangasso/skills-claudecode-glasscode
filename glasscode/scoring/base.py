"""Scoring abstraction (Strategy pattern).

The way a codebase's health is summarized into a number is a policy decision.
Different teams may weigh severities differently — so the algorithm lives behind
an interface and can be swapped without touching parsing or rendering.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import ScanResult, Score


class ScoreStrategy(ABC):
    @abstractmethod
    def compute(self, result: ScanResult) -> Score:
        """Produce a quality `Score` from a `ScanResult`."""
