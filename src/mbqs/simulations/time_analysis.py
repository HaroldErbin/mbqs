"""
Signal processing to compute the surge time.
"""

import numpy as np
from scipy.signal import find_peaks


def get_first_peak_idx(y: np.ndarray) -> int:
    """
    Get the index of the first peak in the signal.

    Args:
        y: The signal data.

    Returns:
        The index of the first peak. If no peak is found, returns the index of
        the global maximum.

    """

    peaks, _ = find_peaks(y)

    if peaks.size > 0:
        return int(peaks[0])

    return int(np.argmax(y))
