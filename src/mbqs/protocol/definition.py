"""
Data definining a protocol.
"""

from collections.abc import Mapping

from mbqs.simulations.state import State
from mbqs.types import QubitPairSeq, SystemSize

from .duration import Duration
from .lattice import get_2pt_idx


class MBQSProtocol:
    """
    Data defining a MBQS protocol.
    """

    def __init__(
        self,
        state: str,
        L: SystemSize,
        J: float,
    ):
        """
        Initialize the MBQS protocol.

        Args:
            state: State of the system.
            L: System size or sequence of system sizes.
            J: Ising coupling.

        """

        self.state = State(state)
        self.L = L
        self.J = J

    @property
    def corr_idx(self) -> QubitPairSeq:
        """
        Get the correlation indices for a given system size.

        Args:
            L: Number of qubits.

        Returns:
            QubitPairSeq: Sequence of qubit pairs for which to compute the correlations.

        """

        return get_2pt_idx(self.L)

    @property
    def surge_time(self) -> float:
        """
        Compute the surge time for a given system size.

        Args:
            L: Number of qubits.

        Returns:
            float: Surge time.

        """

        # FIXME: Use the surge time instead of the Lieb-Robinson time when the first is
        # correctly implemented.
        # return Duration(L=self.L, J=self.J, state=self.state).surge_time
        return Duration(L=self.L, J=self.J, state=self.state).lieb_robinson_time

    @property
    def summary(self) -> Mapping:
        """
        Get a summary of the protocol.

        Returns:
            Mapping: Summary of the protocol.

        """

        return {
            "state": str(self.state),
            "L": self.L,
            "J": self.J,
            "time": self.surge_time,
            "corr_idx": self.corr_idx,
        }
