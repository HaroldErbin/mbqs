"""
Class to contain correlations at surge time.
"""

from mbqs.protocol.duration import Duration
from mbqs.simulations import ising_qutip, ising_tabulated
from mbqs.simulations.state import State, StateType


class SurgeCorrelations:
    """
    Class to contain correlations at surge time.
    """

    def __init__(
        self,
        *,
        state: StateType = State.down,
        L: int,
        method: str = "tabulated",
    ):
        """
        Initialize the SurgeCorrelations class.

        Args:
            state: Initial state.
            L: System size.
            method: Method to use to compute the correlations.

        """

        self.state = state
        self.L = L
        self.method = method

        self.duration = Duration(J=1.0, L=L, state=state)
        self.correlations = self.compute_correlations(L=L, state=state, method=method)

    @property
    def surge_time_J(self):
        """
        Compute the surge time in units of J.
        """

        return self.duration.surge_time(self.method)

    @property
    def fermions_correlations(self):
        """
        Compute the correlations for the Ising model using fermions.
        """

        return SurgeCorrelations.compute_correlations(
            L=self.L, state=self.state, method="fermions"
        )

    @property
    def qutip_correlations(self):
        """
        Compute the correlations for the Ising model using qutip.
        """

        return SurgeCorrelations.compute_correlations(
            L=self.L, state=self.state, method="qutip"
        )

    @property
    def tabulated_correlations(self):
        """
        Compute the correlations for the Ising model using tabulated data.
        """

        return SurgeCorrelations.compute_correlations(
            L=self.L, state=self.state, method="tabulated"
        )

    @staticmethod
    def compute_correlations(
        *, L: int, state=State.down, surge_time=None, method="tabulated"
    ) -> float:
        """
        Compute the surge correlations.
        """

        match method:
            case "fermions":
                raise NotImplementedError
            case "qutip":
                correlations = ising_qutip.get_correlations(
                    L=L, state=state, surge_time=surge_time
                )
            case "tabulated":
                try:
                    correlations = ising_tabulated.get_correlations(L=L, state=state)
                except KeyError:
                    correlations = SurgeCorrelations.compute_correlations(
                        L=L, state=state, method="fermions"
                    )
            case _:
                raise ValueError(f"Unknown method to compute surge time: {method}")

        return correlations
