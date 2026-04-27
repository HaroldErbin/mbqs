import numpy as np
import pytest
from numpy.typing import NDArray

from mbqs.simulations.time_analysis import get_first_peak_time


def test_get_first_peak_time_basic():
    """
    Test basic peak detection without interpolation.
    """

    x = np.linspace(0, 10, 101)
    # peak at x = 5
    y = np.exp(-((x - 5) ** 2))

    peak_time = get_first_peak_time(x, y, interpolate=False)
    assert peak_time == pytest.approx(5.0)


def test_get_first_peak_time_coarse():
    """
    Test peak detection on coarse grid with polynomial interpolation.
    """

    # coarse grid, but true peak at 5.05
    x = np.array([4.4, 4.7, 5.0, 5.3, 5.6])
    y = np.exp(-((x - 5.05) ** 2))

    peak_time = get_first_peak_time(x, y, interpolate=True)

    # interpolation should make it closer to 5.05 than 5.0
    assert abs(peak_time - 5.05) < abs(peak_time - 5.0)
    assert peak_time == pytest.approx(5.05, abs=0.01)


def test_get_first_peak_time_noisy():
    """
    Test peak detection with noise using a window.
    """

    x = np.linspace(0, 10, 101)
    y = np.exp(-((x - 5) ** 2))

    # add small noise
    np.random.seed(42)
    y += 0.01 * np.random.randn(len(x))

    peak_time = get_first_peak_time(x, y, interpolate=True)

    # should be close to 5.0 despite noise
    assert peak_time == pytest.approx(5.0, abs=0.05)


@pytest.mark.parametrize(
    ("times", "values"),
    [
        # Case: len(times_window) < 3
        (np.array([0.0, 1.0]), np.array([0.0, 1.0])),
        # Case: c2 >= 0
        (np.array([0.0, 1.0, 2.0, 3.0, 4.0]), np.array([0.0, 1.0, 4.0, 9.0, 16.0])),
        # Case: interp_peak_time outside window
        (np.array([0.0, 1.0, 2.0, 3.0, 4.0]), np.array([0.0, 1.0, 2.0, 3.0, 4.1])),
    ],
)
def test_get_first_peak_time_edge_cases(times: NDArray, values: NDArray):
    """
    Test edge cases for peak detection.
    """

    peak_time_no_interp = get_first_peak_time(times, values, interpolate=False)
    peak_time_interp = get_first_peak_time(times, values, interpolate=True)

    # In these edge cases, interpolation should fallback to the discrete peak
    assert peak_time_interp == peak_time_no_interp
