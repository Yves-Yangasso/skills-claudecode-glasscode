"""Application service — the Facade that orchestrates the audit pipeline.

It depends only on the abstractions (source / parser / scorer / renderer),
which are injected. That is Dependency Inversion in practice: this class never
names a concrete Semgrep, rich, or file-IO type.
"""

from __future__ import annotations

from .models import ScanResult, Score
from .parsing.base import ScanResultParser
from .rendering.base import ReportRenderer
from .scoring.base import ScoreStrategy
from .sources import ReportSource


class AuditReportService:
    def __init__(
        self,
        source: ReportSource,
        parser: ScanResultParser,
        scorer: ScoreStrategy,
        renderer: ReportRenderer,
    ) -> None:
        self._source = source
        self._parser = parser
        self._scorer = scorer
        self._renderer = renderer

    def run(self) -> tuple[ScanResult, Score]:
        raw = self._source.read()
        result = self._parser.parse(raw)
        score = self._scorer.compute(result)
        self._renderer.render(result, score)
        return result, score
