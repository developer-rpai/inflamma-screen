# Methodology

This document explains how inflamma-screen scores answers, why the bands are
drawn where they are, and, just as importantly, what the scores cannot tell you.

## What this tool is

inflamma-screen is an **educational screening toolkit**. It asks plain-language
questions about commonly described symptom patterns for three chronic
inflammatory skin conditions (hidradenitis suppurativa, psoriasis, atopic
dermatitis) and reports how closely a person's answers overlap those patterns.

The questions are **educational screening prompts, not validated clinical
instruments**. They were written to be understandable, not to replicate any
diagnostic criteria, and the tool has not undergone clinical validation.

## How scoring works

Each question has a weight of 1 to 3, reflecting how characteristic the symptom
is of the condition's commonly described pattern. Key symptoms (for example,
recurrent draining bumps in skin folds for HS-type patterns) carry the highest
weights.

Answers use a three-point scale:

| Answer    | Value |
|-----------|-------|
| Never     | 0     |
| Sometimes | 1     |
| Often     | 2     |

The score is a weighted percentage:

```
score = 100 * sum(weight * answer) / (2 * sum(weight))
```

Unanswered questions count as 0, so a partial answer set dilutes toward lower
bands rather than inflating the result. Worked example: if the answered
questions contribute a weighted sum of 21 out of a possible 44, the score is
`100 * 21 / 44 = 47.7`.

## Result bands

| Band     | Score range | Meaning                                            |
|----------|-------------|----------------------------------------------------|
| Low      | below 30    | Limited overlap with described patterns            |
| Moderate | 30 to 60    | Some overlap; worth noting and discussing          |
| Elevated | above 60    | Notable overlap; consider a clinician appointment  |

The cutoffs are deliberately conservative: reaching "elevated" requires
endorsing a clear majority of the weighted symptom pattern. A single symptom,
even a key one, cannot produce an elevated band on its own.

## Limits

- **Not diagnostic.** Symptom overlap is not a diagnosis. Many skin conditions
  share features, and only a qualified clinician with a physical examination
  can diagnose.
- **Not validated.** The questions and weights reflect commonly described
  patterns from patient-education sources, not a validated instrument. Scores
  have no established sensitivity or specificity.
- **Self-report bias.** People interpret and recall symptoms differently, which
  moves scores in ways the tool cannot correct for.
- **No examination.** The tool cannot see the skin. Location, appearance, and
  texture details that matter clinically are absent by design.
- **Overlap between conditions.** Inflammatory skin conditions share symptoms
  (itching, redness, flares). A high band for one pattern does not exclude
  another condition.

## Design choices for safety

- Every result object, report, and web page carries the full disclaimer.
- Partial answers dilute toward lower bands (see above).
- The web demo and the Python engine implement identical scoring; the question
  data has a single source of truth (`inflamma_screen/data/conditions.json`,
  copied to the web bundle by `scripts/build_web_data.py`).
