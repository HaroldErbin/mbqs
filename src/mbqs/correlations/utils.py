"""
Utilities for correlation functions.
"""

import re
from collections import defaultdict


def convert_2pt_dict(corr: dict) -> dict:
    """
    Convert the keys of the 2-point correlation functions.

    This converts the dict from `{szsz_1: ...}` to `{szsz: {(0, 1): ...}}`.
    """

    key_regex = re.compile(r"(szsz(?:_c)?)_(\d+)(_err)?")

    result_dict = defaultdict(dict)

    if "sz" in corr:
        result_dict["sz"] = corr["sz"]

    if "sz_err" in corr:
        result_dict["sz_err"] = corr["sz_err"]

    for key, value in corr.items():
        if not key.startswith("szsz"):
            continue

        parts = key_regex.match(key)
        if parts is None:
            raise ValueError(f"Invalid key: {key}")
        parts = parts.groups()

        corr_key = parts[0]
        if parts[2] is not None:
            corr_key += parts[2]

        idx = parts[1]
        print(idx)

        result_dict[corr_key][(0, int(idx))] = value

    return dict(result_dict)
