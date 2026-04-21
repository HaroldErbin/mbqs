"""
Compute the MBQS score.
"""

from collections.abc import Mapping, Sequence
from enum import IntEnum
from typing import Any, cast, overload

import numpy as np
from numpy.typing import NDArray

from mbqs.correlations import SampleCorrelations
from mbqs.protocol.data import find_data_type
from mbqs.simulations.state import State
from mbqs.types import BitstringMap, Corr2ptMap

from .metric import compute_metric


class TestSuccess(IntEnum):
    """
    Encoding for MBQS test outcomes.
    """

    __test__ = False

    FAILED = -1
    UNDECIDED = 0
    SUCCESS = 1


@overload
def compute_test_success(
    metric: float, metric_err: float = 0.0, *, threshold: float
) -> TestSuccess: ...


@overload
def compute_test_success(
    metric: float, metric_err: float = 0.0, *, threshold: Sequence[float]
) -> dict[float, TestSuccess]: ...


def compute_test_success(
    metric: float,
    metric_err: float = 0.0,
    *,
    threshold: float | Sequence[float] = 0.1,
) -> TestSuccess | dict[float, TestSuccess]:
    """
    Compute the MBQS success test from a metric and a threshold.

    Args:
        metric: Metric computed for a system size.
        metric_err: Error on the metric.
        threshold: Threshold for the success test.

    Returns:
        TestSuccess: MBQS success test.

    """

    if isinstance(threshold, Sequence):
        return {
            cast(float, eps): compute_test_success(
                metric, metric_err, threshold=cast(float, eps)
            )
            for eps in threshold
        }
    else:
        if metric > threshold:
            return TestSuccess.FAILED

        if metric + metric_err >= threshold:
            return TestSuccess.UNDECIDED
        else:
            return TestSuccess.SUCCESS


@overload
def compute_score(
    data: Mapping[int, Corr2ptMap] | Mapping[int, BitstringMap],
    data_errors: Mapping[int, Corr2ptMap] | None = None,
    *,
    J: float,
    state: State | str = State.down,
    threshold: float = 0.1,
    method: str = "qutip",
    stop_on_fail: bool = False,
) -> tuple[int, dict[int, Any]]: ...


@overload
def compute_score(
    data: Mapping[int, Corr2ptMap] | Mapping[int, BitstringMap],
    data_errors: Mapping[int, Corr2ptMap] | None = None,
    *,
    J: float,
    state: State | str = State.down,
    threshold: Sequence[float],
    method: str = "qutip",
    stop_on_fail: bool = False,
) -> tuple[dict[float, int], dict[int, Any]]: ...


def compute_score(
    data,
    data_errors=None,
    *,
    J,
    state=State.down,
    threshold=0.1,
    method="qutip",
    stop_on_fail=False,
):
    """
    Compute the MBQS metrics for each system size and the associated score.

    One can stop the evaluation on the first test failure in case one cares only about
    the score.

    The function can take a single threshold or a list of thresholds.
    """

    history = {}

    if isinstance(threshold, float):
        threshold = [threshold]

    score = {t: 0 for t in threshold}
    has_failed = {t: False for t in threshold}

    for L, corr in data.items():
        corr_errors = data_errors[L] if data_errors is not None else None

        results = compute_metric(
            corr, corr_errors, J=J, state=state, L=L, method=method
        )
        if isinstance(results, float):
            metric = results
            metric_err = 0.0
        else:
            metric, metric_err = results

        success = compute_test_success(metric, metric_err, threshold=threshold)

        history[L] = {
            "metric": metric,
            "success": success[threshold[0]] if len(threshold) == 1 else success,
        }

        for t, succ in success.items():
            if succ in (TestSuccess.FAILED, TestSuccess.UNDECIDED):
                has_failed[t] = True

            if succ is TestSuccess.SUCCESS and has_failed[t] is False:
                score[t] = L

        if stop_on_fail is True and TestSuccess.SUCCESS not in success.values():
            break

    if len(score) == 1:
        return score[threshold[0]], history

    return score, history


class MBQS:
    """
    Compute the MBQS score.
    """

    correlations: Mapping[int, Corr2ptMap] | None
    correlations_errors: Mapping[int, Corr2ptMap] | None
    samples: Mapping[int, BitstringMap] | None
    J: float
    state: State | str
    threshold: float | Sequence[float]
    score: int | dict[float, int] | None
    history: dict[int, Any] | None

    def __init__(
        self,
        data: Mapping[int, Corr2ptMap] | Mapping[int, BitstringMap],
        data_errors: Mapping[int, Corr2ptMap] | None = None,
        *,
        J: float,
        state: State | str = State.down,
        threshold: float | Sequence[float] = 0.1,
    ):
        """
        Initialize the MBQS scorer.

        Args:
            data: Dictionary of correlations or samples for different system sizes.
            data_errors: Dictionary of errors on the correlations.
            J: Coupling constant.
            state: State of the system.
            threshold: Threshold for the success test.

        """

        self.J = J
        self.state = state
        self.threshold = threshold

        data_type = find_data_type(data)

        if data_type == "correlations_sequence":
            data = cast(Mapping[int, Corr2ptMap], data)
            self.correlations = data
            self.correlations_errors = data_errors
        elif data_type == "samples_sequence":
            data = cast(Mapping[int, BitstringMap], data)
            self.samples = data

            corr_obj = {L: SampleCorrelations(s) for L, s in self.samples.items()}
            self.correlations = {
                L: val.correlations["szsz_c"] for L, val in corr_obj.items()
            }
            self.correlations_errors = {
                L: val.correlations["szsz_c_err"] for L, val in corr_obj.items()
            }
        else:
            raise ValueError(
                "Invalid data type: must be a dict of system sizes to samples or "
                "2-point correlations."
            )

        self.score = None
        self.history = None

    def compute_score(self, method: str = "qutip", stop_on_fail: bool = False) -> None:
        """
        Compute the MBQS score.
        """
        assert self.correlations is not None

        self.score, self.history = compute_score(
            self.correlations,
            self.correlations_errors,
            J=self.J,
            state=self.state,
            threshold=self.threshold,
            method=method,
            stop_on_fail=stop_on_fail,
        )

    def summary(self) -> dict:
        """
        Prepare a summary of the MBQS score.
        """

        summary = {
            "J": self.J,
            "state": self.state,
            "threshold": self.threshold,
            "score": self.score,
            "history": self.history,
        }
        return summary

    def extract_array(self, key: str) -> NDArray:
        """
        Extract an array from the history.

        This is useful for plotting.
        """

        if self.history is None:
            raise ValueError("No history computed yet.")

        match key:
            case "metric":
                return MBQS._metrics_as_array(self.history.values())
            case "success":
                return MBQS._success_as_array(self.history.values())
            case _:
                raise ValueError(f"Invalid key: {key}")

    @staticmethod
    def _metrics_as_array(history) -> NDArray:
        return np.array([values["metric"] for values in history])

    @staticmethod
    def _success_as_array(history) -> NDArray:
        def success_map(success):
            if isinstance(success, dict):
                return np.asarray(list(success.values()), dtype=float)
            else:
                return float(success)

        return np.squeeze(np.c_[[success_map(values["success"]) for values in history]])
