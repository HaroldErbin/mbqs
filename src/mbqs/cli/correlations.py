"""
Action to compute correlation functions from bitstrings.
"""

import json
import os

from mbqs.correlations.samples import SampleCorrelations
from mbqs.correlations.utils import convert_2pt_dict


def _display_corr(corr):
    """
    Display correlation functions.

    Args:
        corr: Dictionary containing the correlation functions.

    Returns:
        str: Formatted string containing the correlation functions.

    """

    text = "# Correlations\n\n"

    for key, values in corr.items():
        if key.endswith("_err"):
            continue

        text += f"- {key}"

        if isinstance(values, dict):
            text += "\n"
            for idx, value in values.items():
                text += f"  - {idx} = {value:.3g}"
                if f"{key}_err" in corr:
                    text += f" ± {corr[f'{key}_err'][idx]:.3g}"
                text += "\n"
        else:
            text += f" = {values:.3g}"
            if f"{key}_err" in corr:
                text += f" ± {corr[f'{key}_err']:.3g}"
            text += "\n"

    return text


def _json_encode_keys(data):
    conv = {}

    if not isinstance(data, dict):
        return data

    for k, v in data.items():
        if isinstance(k, tuple):
            k = str(k)

        conv[k] = _json_encode_keys(v)

    return conv


def correlations_action(args) -> int:
    """
    Compute correlation functions from bitstrings.

    Args:
        args: Parsed arguments from the command line.

    Returns:
        Exit code.

    """

    if args.output is not None and args.verbose is False:
        display_on_cli = False
    else:
        display_on_cli = True

    with open(args.input) as f:
        samples = SampleCorrelations(json.load(f))

    corr = convert_2pt_dict(samples.correlations)

    if display_on_cli is True:
        print(_display_corr(corr))

    if args.output is not None:
        with open(args.output, "w") as f:
            json.dump(_json_encode_keys(corr), f, indent=4)

    return os.EX_OK
