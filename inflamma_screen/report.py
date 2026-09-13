"""Plain-language screening summary a person can take to a clinician visit."""

from __future__ import annotations

from datetime import date

from .engine import DISCLAIMER, ScreeningResult

CLINICIAN_QUESTIONS = [
    "Could my symptoms match a chronic inflammatory skin condition?",
    "What details should I track about my symptoms before my next visit?",
    "Would a referral to a dermatologist be appropriate?",
    "Are there skin-care steps I should or should not try in the meantime?",
]


def build_report(results: list[ScreeningResult]) -> str:
    """Render one or more screening results as a printable summary."""
    lines = [
        "Inflammatory Skin Condition Screening Summary",
        f"Generated: {date.today().isoformat()} (educational tool, not a diagnosis)",
        "",
    ]
    for result in results:
        lines += [
            f"Condition screened: {result.condition_name}",
            f"Result band: {result.band.upper()} (score {result.score}/100)",
            f"Questions answered: {result.questions_answered}/{result.questions_total}",
            result.band_guidance,
            "",
        ]
        if result.key_symptoms_endorsed:
            lines.append("Key symptoms you endorsed:")
            lines += [f"  - {text}" for text in result.key_symptoms_endorsed]
            lines.append("")
    lines += [
        "Questions you may want to ask your clinician:",
        *[f"  - {q}" for q in CLINICIAN_QUESTIONS],
        "",
        "Disclaimer:",
        DISCLAIMER,
    ]
    return "\n".join(lines)


def save_report(text: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
