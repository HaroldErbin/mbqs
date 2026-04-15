"""
Utilities for correlation functions.
"""

from collections import defaultdict


def convert_2pt_dict(corr: dict) -> dict:
    """
    Convert the keys of the 2-point correlation functions.

    This converts the dict from `{szsz_1: ...}` to `{szsz: {(0, 1): ...}}`.
    """

    result_dict = defaultdict(dict)

    if "sz" in corr:
        result_dict["sz"] = corr["sz"]

    if "sz_err" in corr:
        result_dict["sz_err"] = corr["sz_err"]

    for key, value in corr.items():
        if not key.startswith("szsz"):
            continue

        if key.endswith("err"):
            corr_key = key[:-6] + "_err"
            idx = key[-5:-4]
        else:
            corr_key = key[:-2]
            idx = key[-1]

        result_dict[corr_key][(0, int(idx))] = value

    return dict(result_dict)
