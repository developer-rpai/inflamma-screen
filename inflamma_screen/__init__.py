"""Educational screening toolkit for chronic inflammatory skin conditions."""

from .engine import (
    ANSWER_LABELS,
    DISCLAIMER,
    ScreeningResult,
    get_condition,
    list_conditions,
    load_conditions,
    screen_all,
    score_condition,
)

__version__ = "0.1.0"
__all__ = [
    "ANSWER_LABELS",
    "DISCLAIMER",
    "ScreeningResult",
    "get_condition",
    "list_conditions",
    "load_conditions",
    "screen_all",
    "score_condition",
]
