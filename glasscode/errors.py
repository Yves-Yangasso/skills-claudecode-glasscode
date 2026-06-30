
"""Typed exceptions so callers can react to *why* something failed (ISP)."""

from __future__ import annotations


class GlassCodeError(Exception):
    """Base class for every error raised by GlassCode."""


class ReportNotFoundError(GlassCodeError):
    """The scan report file does not exist."""


class InvalidReportError(GlassCodeError):
    """The scan report exists but is not valid JSON / has an unexpected shape."""
