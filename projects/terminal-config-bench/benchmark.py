"""Evaluate a reference repair and a no-op on synthetic deployment tasks."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

CASES = (
    ("invalid-health-path", {"port": 8080, "health": "ready", "retries": 2}),
    ("invalid-port", {"port": 0, "health": "/ready", "retries": 2}),
    ("invalid-retries", {"port": 8080, "health": "/ready", "retries": -1}),
)
VALID = {"port": 8080, "health": "/ready", "retries": 2}


def repair(path):
    """Reference implementation for the supplied synthetic contract."""
    config = json.loads(path.read_text())
    if not 1 <= config["port"] <= 65535:
        config["port"] = 8080
    if not config["health"].startswith("/"):
        config["health"] = "/" + config["health"]
    if config["retries"] < 0:
        config["retries"] = 2
    path.write_text(json.dumps(config))


def evaluate():
    results = {}
    for strategy in ("noop", "repair"):
        outcomes = {}
        for case, broken in CASES:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                config = root / "deployment.json"
                config.write_text(json.dumps({**broken, "service": "demo"}))
                sentinel = root / "keep.txt"
                sentinel.write_text("unchanged")
                result = subprocess.run(
                    [sys.executable, str(Path(__file__).resolve()), strategy],
                    cwd=root, capture_output=True, text=True, timeout=5, check=False,
                )
                outcomes[case] = (
                    result.returncode == 0
                    and json.loads(config.read_text()) == {**VALID, "service": "demo"}
                    and sentinel.read_text() == "unchanged"
                )
        results[strategy] = outcomes
    return results


if __name__ == "__main__":
    if sys.argv[1:] == ["repair"]:
        repair(Path("deployment.json"))
    elif sys.argv[1:] == ["noop"]:
        pass
    elif not sys.argv[1:]:
        print(json.dumps(evaluate(), indent=2))
    else:
        raise SystemExit("Usage: python benchmark.py")
