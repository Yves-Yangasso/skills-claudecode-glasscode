"""Domain models for GlassCode.

These are pure, framework-agnostic data structures. They know nothing about
Semgrep, JSON, or `rich` — that decoupling is what lets parsers, scorers and
renderers vary independently (Single Responsibility + Dependency Inversion).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Normalized severity, independent of the underlying scanner vocabulary."""

    CRITICAL = ("CRITIQUE", "bold red", "🔴", 0)
    HIGH = ("ÉLEVÉ", "yellow", "🟠", 1)
    MEDIUM = ("MOYEN", "cyan", "🟡", 2)
    UNKNOWN = ("INCONNU", "white", "⚪", 3)

    def __init__(self, label: str, color: str, emoji: str, rank: int) -> None:
        self.label = label
        self.color = color
        self.emoji = emoji
        self.rank = rank  # lower = more urgent, used for sorting

    @property
    def badge(self) -> str:
        return f"{self.emoji} {self.label}"


@dataclass(frozen=True)
class Finding:
    """A single problem reported by a scanner."""

    rule_id: str
    path: str
    line: int
    message: str
    severity: Severity
    code: str = ""
    suggested_fix: str = ""

    @property
    def short_rule(self) -> str:
        return self.rule_id.split(".")[-1] if self.rule_id else "—"

    @property
    def location(self) -> str:
        return f"{self.path}:{self.line}"


@dataclass(frozen=True)
class ScanResult:
    """The full outcome of a scan: every finding plus the files that were scanned."""

    findings: tuple[Finding, ...]
    scanned_files: tuple[str, ...]

    @property
    def is_clean(self) -> bool:
        return not self.findings

    @property
    def total_files(self) -> int:
        if self.scanned_files:
            return len(self.scanned_files)
        return len({f.path for f in self.findings})

    @property
    def files_with_critical(self) -> set[str]:
        return {f.path for f in self.findings if f.severity is Severity.CRITICAL}

    def counts_by_severity(self) -> dict[Severity, int]:
        counts = {sev: 0 for sev in Severity}
        for finding in self.findings:
            counts[finding.severity] += 1
        return counts

    def sorted_by_urgency(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: f.severity.rank)


@dataclass(frozen=True)
class Score:
    """A computed quality score for a scan result."""

    value: int          # 0-100
    verdict: str        # human-readable judgement
    color: str          # rich color for display
    clean_files: int
    total_files: int
