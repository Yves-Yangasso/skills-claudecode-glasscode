"""Report sources — where the raw scan data comes from.

Separating *acquiring* the raw data from *interpreting* it (the parser) keeps
each class single-responsibility and lets us swap a file for a string, a URL,
or stdin without touching parsing logic (Dependency Inversion).
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod

from .errors import InvalidReportError, ReportNotFoundError


class ReportSource(ABC):
    """Abstract provider of a raw scan report (already decoded to a dict)."""

    @abstractmethod
    def read(self) -> dict:
        """Return the raw report as a dict, or raise a GlassCodeError."""


class JsonFileReportSource(ReportSource):
    """Reads a Semgrep-style JSON report from a file on disk."""

    def __init__(self, path: str) -> None:
        self._path = path

    def read(self) -> dict:
        try:
            with open(self._path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError as exc:
            raise ReportNotFoundError(f"Rapport introuvable : {self._path}") from exc
        except json.JSONDecodeError as exc:
            raise InvalidReportError(f"JSON invalide ({self._path}) : {exc}") from exc


class InMemoryReportSource(ReportSource):
    """Wraps an already-loaded dict — handy for tests and pipelines."""

    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def read(self) -> dict:
        return self._payload
