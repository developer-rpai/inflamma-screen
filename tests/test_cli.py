"""CLI smoke tests: the interactive screener runs end to end."""

import subprocess
import sys


def run_cli(*args, stdin_text):
    return subprocess.run(
        [sys.executable, "-m", "inflamma_screen.cli", *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_cli_full_run_elevated():
    # 12 answers of "often", then decline saving the report.
    proc = run_cli("-c", "hidradenitis_suppurativa", stdin_text="2\n" * 12 + "n\n")
    assert proc.returncode == 0, proc.stderr
    assert "ELEVATED" in proc.stdout
    assert "not a diagnosis" in proc.stdout.lower()


def test_cli_json_output():
    proc = run_cli("-c", "psoriasis", "-j", stdin_text="0\n" * 12)
    assert proc.returncode == 0, proc.stderr
    assert '"band": "low"' in proc.stdout
    assert '"disclaimer"' in proc.stdout


def test_cli_invalid_condition_exits_nonzero():
    proc = run_cli("-c", "not_real", stdin_text="")
    assert proc.returncode == 2
    assert "unknown condition" in proc.stdout.lower()


def test_cli_saves_report_to_file(tmp_path):
    out = tmp_path / "report.txt"
    proc = run_cli("-c", "atopic_dermatitis", "-o", str(out),
                   stdin_text="1\n" * 12)
    assert proc.returncode == 0, proc.stderr
    text = out.read_text(encoding="utf-8")
    assert "not a diagnosis" in text.lower()
