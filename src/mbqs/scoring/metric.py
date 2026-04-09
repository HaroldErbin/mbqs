"""
Compute the MBQS metric.
"""

from mbqs.correlations import SampleCorrelations
from mbqs.types import BitstringMap, Corr2ptMap


def metric_from_bitstring(state: str, bitstrings: BitstringMap) -> float:
    """
    Compute the MBQS metric from bitstrings.
    """

    correlations = SampleCorrelations(bitstrings).compute_connected_2pt_corr()

    return metric_from_correlations(state, correlations)


def metric_from_correlations(state: str, correlations: Corr2ptMap) -> float:
    """
    Compute the MBQS metric from correlation functions.
    """

    return 0.0
