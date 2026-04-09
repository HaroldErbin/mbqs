"""
Compute the MBQS score.
"""

from collections.abc import Mapping

from mbqs.types import BitstringMap, Corr2ptMap, MetricMap


def get_test_success(metric: float, threshold: float) -> bool:
    """
    Compute the MBQS success test from a metric and a threshold.

    Args:
        metric: Metric computed for a system size.
        threshold: Threshold for the success test.

    Returns:
        float: MBQS success test.

    """

    return False


def compute_score(metrics: MetricMap, threshold: float) -> int:
    """
    Compute the MBQS score from a list of metrics and a threshold.

    Args:
        metrics: Metric computed for each system size.
        threshold: Threshold for the success test.

    """

    return 0


class MBQS:
    """
    Compute the MBQS score.
    """

    def __init__(
        self,
        state: str,
        threshold: float,
        /,
        correlations: Mapping[int, Corr2ptMap] | None = None,
        bitstrings: Mapping[int, BitstringMap] | None = None,
    ):
        """
        Initialize the MBQS scorer.

        Args:
            correlations: Dictionary of correlations for different system sizes.
            bitstrings: Dictionary of bitstrings for different system sizes.
            state: State of the system.
            threshold: Threshold for the success test.

        """

        self.correlations = correlations
        self.bitstrings = bitstrings
        self.state = state
        self.threshold = threshold

        if self.correlations is None:
            # compute from bitsrings (raise error if absent)
            pass

    def metrics(self) -> MetricMap:
        """
        Compute the MBQS metrics for each system size.

        Returns:
            MetricMap: Dictionary of metrics.

        """

        return {}

    def score(self) -> int:
        """
        Compute the MBQS score.

        Returns:
            int: MBQS score.

        """

        return 0
