"""
CLI action to score the results of the MBQS protocol.
"""

import json
import os
from pathlib import Path

from mbqs import MBQS
from mbqs.json_utils import json_decode_keys


def scorer_action(args):
    """
    Execute the scorer action.
    """

    input_path = Path(args.input)
    with open(input_path) as f:
        data = json.load(f)
        data = json_decode_keys(data)

    parameters = {}
    if args.J is not None:
        parameters["J"] = args.J
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

    print(mbqs.summary())

    return os.EX_OK
