"""Engine tests: scoring bands, boundaries, validation, disclaimers."""

import pytest

from inflamma_screen import (
    DISCLAIMER,
    get_condition,
    list_conditions,
    screen_all,
    score_condition,
)
from inflamma_screen.engine import _band_for


CONDITION_IDS = [cid for cid, _ in list_conditions()]


def full_answers(condition_id, value):
    condition = get_condition(condition_id)
    return {q["id"]: value for q in condition["questions"]}


def test_all_zero_answers_gives_low_band():
    for cid in CONDITION_IDS:
        result = score_condition(cid, full_answers(cid, 0))
        assert result.score == 0.0
        assert result.band == "low"


def test_all_max_answers_gives_elevated_band():
    for cid in CONDITION_IDS:
        result = score_condition(cid, full_answers(cid, 2))
        assert result.score == 100.0
        assert result.band == "elevated"


def test_band_boundaries():
    assert _band_for(0.0) == "low"
    assert _band_for(29.9) == "low"
    assert _band_for(30.0) == "moderate"
    assert _band_for(45.0) == "moderate"
    assert _band_for(60.0) == "moderate"
    assert _band_for(60.1) == "elevated"
    assert _band_for(100.0) == "elevated"


def test_boundary_scores_through_engine():
    # One endorsed key symptom on its own must not reach "elevated":
    # unanswered questions count as 0, diluting the score.
    result = score_condition("hidradenitis_suppurativa", {"hs_01": 2})
    assert result.band == "low"
    assert 0 < result.score < 30


def test_partial_answers_dilute_toward_low():
    result = score_condition("psoriasis", {"ps_01": 2})
    assert result.band == "low"
    assert result.questions_answered == 1
    assert result.questions_total == 12


def test_empty_answers_allowed():
    result = score_condition("psoriasis", {})
    assert result.score == 0.0
    assert result.band == "low"
    assert result.questions_answered == 0
    assert result.questions_total == 12


def test_partial_answers_dilute_toward_low():
    # Unanswered questions count as 0, so a single endorsed symptom cannot
    # drive an alarming band on its own.
    result = score_condition("psoriasis", {"ps_01": 2})
    assert result.band == "low"
    assert result.questions_answered == 1
    assert result.questions_total == 12


def test_unknown_condition_raises():
    with pytest.raises(ValueError):
        score_condition("not_a_condition", {})


def test_unknown_question_id_raises():
    with pytest.raises(ValueError):
        score_condition("psoriasis", {"ps_99": 2})


@pytest.mark.parametrize("bad", [-1, 3, 99, "2", 1.5, None])
def test_invalid_answer_values_raise(bad):
    with pytest.raises(ValueError):
        score_condition("psoriasis", {"ps_01": bad})


def test_disclaimer_present_in_every_result():
    answers = {
        "hidradenitis_suppurativa": full_answers("hidradenitis_suppurativa", 2),
        "psoriasis": full_answers("psoriasis", 1),
        "atopic_dermatitis": {},
    }
    for result in screen_all(answers):
        assert result.disclaimer == DISCLAIMER
        assert "not a diagnosis" in result.disclaimer.lower()
        as_dict = result.to_dict()
        assert as_dict["disclaimer"] == DISCLAIMER


def test_key_symptoms_endorsed_only_when_often():
    result = score_condition("atopic_dermatitis", {"ad_01": 2, "ad_02": 1})
    assert len(result.key_symptoms_endorsed) == 1
    assert "itchy" in result.key_symptoms_endorsed[0].lower()


def test_non_key_symptoms_never_listed_as_endorsed():
    result = score_condition("psoriasis", {"ps_03": 2})  # not a key question
    assert result.key_symptoms_endorsed == []


def test_screen_all_returns_one_result_per_condition():
    results = screen_all({cid: {} for cid in CONDITION_IDS})
    assert {r.condition_id for r in results} == set(CONDITION_IDS)


def test_result_dict_round_trip():
    result = score_condition("hidradenitis_suppurativa", full_answers("hidradenitis_suppurativa", 1))
    d = result.to_dict()
    assert d["band"] == "moderate"
    assert d["questions_answered"] == 12
    assert d["band_guidance"]
