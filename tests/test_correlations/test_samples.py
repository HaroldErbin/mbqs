from collections import Counter

import numpy as np
import pytest
from numpy.typing import NDArray

from mbqs.correlations.samples import (
    SampleCorrelations,
    average_corr_1pt,
    average_corr_2pt,
    bits_list_to_sign_array,
    compute_connected_2pt_corr,
    get_sign_tensor,
    samples_corr_npt,
    samples_map_to_arrays,
)
from mbqs.types import BitstringMap

ATOL = 1e-4

samples_L3 = Counter(
    {
        "000": 665,
        "111": 343,
        "100": 180,
        "010": 179,
        "001": 176,
        "101": 154,
        "011": 152,
        "110": 151,
    }
)


corr_L3 = {
    "sz": np.array([-0.172, -0.175, -0.175]),
    "szsz": np.array(
        [
            [1.0, 0.335, 0.341],
            [0.335, 1.0, 0.34],
            [0.341, 0.34, 1.0],
        ]
    ),
    "sz_err": np.array([0.022, 0.022, 0.022]),
    "szsz_err": np.array(
        [
            [0.0, 0.0211, 0.021],
            [0.0211, 0.0, 0.021],
            [0.021, 0.021, 0.0],
        ]
    ),
}

samples_L5 = {
    "00000": 1929,
    "11111": 675,
    "00100": 261,
    "10000": 285,
    "00010": 245,
    "01110": 127,
    "01000": 232,
    "00111": 144,
    "11101": 158,
    "11001": 234,
    "00001": 201,
    "10111": 167,
    "01111": 148,
    "00110": 144,
    "10001": 130,
    "10110": 154,
    "01100": 128,
    "11110": 179,
    "01010": 113,
    "11000": 112,
    "10100": 84,
    "01001": 123,
    "11011": 151,
    "00011": 113,
    "11010": 114,
    "11100": 85,
    "10101": 101,
    "00101": 109,
    "10011": 76,
    "10010": 99,
    "01101": 83,
    "01011": 96,
}

corr_L5 = {
    "sz": np.array(
        [
            -0.1989,
            -0.212,
            -0.2151,
            -0.2157,
            -0.226,
        ]
    ),
    "szsz": np.array(
        [
            [1.0, 0.3869, 0.33, 0.3374, 0.3917],
            [0.3869, 1.0, 0.3317, 0.3437, 0.3911],
            [0.33, 0.3317, 1.0, 0.424, 0.3469],
            [0.3374, 0.3437, 0.424, 1.0, 0.3389],
            [0.3917, 0.3911, 0.3469, 0.3389, 1.0],
        ]
    ),
    "sz_err": np.array(
        [
            0.0117,
            0.0117,
            0.0117,
            0.0117,
            0.0116,
        ]
    ),
    "szsz_err": np.array(
        [
            [0.0, 0.011, 0.0113, 0.0113, 0.011],
            [0.011, 0.0, 0.0113, 0.0112, 0.011],
            [0.0113, 0.0113, 0.0, 0.0108, 0.0112],
            [0.0113, 0.0112, 0.0108, 0.0, 0.0112],
            [0.011, 0.011, 0.0112, 0.0112, 0.0],
        ]
    ),
    "szsz_c": np.array(
        [
            [0.9605, 0.3447, 0.2872, 0.2945, 0.3468],
            [0.3447, 0.9551, 0.2861, 0.298, 0.3432],
            [0.2872, 0.2861, 0.9537, 0.3776, 0.2982],
            [0.2945, 0.298, 0.3776, 0.9535, 0.2901],
            [0.3468, 0.3432, 0.2982, 0.2901, 0.9489],
        ]
    ),
    "szsz_c_err": np.array(
        [
            [0.0047, 0.0158, 0.0161, 0.0161, 0.016],
            [0.0158, 0.005, 0.0163, 0.0162, 0.0161],
            [0.0161, 0.0163, 0.005, 0.0159, 0.0164],
            [0.0161, 0.0162, 0.0159, 0.005, 0.0164],
            [0.016, 0.0161, 0.0164, 0.0164, 0.0053],
        ]
    ),
}

expected_signs = np.array(
    [
        [-1, 1, 1, -1, -1, 1, -1, 1],
        [-1, 1, -1, 1, -1, -1, 1, 1],
        [-1, 1, -1, -1, 1, 1, 1, -1],
    ]
)
expected_counts = np.array(list(samples_L3.values()))


def test_sample_correlations_init() -> None:
    """
    Test initialization of the SampleCorrelations class.
    """

    samples_corr = SampleCorrelations(samples_L3)

    assert np.allclose(samples_corr.corr_1pt, corr_L3["sz"], atol=ATOL)
    assert np.allclose(samples_corr.corr_2pt, corr_L3["szsz"], atol=ATOL)

    assert hasattr(samples_corr, "corr_2pt_c")
    assert hasattr(samples_corr, "corr_2pt_c_err")

    correlations = samples_corr.correlations
    assert np.isclose(correlations["sz"], -0.174, atol=ATOL)
    assert np.isclose(correlations["sz_err"], 0.0220, atol=ATOL)
    assert np.isclose(correlations["szsz"][(0, 1)], 0.3387, atol=ATOL)
    assert np.isclose(correlations["szsz_err"][(0, 1)], 0.0210, atol=ATOL)
    assert np.isclose(correlations["szsz_c"][(0, 1)], 0.3084, atol=ATOL)
    assert np.isclose(correlations["szsz_c_err"][(0, 1)], 0.0287, atol=ATOL)


