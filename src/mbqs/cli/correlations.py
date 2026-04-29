"""
Action to compute correlation functions from bitstrings.
"""

import json
import os

from mbqs import SampleCorrelations, SurgeCorrelations
from mbqs.json_utils import json_encode_keys


def _display_corr(results, is_theory=False):
    """
    Display correlation functions.

    Args:
        results: Dictionary containing the parameters and correlation functions.
        is_theory: Whether the correlations have been computed using a simulation.

    Returns:
        str: Formatted string containing the correlation functions.

    """

    text = "# Correlations"
    if is_theory is True:
        text += " (theory)"
    text += "\n\n"

    text += "## Parameters\n\n"
    text += f"- L = {results['L']}\n"

    if is_theory is True:
        text += f"- State = {results['state']}\n"
        text += f"- Jt = {results['Jt']}\n"

    text += "\n## Values\n\n"

    corr = results["correlations"]

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

    results = {
        "L": samples_corr.L,
        "correlations": samples_corr.correlations,
    }

    return results


def compute_exact_correlations(args):
    """
    Compute correlation functions from bitstrings.
    """

    L = args.L

    corr = SurgeCorrelations(state=args.state, L=L)

    results = {
        "state": args.state,
        "L": L,
        "Jt": corr.surge_time_J,
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
        print(_display_corr(results, is_theory))

    if args.output is not None:
        with open(args.output, "w") as f:
            json.dump(json_encode_keys(results), f, indent=4)

    return os.EX_OK
