"""Regenerate web/questions.js from the packaged conditions data.

The web demo ships its own copy of the questionnaire data so it works as a
fully static page. Run this after editing inflamma_screen/data/conditions.json:

    python3 scripts/build_web_data.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "inflamma_screen" / "data" / "conditions.json"
DST = ROOT / "web" / "questions.js"


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    DST.write_text(
        "/* Generated from inflamma_screen/data/conditions.json by "
        "scripts/build_web_data.py. Do not edit by hand. */\n"
        f"window.INFLAMMA_SCREEN_DATA = {payload};\n",
        encoding="utf-8",
    )
    print(f"wrote {DST} ({len(data['conditions'])} conditions)")


if __name__ == "__main__":
    main()
