"""
Signal processing to compute the surge time.
"""

import numpy as np
from numpy.polynomial import polynomial as poly
from numpy.typing import NDArray
from scipy.signal import find_peaks


def get_first_peak_time(
    times: NDArray, values: NDArray, interpolate: bool = True
) -> float:
    """
    Get the time of the first peak in the signal.

    The precision of the peak is determined by the precision of the simulation time
    grid. In order to improve it, one can perform a polynomial interpolation of the
    signal around the peak.

    Args:
        times: The x-axis data.
        values: The signal data.
        interpolate: Whether to interpolate the signal to find the peak.

    Returns:
        The time of the first peak. If no peak is found, returns the time of
        the global maximum.

    """

    height = 0.1 * np.max(values) if values.size > 0 else None
    peaks, _ = find_peaks(values, height=height)

    if peaks.size > 0:
        idx = int(peaks[0])
    else:
        idx = int(np.argmax(values))

    peak_time = float(times[idx])

    if interpolate is False:
        return peak_time

    window_size = 9
    step = 2

    half_window = window_size // 2
    start = max(0, idx - step * half_window)
    end = min(len(times), idx + step * half_window + 1)

    times_window = times[start:end:step]
    values_window = values[start:end:step]

    if len(times_window) < 3:
        return peak_time

    coeffs = poly.polyfit(times_window, values_window, deg=2)
    _, c1, c2 = coeffs

    if c2 < 0:
        interp_peak_time = -c1 / (2 * c2)
        if times_window[0] <= interp_peak_time <= times_window[-1]:
            return float(interp_peak_time)

    return peak_time
