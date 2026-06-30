import pytest


@pytest.fixture
def semgrep_payload():
    return {
        "results": [
            {
                "check_id": "python.security.dangerous-subprocess-use",
                "path": "app/utils.py",
                "start": {"line": 12},
                "extra": {
                    "severity": "ERROR",
                    "message": "shell=True : risque d'injection.",
                    "lines": "subprocess.call(cmd, shell=True)",
                    "fix": "Utilise une liste d'arguments.",
                },
            },
            {
                "check_id": "python.flask.debug-enabled",
                "path": "app/main.py",
                "start": {"line": 40},
                "extra": {"severity": "WARNING", "message": "debug=True."},
            },
            {
                "check_id": "python.lang.unused-import",
                "path": "app/main.py",
                "start": {"line": 1},
                "extra": {"severity": "INFO", "message": "Import inutilisé."},
            },
        ],
        "paths": {"scanned": ["app/utils.py", "app/main.py", "app/models.py", "app/db.py"]},
    }
