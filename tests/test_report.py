"""Report tests: disclaimers, bands, and endorsed symptoms."""

from inflamma_screen import score_condition
from inflamma_screen.report import build_report, save_report


def elevated_hs_result():
    answers = {
        "hs_01": 2, "hs_02": 2, "hs_03": 2, "hs_04": 2,
        "hs_05": 1, "hs_06": 1, "hs_07": 1, "hs_08": 2,
        "hs_09": 0, "hs_10": 0, "hs_11": 1, "hs_12": 0,
    }
    return score_condition("hidradenitis_suppurativa", answers)


def test_report_contains_full_disclaimer():
    text = build_report([elevated_hs_result()])
    assert "not a diagnosis" in text.lower()
    assert "not a medical device" in text.lower()


def test_report_contains_band_and_score():
    result = elevated_hs_result()
    text = build_report([result])
    assert result.band.upper() in text
    assert str(result.score) in text
    assert result.condition_name in text


def test_report_lists_endorsed_key_symptoms():
    text = build_report([elevated_hs_result()])
    assert "Key symptoms you endorsed" in text


def test_report_suggests_clinician_questions():
    text = build_report([elevated_hs_result()])
    assert "dermatologist" in text.lower()


def test_save_report_roundtrip(tmp_path):
    text = build_report([elevated_hs_result()])
    path = str(tmp_path / "summary.txt")
    assert save_report(text, path) == path
    with open(path, encoding="utf-8") as f:
        assert f.read() == text
