"""Machine-readable renderer — for CI gates and tooling.

Demonstrates the Open/Closed payoff: a brand-new output format is a new class,
with zero changes to parsing, scoring, or the service.
"""

from __future__ import annotations

import json
import sys

from ..models import ScanResult, Score
from .base import ReportRenderer


class JsonReportRenderer(ReportRenderer):
    def __init__(self, stream=None) -> None:
        self._stream = stream if stream is not None else sys.stdout

    def render(self, result: ScanResult, score: Score) -> None:
        payload = {
            "score": {
                "value": score.value,
                "verdict": score.verdict,
                "clean_files": score.clean_files,
                "total_files": score.total_files,
            },
            "counts": {
                sev.label: count
                for sev, count in result.counts_by_severity().items()
            },
            "findings": [
                {
                    "severity": f.severity.label,
                    "rule": f.short_rule,
                    "path": f.path,
                    "line": f.line,
                    "message": f.message,
                    "fix": f.suggested_fix,
                }
                for f in result.sorted_by_urgency()
            ],
        }
        json.dump(payload, self._stream, ensure_ascii=False, indent=2)
        self._stream.write("\n")