def test_bits_list_to_sign_array() -> None:
    """Test conversion of a list of bitstrings to a sign array."""
    bits_list = list(samples_L3.keys())

    assert np.allclose(bits_list_to_sign_array(bits_list), expected_signs)


def test_samples_map_to_arrays() -> None:
    """Test conversion of bitstrings dictionary with counts to expected arrays."""
    signs, counts = samples_map_to_arrays(samples_L3)

    assert np.allclose(signs, expected_signs)
    assert np.allclose(counts, expected_counts)


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (
            1,
            np.array(
                [
                    [-1, 1, 1, -1, -1, 1, -1, 1],
                    [-1, 1, -1, 1, -1, -1, 1, 1],
                    [-1, 1, -1, -1, 1, 1, 1, -1],
                ]
            ),
        ),
        (
            2,
            np.array(
                [
                    [
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, -1, -1, 1, -1, -1, 1],
                        [1, 1, -1, 1, -1, 1, -1, -1],
                    ],
                    [
                        [1, 1, -1, -1, 1, -1, -1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, -1, -1, -1, 1, -1],
                    ],
                    [
                        [1, 1, -1, 1, -1, 1, -1, -1],
                        [1, 1, 1, -1, -1, -1, 1, -1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                    ],
                ]
            ),
        ),
    ],
)
def test_get_sign_tensor(n: int, expected: NDArray) -> None:
    """Test building the sign tensor for n-point correlation functions."""
    sign_tensor = get_sign_tensor(expected_signs, n)

    assert np.allclose(sign_tensor, expected)


@pytest.mark.parametrize(
    ("n", "samples", "expected_mean", "expected_err"),
    [
        (
            1,
            samples_L3,
            corr_L3["sz"],
            corr_L3["sz_err"],
        ),
        (
            2,
            samples_L3,
            corr_L3["szsz"],
            corr_L3["szsz_err"],
        ),
        (
            1,
            samples_L5,
            corr_L5["sz"],
            corr_L5["sz_err"],
        ),
        (
            2,
            samples_L5,
            corr_L5["szsz"],
            corr_L5["szsz_err"],
        ),
    ],
)
def test_samples_corr_npt(
    n: int,
    samples: BitstringMap,
    expected_mean: NDArray,
    expected_err: NDArray,
) -> None:
    """Test computation of the n-point correlation functions and deviations."""

    signs, counts = samples_map_to_arrays(samples)
    mean, std = samples_corr_npt(signs, counts, n=n)

    assert np.allclose(mean, expected_mean, atol=ATOL)
    assert np.allclose(std, expected_err, atol=ATOL)


@pytest.mark.parametrize(
    ("expected_c", "expected_err"),
    [
        (
            np.array(
                [
                    [0.9704, 0.3049, 0.3109],
                    [0.3049, 0.9694, 0.3094],
                    [0.3109, 0.3094, 0.9694],
                ]
            ),
            np.array(
                [
                    [0.0076, 0.0287, 0.0287],
                    [0.0287, 0.0077, 0.0287],
                    [0.0287, 0.0287, 0.0077],
                ]
            ),
        ),
    ],
)
def test_compute_connected_2pt_corr(
    expected_c: NDArray,
    expected_err: NDArray,
) -> None:
    """Test the computation of connected 2-point correlation functions."""
    corr_1pt, corr_1pt_err = samples_corr_npt(expected_signs, expected_counts, n=1)
    corr_2pt, corr_2pt_err = samples_corr_npt(expected_signs, expected_counts, n=2)

    corr_2pt_c, corr_2pt_c_err = compute_connected_2pt_corr(
        corr_1pt, corr_2pt, corr_1pt_err, corr_2pt_err
    )

    assert np.allclose(corr_2pt_c, expected_c, atol=ATOL)
    assert np.allclose(corr_2pt_c_err, expected_err, atol=ATOL)

    corr_2pt_c = compute_connected_2pt_corr(corr_1pt, corr_2pt)
    assert np.allclose(corr_2pt_c, expected_c, atol=ATOL)


@pytest.mark.parametrize(
    "corr, expected",
    [
        (corr_L3["sz"], -0.174),
    ],
)
def test_average_corr_1pt(corr: NDArray, expected: float) -> None:
    """Test averaging of the 1-point correlation functions."""

    assert np.allclose(average_corr_1pt(corr), expected)


@pytest.mark.parametrize(
    "corr, expected",
    [
        (corr_L3["szsz"], np.array([1.0, 0.3387, 0.3387])),
    ],
)
def test_average_corr_2pt(corr: NDArray, expected: NDArray) -> None:
    """Test averaging of the 2-point correlation functions."""

    assert np.allclose(average_corr_2pt(corr), expected, atol=ATOL)
