# Contributing

Thanks for your interest in inflamma-screen. This project is educational and
non-diagnostic by design; every contribution must keep it that way.

## Ground rules

- **Non-diagnostic always.** Any new user-facing result, report, or page must
  include the full disclaimer from `inflamma_screen/engine.py`. If your change
  adds a surface where results appear, add a test asserting the disclaimer is
  present.
- **Educational prompts, not instruments.** Questions must stay plain-language
  and must never be presented as validated clinical tools.
- **No personal health content.** Do not add anecdotes, case details, or
  anything about any individual's health, including the author's.

## Development setup

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[test]"
.venv/bin/python -m pytest -q
```

## Adding or editing questions

1. Edit `inflamma_screen/data/conditions.json` (the single source of truth).
2. Keep 10 to 14 questions per condition, plain language, weights 1 to 3.
3. Mark at most 4 questions per condition as `"key": true`.
4. Run `python3 scripts/build_web_data.py` to refresh `web/questions.js`.
5. Run the test suite. Update `docs/METHODOLOGY.md` if scoring changes.

## Code style

Clean, idiomatic Python; comments only where the why is not obvious. No filler.

## Opening a pull request

Describe what changed, why, and how you tested it. CI runs the full pytest
suite on Python 3.10 through 3.12.
