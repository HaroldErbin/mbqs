"""
CLI action to score the results of the MBQS protocol.
"""

import json
import os
from pathlib import Path

from mbqs import MBQS
from mbqs.json_utils import json_decode_keys

protocol_text = [
    "State = {state}",
    "Jt = {J:.4g}",
    "Threshold = {threshold}",
]

size_text = "L = {L}"

score_text = "Score = {score}"
success_text = "Test: {success!s}"


def _metric_text(metric, metric_err=0.0, **kwargs):
    text = f"P2 = {metric:.4g}"
    if metric_err > 0:
        text += f" ± {metric_err:.4g}"

    return text


def _display_text(data):

    if "score" in data:
        text = "# MBQS score\n\n"
        text += "\n".join(protocol_text).format(**data)
        text += f"\n\n*{score_text.format(**data)}*"
        text += "\n\n## History\n\n"

        for L, dic in data["history"].items():
            text += f"L = {L}\n"
            text += f"- {_metric_text(**dic)}\n"
            text += f"- {success_text.format(**dic)}\n"
            text += "\n"

        text = text.strip("\n")
    else:
        text = "# MBQS metric\n\n"
        protocol_text.insert(-1, size_text)
        text += "\n".join(protocol_text).format(**data)
        text += "\n\n"
        text += _metric_text(**data)
        text += f"\n{success_text.format(**data)}"

    return text


def scorer_action(args):
    """
    Execute the scorer action.
    """

    input_path = Path(args.input)
    with open(input_path) as f:
        data = json.load(f)
        data = json_decode_keys(data)

    parameters = {}
    if args.state is not None:
        parameters["state"] = args.state
    if args.L is not None:
        parameters["L"] = args.L
    if args.threshold is not None:
        parameters["threshold"] = args.threshold

    mbqs = MBQS(data=data, **parameters)
    if "_sequence" in mbqs.data_type:
        mbqs.compute_score()
    else:
        mbqs.compute_metric()

    print(_display_text(mbqs.summary()))

    return os.EX_OK
