"""GlassCode — visual code quality & security audit reports.

Public API: build a pipeline via the factory, or compose your own with the
abstractions exported here.
"""

from .factory import build_service, build_renderer
from .models import Finding, ScanResult, Score, Severity
from .service import AuditReportService

__version__ = "1.0.0"

__all__ = [
    "build_service",
    "build_renderer",
    "AuditReportService",
    "ScanResult",
    "Finding",
    "Score",
    "Severity",
    "__version__",
]
