"""
Compute the MBQS score.
"""

from collections.abc import Mapping, Sequence
from enum import IntEnum
from typing import Any, cast, overload

import numpy as np
from numpy.typing import NDArray

from mbqs.correlations import SampleCorrelations
from mbqs.protocol.data_utils import find_data_type, find_protocol_parameters
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

    correlations: Corr2ptMap | Mapping[int, Corr2ptMap] | None
    correlations_errors: Corr2ptMap | Mapping[int, Corr2ptMap] | None
    samples: BitstringMap | Mapping[int, BitstringMap] | None
    J: float
    state: State | str
    L: int | Sequence[int] | None
    threshold: float | Sequence[float]

    score: int | dict[float, int] | None = None
    history: dict[int, Any] | None = None
    metric: float | dict[int, float] | None = None
    metric_err: float | dict[int, float] = 0.0
    success: TestSuccess | dict[float, TestSuccess] | None = None

    data_type: str

    def __init__(
        self,
        data: Corr2ptMap
        | BitstringMap
        | Mapping[str, Any]
        | Mapping[int, Corr2ptMap]
        | Mapping[int, BitstringMap],
        data_errors: Corr2ptMap
        | Mapping[int, Corr2ptMap]
        | Mapping[str, Any]
        | None = None,
        *,
        J: float = 1.0,
        state: State | str = State.down,
        L: int | None = None,
        threshold: float | Sequence[float] = 0.1,
    ):
        """
        Initialize the MBQS scorer.

        Args:
            data: Dictionary of correlations or samples for different system sizes.
            data_errors: Dictionary of errors on the correlations.
            J: Coupling constant.
            state: State of the system.
            L: System size.
            threshold: Threshold for the success test.

        """

        data_type = find_data_type(cast(Mapping[str, Any], data))
        parameters = find_protocol_parameters(cast(Mapping[str, Any], data))

        self.J = parameters.get("J", J)
        self.state = State(parameters.get("state", state))
        self.threshold = parameters.get("threshold", threshold)

        if data_type == "protocol":
            raise ValueError("Data must contain either correlations or samples.")

        if data_type.startswith("protocol_"):
            if isinstance(data, dict):
                data_dict = cast(Mapping[str, Any], data)
                if "correlations" in data_dict:
                    data = data_dict["correlations"]
                elif "samples" in data_dict:
                    data = data_dict["samples"]

            data_type = data_type.removeprefix("protocol_")

        self.data_type = data_type

        match data_type:
            case "correlations":
                self.correlations = cast(Corr2ptMap, data)
                self.correlations_errors = cast(Corr2ptMap, data_errors)

            case "correlations_dict":
                data_dict = cast(Mapping[str, Any], data)
                if data_errors is not None:
                    data_errors_dict = cast(Mapping[str, Any], data_errors)
                    self.correlations_errors = cast(
                        Corr2ptMap, data_errors_dict["szsz_c_err"]
                    )
                elif "szsz_c_err" in data_dict:
                    self.correlations_errors = cast(Corr2ptMap, data_dict["szsz_c_err"])
                else:
                    self.correlations_errors = None

                self.correlations = cast(Corr2ptMap, data_dict["szsz_c"])

                self.data_type = "correlations"

            case "samples":
                self.samples = cast(BitstringMap, data)

                L = len(next(iter(self.samples.keys())))

                corr_obj = SampleCorrelations(self.samples)
                self.correlations = corr_obj.correlations["szsz_c"]
                self.correlations_errors = corr_obj.correlations["szsz_c_err"]

            case "correlations_sequence":
                self.correlations = cast(Mapping[int, Corr2ptMap], data)
                self.correlations_errors = cast(Mapping[int, Corr2ptMap], data_errors)

            case "samples_sequence":
                self.samples = cast(Mapping[int, BitstringMap], data)

                corr_obj = {L: SampleCorrelations(s) for L, s in self.samples.items()}
                self.correlations = {
                    L: val.correlations["szsz_c"] for L, val in corr_obj.items()
                }
                self.correlations_errors = {
                    L: val.correlations["szsz_c_err"] for L, val in corr_obj.items()
                }

            case _:
                raise ValueError("Invalid data type.")

        if self.data_type in ("samples_sequence", "correlations_sequence"):
            if L is not None:
                raise ValueError("L should not be provided when data is a sequence.")

            self.L = list(self.correlations.keys())
        else:
            L = parameters.get("L", L)
            if L is None:
                raise ValueError("L must be provided when data is not a sequence.")

            self.L = int(L)

    def compute_score(self, method: str = "qutip", stop_on_fail: bool = False) -> None:
        """
        Compute the MBQS score.
        """

        assert self.correlations is not None

        if self.data_type not in ("correlations_sequence", "samples_sequence"):
            raise TypeError("Data type must be a sequence to evaluate the score.")

        self.correlations = cast(Mapping[int, Corr2ptMap], self.correlations)
        self.correlations_errors = cast(
            Mapping[int, Corr2ptMap], self.correlations_errors
        )

        self.score, self.history = compute_score(
            self.correlations,
            self.correlations_errors,
            J=self.J,
            state=self.state,
            threshold=self.threshold,
            method=method,
            stop_on_fail=stop_on_fail,
        )

    def compute_metric(self, method: str = "qutip") -> None:
        """
        Compute the MBQS metric.
        """

        assert self.correlations is not None

        if self.data_type not in ("correlations", "samples"):
            raise TypeError("Data type must not be a sequence to evaluate the metric.")

        self.correlations = cast(Corr2ptMap, self.correlations)
        self.correlations_errors = cast(Corr2ptMap, self.correlations_errors)

        result = compute_metric(
            self.correlations,
            self.correlations_errors,
            J=self.J,
            state=self.state,
            L=cast(int, self.L),
            method=method,
        )

        if isinstance(result, tuple):
            self.metric, self.metric_err = result
        else:
            self.metric = result
            self.metric_err = 0.0

        self.success = compute_test_success(
            self.metric,
            self.metric_err,
            threshold=self.threshold,
        )

    def summary(self) -> dict[str, Any]:
        """
        Prepare a summary of the MBQS score.
        """

        summary: dict[str, Any] = {
            "J": self.J,
            "state": self.state,
            "threshold": self.threshold,
        }

        if self.data_type in ("correlations_sequence", "samples_sequence"):
            summary["score"] = self.score
            summary["history"] = self.history
        else:
            summary["metric"] = self.metric
            if self.metric_err != 0:
                summary["metric_err"] = self.metric_err
            summary["success"] = self.success
            summary["L"] = self.L

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
