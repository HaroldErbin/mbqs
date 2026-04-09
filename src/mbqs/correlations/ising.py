"""
Compute the theoretical correlation functions for the critical Ising model.
"""

from mbqs.types import Corr1ptMap, Corr2ptMap

from .utils import compute_connected_2pt_corr


class IsingCorrelations:
    """
    Compute the theoretical correlation functions for the critical Ising model.
    """

    def __init__(self, J: float, state: str):
        """
        Initialize the Ising correlations.
        """

        self.J = J
        self.state = state

    def compute_1pt_corr(self, t: float) -> Corr1ptMap:
        """
        Compute the 1-point correlation function.

        """

        return {}

    def compute_2pt_corr(self, t: float) -> Corr2ptMap:
        """
        Compute the 2-point correlation functions.

        """

        return {}

    def compute_connected_2pt_corr(self, t: float) -> Corr2ptMap:
        """
        Compute the connected 2-point correlation functions.

        """

        return compute_connected_2pt_corr(
            self.compute_1pt_corr(t), self.compute_2pt_corr(t)
        )
