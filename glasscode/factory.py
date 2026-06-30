"""Factory — wires concrete implementations into a ready-to-run service.

Centralizing construction here keeps the CLI thin and makes the default object
graph swappable in one place. The renderer registry is the Open/Closed seam:
register a new format without editing existing branches.
"""

from __future__ import annotations

from typing import Callable

from .rendering.base import ReportRenderer
from .rendering.json_report import JsonReportRenderer
from .rendering.rich_console import RichConsoleRenderer
from .scoring.strategies import CriticalFreeRatioStrategy
from .parsing.semgrep import SemgrepParser
from .service import AuditReportService
from .sources import JsonFileReportSource

# format name -> renderer constructor (Open/Closed: extend the map, don't edit code)
_RENDERERS: dict[str, Callable[[], ReportRenderer]] = {
    "rich": RichConsoleRenderer,
    "json": JsonReportRenderer,
}

AVAILABLE_FORMATS = tuple(_RENDERERS)


def build_renderer(fmt: str) -> ReportRenderer:
    try:
        return _RENDERERS[fmt]()
    except KeyError as exc:
        raise ValueError(
            f"Format inconnu '{fmt}'. Disponibles : {', '.join(AVAILABLE_FORMATS)}"
        ) from exc


def build_service(
    json_path: str,
    root: str | None = None,
    fmt: str = "rich",
) -> AuditReportService:
    """Assemble the default audit pipeline for a Semgrep JSON report."""
    return AuditReportService(
        source=JsonFileReportSource(json_path),
        parser=SemgrepParser(root=root),
        scorer=CriticalFreeRatioStrategy(),
        renderer=build_renderer(fmt),
    )
