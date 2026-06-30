"""Human-facing renderer: a colored console report built with `rich`.

`rich` is imported lazily inside the constructor so that importing the package
(e.g. for the JSON renderer in CI) never requires `rich` to be installed.
"""

from __future__ import annotations

from ..models import ScanResult, Score, Severity
from .base import ReportRenderer


class RichConsoleRenderer(ReportRenderer):
    def __init__(self, top_n: int = 3) -> None:
        try:
            from rich.console import Console
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise ImportError(
                "Le module 'rich' est requis pour le rendu console. "
                "Installe-le avec : pip install rich"
            ) from exc
        self._console = Console()
        self._top_n = top_n

    def render(self, result: ScanResult, score: Score) -> None:
        if result.is_clean:
            self._render_clean()
            return
        self._render_table(result)
        self._console.print()
        self._render_summary(result, score)
        self._render_top(result)

    # -- sub-steps -------------------------------------------------------

    def _render_clean(self) -> None:
        from rich.panel import Panel

        self._console.print(
            Panel(
                "[bold green]✅ Aucun problème détecté.[/] "
                "Le code est transparent. 🪟",
                title="📊 GlassCode",
                border_style="green",
            )
        )

    def _render_table(self, result: ScanResult) -> None:
        from rich.table import Table
        from rich.text import Text

        table = Table(
            title="🔎 GlassCode — Problèmes détectés",
            header_style="bold white on grey23",
            expand=True,
            row_styles=["", "grey11"],
        )
        table.add_column("Sévérité", no_wrap=True)
        table.add_column("Fichier", style="bold", overflow="fold")
        table.add_column("Ligne", justify="right", no_wrap=True)
        table.add_column("Règle", style="dim", overflow="fold")
        table.add_column("Message", overflow="fold")

        for finding in result.sorted_by_urgency():
            sev = finding.severity
            table.add_row(
                Text(sev.badge, style=sev.color),
                finding.path,
                str(finding.line),
                finding.short_rule,
                finding.message or "—",
            )
        self._console.print(table)

    def _render_summary(self, result: ScanResult, score: Score) -> None:
        from rich.panel import Panel

        counts = result.counts_by_severity()
        filled = round(score.value / 5)
        bar = f"[{score.color}]" + "█" * filled + "[/]" + "░" * (20 - filled)

        summary = (
            f"Score qualité : {bar} "
            f"[bold {score.color}]{score.value}%[/]  ({score.verdict})\n\n"
            f"🔴 Critique : [bold red]{counts[Severity.CRITICAL]}[/]    "
            f"🟠 Élevé : [yellow]{counts[Severity.HIGH]}[/]    "
            f"🟡 Moyen : [cyan]{counts[Severity.MEDIUM]}[/]\n"
            f"Fichiers scannés : {score.total_files}   "
            f"Fichiers sains : {score.clean_files}"
        )
        self._console.print(
            Panel(summary, title="📊 Synthèse", border_style=score.color)
        )

    def _render_top(self, result: ScanResult) -> None:
        from rich.syntax import Syntax
        from rich.text import Text

        top = result.sorted_by_urgency()[: self._top_n]
        if not top:
            return
        self._console.print("\n[bold]🎯 Corrections prioritaires[/]\n")
        for i, finding in enumerate(top, 1):
            sev = finding.severity
            header = Text(f"{i}. {sev.badge}  ", style=sev.color)
            header.append(finding.location, style="bold white")
            self._console.print(header)
            self._console.print(f"   [italic]{finding.message}[/]")
            if finding.code:
                self._console.print(
                    Syntax(finding.code, "python", theme="ansi_dark",
                           line_numbers=False, word_wrap=True)
                )
            if finding.suggested_fix:
                self._console.print(
                    f"   [green]→ Fix suggéré :[/] {finding.suggested_fix}"
                )
            self._console.print()
