"""
Results for the MBQS protocol using tabulated data.
"""

import json
from pathlib import Path

from mbqs.json_utils import json_decode_keys

from .state import State, StateType

_DATA_PATH = Path(__file__).parent.parent / "data"


def get_surge_time(
    *,
    L: int,
    J: float = 1.0,
    state: StateType = State.down,
    dt: float = 0.001,
    interpolate: bool = False,
):
    """
    Compute the surge time for the Ising Hamiltonian from tabulated data.
    """

    state = State(state)

    data_path = _DATA_PATH / "table_surge_times.json"

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    return float(data[str(state)][str(L)]) / J


def get_correlations(
    *,
    L: int,
    state: StateType = State.down,
):
    """
    Compute the correlation functions for the Ising Hamiltonian from tabulated data.
    """

    state = State(state)

    data_path = _DATA_PATH / "table_correlations.json"

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    correlations = data[str(state)][str(L)]

    return json_decode_keys(correlations)
