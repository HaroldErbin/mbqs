"""
Data definining a protocol.
"""

from collections.abc import Mapping

from mbqs.types import QubitPairSeq, SystemSize, SystemSizeSeq


class MBQSProtocol:
    """
    Data defining a MBQS protocol.
    """

    def __init__(
        self,
        state: str,
        L: SystemSize | SystemSizeSeq,
    ):
        """
        Initialize the MBQS protocol.

        Args:
            state: State of the system.
            L: System size or sequence of system sizes.

        """

        self.state = state
        self.L = L

    @property
    def corr_idx(self) -> QubitPairSeq | Mapping[int, QubitPairSeq]:
        """
        Get the correlation indices for a given system size.

        Args:
            L: Number of qubits.

        Returns:
            QubitPairSeq: Sequence of qubit pairs for which to compute the correlations.

        """

        return [(0, 1)]

    @property
    def surge_time(self) -> float | Mapping[int, float]:
        """
        Compute the surge time for a given system size.

        Args:
            L: Number of qubits.

        Returns:
            float: Surge time.

        """

        return 0.0

    def summary(self) -> dict:
        """
        Get a summary of the protocol.

        Returns:
            dict: Summary of the protocol.

        """

        return {}
