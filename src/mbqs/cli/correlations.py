"""
Action to compute correlation functions from bitstrings.
"""

import json
import os
from typing import cast

from mbqs import RydbergMapping
from mbqs.cli.arguments import ARGS_DEFAULT
from mbqs.correlations import SampleCorrelations, SurgeCorrelations
from mbqs.json_utils import json_encode_keys


def _display_corr(corr, is_theory=False):
    """
    Display correlation functions.

    Args:
        corr: Dictionary containing the correlation functions.
        is_theory: Whether the correlations have been computed using a simulation.

    Returns:
        str: Formatted string containing the correlation functions.

    """

    text = "# Correlations"
    if is_theory is True:
        text += " (theory)"
    text += "\n\n"

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


def compute_correlations_from_samples(args):
    """
    Compute correlation functions from bitstrings.
    """

    with open(args.input) as f:
        samples_corr = SampleCorrelations(json.load(f))

    return samples_corr.correlations


def compute_exact_correlations(args):
    """
    Compute correlation functions from bitstrings.
    """

    L = args.L

    if args.J is None and args.a is None:
        args.J = cast(float, ARGS_DEFAULT["J"])

    if args.a is not None:
        level = args.level if args.level is not None else ARGS_DEFAULT["level"]
        level = cast(int, level)
        J = RydbergMapping.compute_J(args.a, level)
    else:
        J = args.J

    corr = SurgeCorrelations(J=J, state=args.state, L=L)

    results = {
        "J": J,
        "state": args.state,
        "L": L,
        "correlations": corr.correlations,
    }

    return results


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

    if args.input is not None:
        results = compute_correlations_from_samples(args)
        is_theory = False
    else:
        if args.L is None:
            raise ValueError("System size `-L` must be provided.")
        results = compute_exact_correlations(args)
        is_theory = True

    if display_on_cli is True:
        if "correlations" in results:
            corr = results["correlations"]
        else:
            corr = results

        print(_display_corr(corr, is_theory))

    if args.output is not None:
        with open(args.output, "w") as f:
            json.dump(json_encode_keys(results), f, indent=4)

    return os.EX_OK
