import io
import json

from glasscode.parsing import SemgrepParser
from glasscode.rendering.json_report import JsonReportRenderer
from glasscode.scoring import CriticalFreeRatioStrategy
from glasscode.service import AuditReportService
from glasscode.sources import InMemoryReportSource


def test_service_runs_full_pipeline(semgrep_payload):
    stream = io.StringIO()
    service = AuditReportService(
        source=InMemoryReportSource(semgrep_payload),
        parser=SemgrepParser(),
        scorer=CriticalFreeRatioStrategy(),
        renderer=JsonReportRenderer(stream=stream),
    )
    result, score = service.run()

    assert score.value == 75
    payload = json.loads(stream.getvalue())
    assert payload["score"]["value"] == 75
    assert payload["counts"]["CRITIQUE"] == 1
    assert len(payload["findings"]) == 3
    # findings come out sorted, critical first
    assert payload["findings"][0]["severity"] == "CRITIQUE"
