"""Parsers turn a raw scanner report into the domain `ScanResult`."""

from .base import ScanResultParser
from .semgrep import SemgrepParser

__all__ = ["ScanResultParser", "SemgrepParser"]
