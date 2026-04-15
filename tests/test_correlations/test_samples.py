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

samples = Counter(
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

expected_signs = np.array(
    [
        [-1, 1, 1, -1, -1, 1, -1, 1],
        [-1, 1, -1, 1, -1, -1, 1, 1],
        [-1, 1, -1, -1, 1, 1, 1, -1],
    ]
)
expected_counts = np.array(list(samples.values()))

expected_corr_1pt = np.array([-0.172, -0.175, -0.175])
expected_corr_2pt = np.array(
    [[1.0, 0.335, 0.341], [0.335, 1.0, 0.34], [0.341, 0.34, 1.0]]
)


def test_sample_correlations_init() -> None:
    """
    Test initialization of the SampleCorrelations class.
    """

    samples_corr = SampleCorrelations(samples)

    assert np.allclose(samples_corr.corr_1pt, expected_corr_1pt, atol=1e-4)
    assert np.allclose(samples_corr.corr_2pt, expected_corr_2pt, atol=1e-4)

    assert hasattr(samples_corr, "corr_2pt_c")
    assert hasattr(samples_corr, "corr_2pt_c_err")

    correlations = samples_corr.correlations
    assert np.isclose(correlations["sz"], -0.174, atol=1e-4)
    assert np.isclose(correlations["sz_err"], 0.0220, atol=1e-4)
    assert np.isclose(correlations["szsz_1"], 0.3387, atol=1e-4)
    assert np.isclose(correlations["szsz_1_err"], 0.0210, atol=1e-4)
    assert np.isclose(correlations["szsz_2"], 0.3387, atol=1e-4)
    assert np.isclose(correlations["szsz_2_err"], 0.0210, atol=1e-4)


def test_bits_list_to_sign_array() -> None:
    """Test conversion of a list of bitstrings to a sign array."""
    bits_list = list(samples.keys())

    assert np.allclose(bits_list_to_sign_array(bits_list), expected_signs)


def test_samples_map_to_arrays() -> None:
    """Test conversion of bitstrings dictionary with counts to expected arrays."""
    signs, counts = samples_map_to_arrays(samples)

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
    ("n", "expected_mean", "expected_std"),
    [
        (
            1,
            expected_corr_1pt,
            np.array([0.0220, 0.0220, 0.0220]),
        ),
        (
            2,
            expected_corr_2pt,
            np.array(
                [
                    [0.0, 0.0211, 0.0210],
                    [0.0211, 0.0, 0.0210],
                    [0.0210, 0.0210, 0.0],
                ]
            ),
        ),
    ],
)
def test_samples_corr_npt(
    n: int,
    expected_mean: NDArray,
    expected_std: NDArray,
) -> None:
    """Test computation of the n-point correlation functions and deviations."""

    mean, std = samples_corr_npt(expected_signs, expected_counts, n=n)

    assert np.allclose(mean, expected_mean, atol=1e-4)
    assert np.allclose(std, expected_std, atol=1e-4)


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

    assert np.allclose(corr_2pt_c, expected_c, atol=1e-4)
    assert np.allclose(corr_2pt_c_err, expected_err, atol=1e-4)

    corr_2pt_c = compute_connected_2pt_corr(corr_1pt, corr_2pt)
    assert np.allclose(corr_2pt_c, expected_c, atol=1e-4)


@pytest.mark.parametrize(
    "corr, expected",
    [
        (expected_corr_1pt, -0.174),
    ],
)
def test_average_corr_1pt(corr: NDArray, expected: float) -> None:
    """Test averaging of the 1-point correlation functions."""

    assert np.allclose(average_corr_1pt(corr), expected)


@pytest.mark.parametrize(
    "corr, expected",
    [
        (expected_corr_2pt, np.array([1.0, 0.3387, 0.3387])),
    ],
)
def test_average_corr_2pt(corr: NDArray, expected: NDArray) -> None:
    """Test averaging of the 2-point correlation functions."""

    assert np.allclose(average_corr_2pt(corr), expected, atol=1e-4)
