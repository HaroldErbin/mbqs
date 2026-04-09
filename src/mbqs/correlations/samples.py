"""
Compute the experimental correlation functions from bitstrings.
"""

from mbqs.types import BitstringMap, Corr1ptMap, Corr2ptMap

from .utils import compute_connected_2pt_corr


class SampleCorrelations:
    """
    Compute the experimental correlation functions from bitstrings.
    """

    def __init__(self, bitstrings: BitstringMap):
        """
        Initialize the Ising correlations.

        Args:
            bitstrings: Bitstrings of the system.

        """
        self.bitstrings = bitstrings

    def compute_1pt_corr(self) -> Corr1ptMap:
        """
        Compute the 1-point correlation function.

        """

        return {}

    def compute_2pt_corr(self) -> Corr2ptMap:
        """
        Compute the 2-point correlation functions.

        """

        return {}

    def compute_connected_2pt_corr(self) -> Corr2ptMap:
        """
        Compute the connected 2-point correlation functions.

        """

        return compute_connected_2pt_corr(
            self.compute_1pt_corr(), self.compute_2pt_corr()
        )
