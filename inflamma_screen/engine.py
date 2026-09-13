"""Core screening engine: weighted symptom scoring with transparent bands.

Every result object carries the educational disclaimer. Nothing here is a
diagnostic instrument; see docs/METHODOLOGY.md for the scoring rationale
and its limits.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from importlib import resources

DISCLAIMER = (
    "Educational screening only. This is not a diagnosis. This tool is not "
    "a medical device and cannot confirm or rule out any condition. Results "
    "reflect how closely your answers match commonly described symptom "
    "patterns. Please discuss your symptoms with a qualified clinician."
)

ANSWER_LABELS = {0: "Never", 1: "Sometimes", 2: "Often"}

BAND_GUIDANCE = {
    "low": (
        "Your answers show limited overlap with commonly described patterns "
        "for this condition. If symptoms persist or worry you, a clinician can "
        "still help you understand them."
    ),
    "moderate": (
        "Your answers show some overlap with commonly described patterns for "
        "this condition. Consider writing down your symptoms and discussing "
        "them with a clinician."
    ),
    "elevated": (
        "Your answers show notable overlap with commonly described patterns "
        "for this condition. Consider booking a clinician appointment and "
        "bringing the generated summary with you."
    ),
}

_LOW_CUTOFF = 30.0
_MODERATE_CUTOFF = 60.0


def _band_for(percent: float) -> str:
    if percent < _LOW_CUTOFF:
        return "low"
    if percent <= _MODERATE_CUTOFF:
        return "moderate"
    return "elevated"


def load_conditions() -> dict:
    """Load the bundled condition and question data."""
    path = resources.files("inflamma_screen") / "data" / "conditions.json"
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)["conditions"]


def get_condition(condition_id: str) -> dict:
    for condition in load_conditions():
        if condition["id"] == condition_id:
            return condition
    raise ValueError(f"unknown condition: {condition_id!r}")


def list_conditions() -> list[tuple[str, str]]:
    """Return (condition_id, display name) pairs in data order."""
    return [(c["id"], c["name"]) for c in load_conditions()]


@dataclass
class ScreeningResult:
    condition_id: str
    condition_name: str
    score: float
    band: str
    band_guidance: str
    key_symptoms_endorsed: list[str] = field(default_factory=list)
    questions_answered: int = 0
    questions_total: int = 0
    disclaimer: str = DISCLAIMER

    def to_dict(self) -> dict:
        return {
            "condition_id": self.condition_id,
            "condition_name": self.condition_name,
            "score": self.score,
            "band": self.band,
            "band_guidance": self.band_guidance,
            "key_symptoms_endorsed": self.key_symptoms_endorsed,
            "questions_answered": self.questions_answered,
            "questions_total": self.questions_total,
            "disclaimer": self.disclaimer,
        }


def score_condition(condition_id: str, answers: dict[str, int]) -> ScreeningResult:
    """Score one condition's answers and return a banded result.

    answers maps question id to 0 (never), 1 (sometimes), or 2 (often).
    Questions without an answer count as 0, so partial answer sets dilute
    toward lower bands instead of inflating them.
    """
    condition = get_condition(condition_id)
    questions = {q["id"]: q for q in condition["questions"]}

    for qid, value in answers.items():
        if qid not in questions:
            raise ValueError(f"unknown question id: {qid!r}")
        if value not in (0, 1, 2):
            raise ValueError(
                f"answer for {qid!r} must be 0, 1, or 2; got {value!r}"
            )

    weighted = 0
    max_weighted = 0
    endorsed: list[str] = []

    for question in condition["questions"]:
        value = answers.get(question["id"], 0)
        weighted += question["weight"] * value
        max_weighted += question["weight"] * 2
        if question.get("key") and value == 2:
            endorsed.append(question["text"])

    percent = round(100.0 * weighted / max_weighted, 1) if max_weighted else 0.0
    band = _band_for(percent)

    return ScreeningResult(
        condition_id=condition["id"],
        condition_name=condition["name"],
        score=percent,
        band=band,
        band_guidance=BAND_GUIDANCE[band],
        key_symptoms_endorsed=endorsed,
        questions_answered=len(answers),
        questions_total=len(questions),
    )


def screen_all(answers_by_condition: dict[str, dict[str, int]]) -> list[ScreeningResult]:
    """Score every condition present in answers_by_condition."""
    return [
        score_condition(condition_id, answers)
        for condition_id, answers in answers_by_condition.items()
    ]
