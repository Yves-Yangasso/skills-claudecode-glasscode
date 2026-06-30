"""Scoring strategies turn a `ScanResult` into a `Score`."""

from .base import ScoreStrategy
from .strategies import CriticalFreeRatioStrategy

__all__ = ["ScoreStrategy", "CriticalFreeRatioStrategy"]
