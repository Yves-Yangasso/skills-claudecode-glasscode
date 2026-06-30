"""Adapter from Semgrep's JSON output to the GlassCode domain model."""

from __future__ import annotations

import os

from ..models import Finding, ScanResult, Severity
from .base import ScanResultParser

# Semgrep's severity vocabulary -> our normalized severity.
_SEMGREP_SEVERITY = {
    "ERROR": Severity.CRITICAL,
    "WARNING": Severity.HIGH,
    "INFO": Severity.MEDIUM,
}


class SemgrepParser(ScanResultParser):
    """Parses the structure produced by `semgrep --json`.

    `root` is the scanned directory; when provided, file paths are made relative
    to it for readable display.
    """

    def __init__(self, root: str | None = None) -> None:
        self._root = root

    def parse(self, raw: dict) -> ScanResult:
        results = raw.get("results") or []
        findings = tuple(self._to_finding(item) for item in results)

        scanned = (raw.get("paths") or {}).get("scanned") or []
        scanned = tuple(self._relativize(path) for path in scanned)

        return ScanResult(findings=findings, scanned_files=scanned)

    def _to_finding(self, item: dict) -> Finding:
        extra = item.get("extra") or {}
        severity = _SEMGREP_SEVERITY.get(
            str(extra.get("severity", "")).upper(), Severity.UNKNOWN
        )
        message = str(extra.get("message", "")).strip().split("\n")[0]
        return Finding(
            rule_id=item.get("check_id", "") or "",
            path=self._relativize(item.get("path", "")),
            line=(item.get("start") or {}).get("line", 0) or 0,
            message=message,
            severity=severity,
            code=str(extra.get("lines", "") or "").strip(),
            suggested_fix=str(extra.get("fix", "") or "").strip(),
        )

    def _relativize(self, path: str) -> str:
        if not path:
            return "?"
        if self._root and os.path.isdir(self._root):
            try:
                return os.path.relpath(path, self._root)
            except ValueError:
                return path
        return path
