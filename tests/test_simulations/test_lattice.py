import logging

import numpy as np
import pytest

from mbqs.simulations.lattice import get_2pt_idx, get_antipodal_idx, ring_coordinates

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.mark.parametrize(
    ("L", "a", "coords"),
    [
        (1, 5, np.array([[0.0, 0.0]])),
        (2, 4, np.array([[2.0, 0.0], [-2.0, 0.0]])),
        (2, 5, np.array([[2.5, 0.0], [-2.5, 0.0]])),
        (3, 5, np.array([[2.88675135, 0.0], [-1.44337567, 2.5], [-1.44337567, -2.5]])),
        (
            10,
            5,
            np.array(
                [
                    [8.09016994e00, 0.00000000e00],
                    [6.54508497e00, 4.75528258e00],
                    [2.50000000e00, 7.69420884e00],
                    [-2.50000000e00, 7.69420884e00],
                    [-6.54508497e00, 4.75528258e00],
                    [-8.09016994e00, 9.90760073e-16],
                    [-6.54508497e00, -4.75528258e00],
                    [-2.50000000e00, -7.69420884e00],
                    [2.50000000e00, -7.69420884e00],
                    [6.54508497e00, -4.75528258e00],
                ]
            ),
        ),
    ],
)
def test_ring_coordinates(L, a, coords):

    assert np.allclose(ring_coordinates(L, a), coords)


@pytest.mark.parametrize(
    ("L", "a", "center", "coords"),
    [
        (2, 5, np.array([[1, 1]]), np.array([[3.5, 1.0], [-1.5, 1.0]])),
    ],
)
def test_ring_coordinates_center(L, a, center, coords):

    assert np.allclose(ring_coordinates(L, a, center=center), coords)


@pytest.mark.parametrize(
    ("L", "a", "rotate", "coords"),
    [
        (2, 5, np.pi / 2, np.array([[0.0, 2.5], [0.0, -2.5]])),
    ],
)
def test_ring_coordinates_rotate(L, a, rotate, coords):

    assert np.allclose(ring_coordinates(L, a, rotate=rotate), coords)


@pytest.mark.parametrize(
    ("L", "idx"),
    [
        (2, 1),
        (3, 1),
        (4, 2),
        (5, 2),
        (6, 3),
    ],
)
def test_get_antipodal_idx(L, idx):

    assert get_antipodal_idx(L) == idx


@pytest.mark.parametrize(
    ("L", "idx_list"),
    [
        (2, [(0, 1)]),
        (3, [(0, 1)]),
        (4, [(0, 1), (0, 2)]),
        (5, [(0, 1), (0, 2)]),
        (6, [(0, 1), (0, 2), (0, 3)]),
    ],
)
def test_get_2pt_idx(L, idx_list):

    assert get_2pt_idx(L) == idx_list
