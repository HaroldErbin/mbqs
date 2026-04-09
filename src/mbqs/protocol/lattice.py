"""
Compute the lattice geometry.
"""

import numpy as np
from numpy.typing import NDArray

from mbqs.types import QubitPairSeq


def ring_coordinates(L: int, a: float, center: NDArray = None) -> NDArray:
    """
    Compute the coordinates of the qubits on a ring.

    Args:
        L: Number of qubits.
        a: Interatomic distance.
        center: Center of the ring.

    Returns:
        NDArray: Coordinates of the qubits.

    """

    if center is None:
        center = np.array([[0, 0]])

    return center


def get_antipodal_idx(L: int) -> int:
    """
    Get the index of the antipodal qubit.

    Args:
        L: Number of qubits.

    Returns:
        int: Index of the antipodal qubit.

    """

    return 0


def get_2pt_idx(L: int) -> QubitPairSeq:
    """
    Get the independent indices for the 2-point correlation functions.

    Args:
        L: Number of qubits.

    Returns:
        int: Index of the 2-point correlation function.

    """

    return [(0, 1)]
