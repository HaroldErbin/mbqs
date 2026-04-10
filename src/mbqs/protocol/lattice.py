"""
Compute the lattice geometry.
"""

from collections.abc import Sequence
from typing import cast

import numpy as np
from numpy.typing import NDArray

from mbqs.types import QubitPairSeq


def ring_coordinates(
    L: int,
    a: float,
    center: Sequence[float] | NDArray | None = None,
    rotate: float = 0.0,
) -> NDArray:
    """
    Compute the coordinates of the qubits on a ring.

    Args:
        L: Number of qubits.
        a: Interatomic distance.
        center: Center of the ring, as an array of shape (1, 2,).
        rotate: Rotation angle of the ring (in radians).

    Returns:
        NDArray: Coordinates of the qubits, as an array of shape (L, 2).

    """

    if center is None:
        center = np.array([[0, 0]])

    center = np.array(center).reshape(1, 2)

    if L == 1:
        return center

    coords = center + (
        a
        / (2 * np.sin(np.pi / L))
        * np.array(
            [
                (np.cos(theta + rotate), np.sin(theta + rotate))
                for theta in 2 * np.pi / L * np.arange(L)
            ]
        )
    )

    return cast(NDArray, coords)


def get_antipodal_idx(L: int) -> int:
    """
    Get the index of the antipodal qubit.

    Args:
        L: Number of qubits.

    Returns:
        int: Index of the antipodal qubit.

    """

    return L // 2


def get_2pt_idx(L: int) -> QubitPairSeq:
    """
    Get the independent indices for the 2-point correlation functions.

    Args:
        L: Number of qubits.

    Returns:
        int: Index of the 2-point correlation function.

    """

    return [(0, i) for i in range(1, get_antipodal_idx(L) + 1)]
