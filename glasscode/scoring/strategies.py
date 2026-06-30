"""Concrete scoring strategies."""

from __future__ import annotations

from ..models import ScanResult, Score
from .base import ScoreStrategy


class CriticalFreeRatioStrategy(ScoreStrategy):
    """Score = share of scanned files that carry no critical finding.

    Thresholds map the percentage to a verdict and a display color.
    """

    _THRESHOLDS = (
        (90, "Excellent", "green"),
        (70, "Correct", "yellow"),
        (0, "À risque", "red"),
    )

    def compute(self, result: ScanResult) -> Score:
        total = result.total_files
        clean = max(total - len(result.files_with_critical), 0)
        value = int((clean / total) * 100) if total else 100

        verdict, color = self._classify(value)
        return Score(
            value=value,
            verdict=verdict,
            color=color,
            clean_files=clean,
            total_files=total,
        )

    def _classify(self, value: int) -> tuple[str, str]:
        for threshold, verdict, color in self._THRESHOLDS:
            if value >= threshold:
                return verdict, color
        return "À risque", "red"
