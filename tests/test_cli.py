import json

from glasscode.cli import main


def _write(tmp_path, payload):
    p = tmp_path / "report.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


def test_cli_json_format_succeeds(tmp_path, semgrep_payload, capsys):
    path = _write(tmp_path, semgrep_payload)
    code = main([path, "--format", "json"])
    assert code == 0
    assert json.loads(capsys.readouterr().out)["score"]["value"] == 75


def test_cli_fail_under_gate(tmp_path, semgrep_payload):
    path = _write(tmp_path, semgrep_payload)
    # score is 75; requiring 90 must fail the gate
    assert main([path, "--format", "json", "--fail-under", "90"]) == 1
    assert main([path, "--format", "json", "--fail-under", "70"]) == 0


def test_cli_missing_file_returns_error():
    assert main(["/does/not/exist.json", "--format", "json"]) == 1
