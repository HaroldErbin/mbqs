"""
Compute the MBQS metric.
"""

from typing import overload

import numpy as np

from mbqs.correlations import SampleCorrelations
from mbqs.simulations import ising_qutip
from mbqs.simulations.lattice import get_antipodal_idx
from mbqs.simulations.state import State, StateType
from mbqs.types import BitstringMap, Corr2ptMap, Metric


def compute_metric(
    data,
    data_err=None,
    *,
    state: StateType = State.down,
    L: int,
    method: str = "qutip",
):
    """
    Compute the MBQS metric from correlations or bitstrings.
    """

    first_key = next(iter(data))

    if isinstance(first_key, str):
        return metric_from_bitstring(data, state=state, L=L, method=method)
    elif isinstance(first_key, tuple):
        return metric_from_correlations(data, data_err, state=state, L=L, method=method)
    else:
        raise ValueError(f"Invalid data type: {type(first_key)}")


@overload
def metric_from_correlations(
    correlations: Corr2ptMap,
    correlations_errors: None = None,
    *,
    state: StateType,
    L: int,
    method: str = "qutip",
) -> Metric: ...


@overload
def metric_from_correlations(
    correlations: Corr2ptMap,
    correlations_errors: Corr2ptMap,
    *,
    state: StateType,
    L: int,
    method: str = "qutip",
) -> tuple[Metric, Metric]: ...


def metric_from_correlations(
    correlations,
    correlations_errors=None,
    *,
    state=State.down,
    L,
    method="qutip",
):
    """
    Compute the MBQS metric from correlation functions.
    """

    antipodal_idx = get_antipodal_idx(L)

    samples_set = set(correlations.keys())
    theory_set = set((0, i) for i in range(1, antipodal_idx + 1))

    if samples_set != theory_set:
        raise ValueError(
            "Correlations are not defined for all required pairs. "
            f"Missing pairs: {theory_set - samples_set}"
        )

    match method:
        case "qutip":
            duration = ising_qutip.get_surge_time(L=L, J=1.0, state=state, dt=0.001)

            _, theory_correlations = ising_qutip.make_quench(
                state=state,
                L=L,
                duration=duration,
                antipodal_only=False,
            )

        case _:
            raise ValueError(f"Method {method} is not implemented.")

    theory_values = np.array(
        list(theory_correlations[f"szsz_c_{i}"][1] for i in range(1, antipodal_idx + 1))
    )
    sample_values = np.array(
        [correlations[(0, i)] for i in range(1, antipodal_idx + 1)]
    )

    metric = np.mean(np.abs(theory_values - sample_values) / theory_values)

    if correlations_errors is not None:
        sample_errors = np.array(
            [correlations_errors[(0, i)] for i in range(1, antipodal_idx + 1)]
        )

        metric_err = np.mean(np.abs(sample_errors / theory_values))

        return metric, metric_err
    else:
        return metric


def metric_from_bitstring(
    bitstrings: BitstringMap,
    *,
    state: StateType = State.down,
    L: int,
    method: str = "qutip",
) -> tuple[Metric, Metric]:
    """
    Compute the MBQS metric from bitstrings.
    """

    samples_corr = SampleCorrelations(bitstrings)

    return metric_from_correlations(
        samples_corr.correlations["szsz_c"],
        samples_corr.correlations["szsz_c_err"],
        state=state,
        L=L,
        method=method,
    )
