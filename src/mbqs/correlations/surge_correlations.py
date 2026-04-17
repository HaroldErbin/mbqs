"""
Class to contain correlations at surge time.
"""

from mbqs.correlations.utils import convert_2pt_dict
from mbqs.protocol.duration import Duration
from mbqs.simulations import ising_qutip
from mbqs.simulations.state import State


class SurgeCorrelations:
    """
    Class to contain correlations at surge time.
    """

    def __init__(
        self,
        *,
        J: float = 1.0,
        state: State | str = State.down,
        L: int,
        method: str = "qutip",
    ):
        """
        Initialize the SurgeCorrelations class.

        Args:
            J: Interaction strength.
            state: Initial state.
            L: System size.
            method: Method to use to compute the correlations.

        """

        self.J = J
        self.state = state
        self.L = L
        self.method = method

        self.duration = Duration(J=J, L=L, state=state)

        quench_results = ising_qutip.make_quench(
            J=J,
            state=state,
            L=L,
            duration=self.surge_time,
            antipodal_only=False,
        )
        self.correlations = convert_2pt_dict(
            {k: v[-1] for k, v in quench_results[1].items()}
        )

    @property
    def surge_time(self):
        """
        Compute the surge time.
        """

        return self.duration.surge_time(self.method)
