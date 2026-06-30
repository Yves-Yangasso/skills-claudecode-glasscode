from glasscode.models import Severity
from glasscode.parsing import SemgrepParser


def test_parses_all_findings(semgrep_payload):
    result = SemgrepParser().parse(semgrep_payload)
    assert len(result.findings) == 3
    assert result.scanned_files == (
        "app/utils.py", "app/main.py", "app/models.py", "app/db.py",
    )


def test_maps_semgrep_severity(semgrep_payload):
    result = SemgrepParser().parse(semgrep_payload)
    by_rule = {f.short_rule: f for f in result.findings}
    assert by_rule["dangerous-subprocess-use"].severity is Severity.CRITICAL
    assert by_rule["debug-enabled"].severity is Severity.HIGH
    assert by_rule["unused-import"].severity is Severity.MEDIUM


def test_unknown_severity_falls_back():
    payload = {"results": [{"check_id": "x", "path": "a.py",
                            "start": {"line": 1},
                            "extra": {"severity": "WEIRD", "message": "?"}}]}
    result = SemgrepParser().parse(payload)
    assert result.findings[0].severity is Severity.UNKNOWN


def test_empty_report_is_clean():
    result = SemgrepParser().parse({"results": [], "paths": {"scanned": []}})
    assert result.is_clean
    assert result.findings == ()


def test_missing_keys_do_not_crash():
    result = SemgrepParser().parse({})
    assert result.is_clean
    assert result.total_files == 0
