import numpy as np
import pytest

from mbqs.scoring.metric import (
    compute_metric,
    metric_from_bitstring,
    metric_from_correlations,
)

ATOL = 1e-3

L = 5
J_75 = 1.2160498936625515

theory_correlations = {(0, 1): 0.43926304, (0, 2): 0.41055844}

samples = {
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

correlations = {
    "sz": -0.2135,
    "sz_err": 0.01168,
    "szsz": {(0, 1): 0.3746, (0, 2): 0.3498},
    "szsz_err": {(0, 1): 0.01106, (0, 2): 0.0112},
    "szsz_c": {(0, 1): 0.3291, (0, 2): 0.3042},
    "szsz_c_err": {(0, 1): 0.01608, (0, 2): 0.01618},
}


@pytest.mark.parametrize(
    ("L", "J", "correlations", "expected"),
    [
        (5, J_75, theory_correlations, 0.0),
        (5, J_75, correlations["szsz_c"], 0.255),
    ],
)
def test_compute_metric_qutip(L, J, correlations, expected):
    metric = metric_from_correlations(correlations, J=J, L=L, state="down")

    assert np.isclose(metric, expected, atol=ATOL)


@pytest.mark.parametrize(
    ("L", "J", "correlations", "correlations_errors", "expected_mean", "expected_err"),
    [
        (5, J_75, correlations["szsz_c"], correlations["szsz_c_err"], 0.255, 0.038),
        (5, J_75, theory_correlations, {(0, 1): 0.0, (0, 2): 0.0}, 0.0, 0.0),
    ],
)
def test_compute_metric_qutip_with_err(
    L, J, correlations, correlations_errors, expected_mean, expected_err
):
    metric, metric_err = metric_from_correlations(
        correlations, correlations_errors, J=J, L=L, state="down"
    )

    assert np.isclose(metric, expected_mean, atol=ATOL)
    assert np.isclose(metric_err, expected_err, atol=ATOL)


def test_metric_from_bitstring():
    metric, metric_err = metric_from_bitstring(samples, J=J_75, L=L, state="down")

    assert np.isclose(metric, 0.255, atol=ATOL)
    assert np.isclose(metric_err, 0.038, atol=ATOL)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (samples, 0.255),
        (correlations["szsz_c"], 0.255),
    ],
)
def test_compute_metric(data, expected):
    """
    Test compute_metric correctly dispatches based on input type.
    """

    res = compute_metric(data, J=J_75, L=L, state="down")

    if isinstance(res, tuple):
        res = res[0]
    assert np.isclose(res, expected, atol=ATOL)


def test_compute_metric_invalid_type():
    """Test compute_metric raises ValueError for invalid data key type."""
    with pytest.raises(ValueError, match="Invalid data type"):
        compute_metric({1: 2}, J=J_75, L=L, state="down")
