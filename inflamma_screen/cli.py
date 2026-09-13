"""Interactive terminal screener for chronic inflammatory skin conditions."""

from __future__ import annotations

import argparse
import json
import sys

from .engine import (
    ANSWER_LABELS,
    DISCLAIMER,
    ScreeningResult,
    get_condition,
    list_conditions,
    score_condition,
)
from .report import build_report, save_report

PROMPT = "Your answer [0 never / 1 sometimes / 2 often]: "

_ALIASES = {
    "n": 0, "never": 0,
    "s": 1, "sometimes": 1,
    "o": 2, "often": 2,
}


def parse_answer(raw: str) -> int | None:
    raw = raw.strip().lower()
    if raw in ("0", "1", "2"):
        return int(raw)
    return _ALIASES.get(raw)


def ask_questions(condition: dict) -> dict[str, int]:
    answers: dict[str, int] = {}
    questions = condition["questions"]
    for i, question in enumerate(questions, 1):
        while True:
            print(f"\n[{i}/{len(questions)}] {question['text']}")
            value = parse_answer(input(PROMPT))
            if value is None:
                print("Please answer 0, 1, or 2 (or n/s/o).")
                continue
            answers[question["id"]] = value
            break
    return answers


def pick_condition() -> dict:
    options = list_conditions()
    print("Which condition would you like to screen for?\n")
    for i, (cid, name) in enumerate(options, 1):
        print(f"  {i}. {name}")
    while True:
        choice = input("\nEnter a number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return get_condition(options[int(choice) - 1][0])
        print("Please enter a valid number.")


def show_result(result: ScreeningResult) -> None:
    print("\n" + "=" * 60)
    print(f"{result.condition_name}: {result.band.upper()} ({result.score}/100)")
    print("=" * 60)
    print(result.band_guidance)
    if result.key_symptoms_endorsed:
        print("\nKey symptoms you endorsed:")
        for text in result.key_symptoms_endorsed:
            print(f"  - {text}")
    print(f"\n{DISCLAIMER}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inflamma-screen",
        description="Educational screening for chronic inflammatory skin conditions. Not a diagnostic tool.",
        add_help=False,
    )
    parser.add_argument("-h", action="help", help="show this help message")
    parser.add_argument("-c", metavar="CONDITION", default=None,
                        help="condition id to screen (skips the picker)")
    parser.add_argument("-o", metavar="FILE", default=None,
                        help="save a plain-language report to FILE")
    parser.add_argument("-j", action="store_true",
                        help="print the result as JSON instead of text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    print("inflamma-screen: educational symptom screening")
    print("This tool does not provide a diagnosis.\n")

    if args.c:
        try:
            condition = get_condition(args.c)
        except ValueError as exc:
            print(f"Error: {exc}")
            print("Available:", ", ".join(cid for cid, _ in list_conditions()))
            return 2
    else:
        condition = pick_condition()
    answers = ask_questions(condition)
    result = score_condition(condition["id"], answers)

    if args.j:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        show_result(result)

    if args.o:
        save_report(build_report([result]), args.o)
        print(f"\nReport saved to {args.o}")
    elif not args.j:
        save = input("\nSave a summary to take to a clinician? [y/N]: ").strip().lower()
        if save == "y":
            path = input("File path [screening-summary.txt]: ").strip() or "screening-summary.txt"
            save_report(build_report([result]), path)
            print(f"Report saved to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
