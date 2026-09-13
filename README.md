# inflamma-screen

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](pyproject.toml)
[![CI](https://github.com/developer-rpai/inflamma-screen/actions/workflows/ci.yml/badge.svg)](https://github.com/developer-rpai/inflamma-screen/actions)

An open-source educational toolkit that screens for commonly described symptom
patterns of chronic inflammatory skin conditions. Answer plain-language
questions, get a transparent banded result (low / moderate / elevated) with a
plain-language summary you can take to a clinician appointment.

> **Educational tool only. This is not a diagnosis.** inflamma-screen is not a
> medical device, has not been clinically validated, and cannot confirm or rule
> out any condition. Always discuss your symptoms with a qualified clinician.

## Quickstart

```bash
pip install inflamma-screen
```

```python
from inflamma_screen import score_condition

answers = {"hs_01": 2, "hs_02": 1, "hs_03": 0}  # 0 never, 1 sometimes, 2 often
result = score_condition("hidradenitis_suppurativa", answers)

print(result.band, result.score)  # e.g. moderate 47.7
print(result.disclaimer)          # every result carries the disclaimer
```

Prefer the terminal? Run the interactive screener:

```bash
python -m inflamma_screen.cli
```

Or try the zero-dependency web demo: open `web/index.html` in any browser
(a hosted demo link will be added here once deployed).

## Conditions covered

| Condition | Questions | Pattern screened |
|-----------|-----------|------------------|
| Hidradenitis suppurativa | 12 | Recurrent painful bumps in skin folds, draining lesions, tunnels, scarring |
| Psoriasis | 12 | Scaly plaques, nail changes, Koebner pattern, joint symptoms |
| Atopic dermatitis | 12 | Intense itch, flexural patches, atopic history, triggers |

Questions are educational screening prompts written in plain language. They are
not validated clinical instruments.

## How scoring works

Each question carries a weight of 1 to 3. Answers score 0 (never), 1
(sometimes), or 2 (often). The result is a weighted percentage:

```
score = 100 * sum(weight * answer) / (2 * sum(weight))
```

Bands: **low** below 30, **moderate** 30 to 60, **elevated** above 60.
Unanswered questions count as 0, so partial answers dilute toward lower bands.
Full details, worked examples, and limits are in [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## Project layout

```
inflamma_screen/      Python package (engine, CLI, clinician-ready reports)
  data/conditions.json   single source of truth for questions
web/                  static demo (vanilla HTML/CSS/JS, zero dependencies)
tests/                pytest suite (28 tests)
docs/METHODOLOGY.md   scoring rationale and limits
examples/quickstart.py
```

## Patient resources

- American Academy of Dermatology: https://www.aad.org
- HS Foundation: https://www.hs-foundation.org
- National Psoriasis Foundation: https://www.psoriasis.org
- National Eczema Association: https://nationaleczema.org

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The non-negotiable rules: every
user-facing result must carry the disclaimer, questions stay educational and
plain-language, and no personal health content of any kind.

## Citation

```bibtex
@software{pai2026inflammascreen,
  author  = {Pai, Mitra},
  title   = {inflamma-screen: an educational screening toolkit for chronic inflammatory skin conditions},
  version = {0.1.0},
  date    = {2026-09-12},
  url     = {https://github.com/developer-rpai/inflamma-screen}
}
```

## License

Apache-2.0. See [LICENSE](LICENSE).
