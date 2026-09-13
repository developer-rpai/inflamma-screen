from inflamma_screen import score_condition

answers = {"hs_01": 2, "hs_02": 2, "hs_03": 1, "hs_04": 0,
           "hs_05": 1, "hs_06": 2, "hs_07": 1, "hs_08": 0,
           "hs_09": 0, "hs_10": 0, "hs_11": 1, "hs_12": 0}

result = score_condition("hidradenitis_suppurativa", answers)

print(f"{result.condition_name}: {result.band} ({result.score}/100)")
print(result.band_guidance)
print(result.disclaimer)
