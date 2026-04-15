"""
Compute the experimental correlation functions from bitstrings.
"""

from collections.abc import Mapping, Sequence
from typing import overload

import numpy as np
from numpy.typing import NDArray

from mbqs.types import BitstringMap


class SampleCorrelations:
    """
    Compute the experimental correlation functions from bitstrings.

    This object stores both the raw 1-point, 2-point and connected 2-point correlation
    functions and their errors as attributes. It also defines a dictionary of the
    correlation functions with keys "sz", "sz_err", "szsz_i" and "szsz_i_err" which
    contains average (using translation symmetry) of the previous quantities.
    """

    def __init__(self, samples: BitstringMap):
        """
        Initialize the correlations object.

        Args:
            samples: Counts of bitsrings which have been measured.

        """

        self.samples = samples

        signs, values = samples_map_to_arrays(self.samples)

        self.corr_1pt, self.corr_1pt_err = samples_corr_npt(signs, values, n=1)
        self.corr_2pt, self.corr_2pt_err = samples_corr_npt(signs, values, n=2)

        self.corr_2pt_c, self.corr_2pt_c_err = compute_connected_2pt_corr(
            self.corr_1pt, self.corr_2pt, self.corr_1pt_err, self.corr_2pt_err
        )

        self.correlations = {
            "sz": average_corr_1pt(self.corr_1pt),
            "sz_err": average_corr_1pt(self.corr_1pt_err),
        }

        avg_2pt = average_corr_2pt(self.corr_2pt)
        avg_2pt_err = average_corr_2pt(self.corr_2pt_err)

        self.correlations.update(
            {f"szsz_{i}": avg_2pt[i] for i in range(1, len(avg_2pt))}
        )
        self.correlations.update(
            {f"szsz_{i}_err": avg_2pt_err[i] for i in range(1, len(avg_2pt))}
        )


def bits_list_to_sign_array(bits_list: Sequence[str]) -> NDArray[np.integer]:
    """
    Convert a list of bitstrings to a sign array.
    """

    L = len(next(iter(bits_list)))

    # shape: (L, n_states)
    bits = np.c_[[np.fromiter(k, dtype=np.int8, count=L) for k in bits_list]].T

    return (-1) ** (bits + 1)


def samples_map_to_arrays(samples: Mapping):
    """
    Convert dict of bitstrings with counts to an array of signs and counts.
    """

    bits_list = list(samples.keys())

    # shape: (L, len(samples))
    signs = bits_list_to_sign_array(bits_list)

    # shape: (len(samples),)
    counts = np.array(list(samples.values()))

    return signs, counts


def get_sign_tensor(signs, n):
    """
    Build the sign tensor used to compute n-point correlation functions.
    """

    args = []

    for i in range(n):
        args.append(signs)
        args.append([i, n])

    return np.einsum(*args, list(range(n + 1)), optimize=True)


def samples_corr_npt(signs, counts, *, n):
    r"""
    Compute the n-point correlation functions and their deviations.

    The correlation functions are evaluated as the average over the samples:

    ..math::

        \bar x
            = \frac{1}{N} \, \sum_{i=1}^N N_i (x_i - \bar x)
            = \sum_{i=1}^N p_i (x_i - \bar x)

    where :math:`x_i` correspond to the observables built from the bitsrings.

    `std` corresponds to the standard error (standard deviation of the mean) as:

    ..math::

        \sigma_{\bar x}
            = \frac{\sigma_x}{\sqrt{N}}.

    where $\sigma_x$ is the standard deviation of the samples:

    ..math::

        \sigma_{x}^2
            = \frac{1}{N - 1} \, \sum_{i=1}^N N_i (x_i - \bar x)^2
            = \frac{N}{N - 1} \sum_{i=1}^N p_i (x_i - \bar x)^2

    If we were not using the unbiased estimation of the standard deviation, we could compute
    the mean and standard deviation using only the probabilities instead of the values. The bias
    could be corrected when reporting error bars by diving with :math:`\sqrt{N - 1}` instead of
    :math:`\sqrt{N}`. However, the advantages of working with the values is that all intermediate
    steps are performed with integers, which leads to more accurate results than floats.
    """

    N_samples = np.sum(counts)
    corr_tensor = get_sign_tensor(signs, n)

    mean = np.sum(counts * corr_tensor, axis=-1, keepdims=True) / N_samples
    std = np.sqrt(np.sum(counts * (corr_tensor - mean) ** 2, axis=-1) / (N_samples - 1))

    return np.squeeze(mean), std / np.sqrt(N_samples)


@overload
def compute_connected_2pt_corr(
    corr_1pt: NDArray,
    corr_2pt: NDArray,
    corr_1pt_err: None = None,
    corr_2pt_err: None = None,
) -> NDArray: ...


@overload
def compute_connected_2pt_corr(
    corr_1pt: NDArray,
    corr_2pt: NDArray,
    corr_1pt_err: NDArray,
    corr_2pt_err: NDArray,
) -> tuple[NDArray, NDArray]: ...


def compute_connected_2pt_corr(
    corr_1pt,
    corr_2pt,
    corr_1pt_err=None,
    corr_2pt_err=None,
):
    """
    Compute the connected 2-point correlation functions.
    """

    corr_2pt_c = corr_2pt - np.outer(corr_1pt, corr_1pt)

    if corr_1pt_err is not None and corr_2pt_err is not None:
        corr_2pt_c_err = (
            corr_2pt_err
            + np.abs(np.outer(corr_1pt, corr_1pt_err))
            + np.abs(np.outer(corr_1pt_err, corr_1pt))
        )

        return corr_2pt_c, corr_2pt_c_err

    return corr_2pt_c


def average_corr_1pt(corr):
    """
    Average the 1-point correlation functions.

    This uses translation invariance of the ring.
    """

    return np.mean(corr)


def average_corr_2pt(corr):
    """
    Average the 2-point correlation functions.

    This uses translation invariance of the ring.
    """

    rolled = np.c_[[np.roll(col, -i) for i, col in enumerate(corr.T)]].T
    return np.mean(rolled, axis=1)
