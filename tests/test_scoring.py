from glasscode.parsing import SemgrepParser
from glasscode.scoring import CriticalFreeRatioStrategy


def test_score_is_ratio_of_critical_free_files(semgrep_payload):
    result = SemgrepParser().parse(semgrep_payload)
    score = CriticalFreeRatioStrategy().compute(result)
    # 4 scanned files, 1 has a critical finding -> 3/4 = 75%
    assert score.value == 75
    assert score.verdict == "Correct"
    assert score.clean_files == 3
    assert score.total_files == 4


def test_clean_scan_scores_100():
    result = SemgrepParser().parse({"results": [], "paths": {"scanned": ["a.py"]}})
    score = CriticalFreeRatioStrategy().compute(result)
    assert score.value == 100
    assert score.verdict == "Excellent"


def test_all_critical_scores_low():
    payload = {
        "results": [
            {"check_id": "r", "path": "a.py", "start": {"line": 1},
             "extra": {"severity": "ERROR", "message": "boom"}}
        ],
        "paths": {"scanned": ["a.py"]},
    }
    result = SemgrepParser().parse(payload)
    score = CriticalFreeRatioStrategy().compute(result)
    assert score.value == 0
    assert score.verdict == "À risque"
