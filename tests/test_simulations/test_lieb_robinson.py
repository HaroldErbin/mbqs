import numpy as np
import pytest

from mbqs.simulations.lieb_robinson import compute_lieb_robinson_time

J_75 = 1.2160498936625515


@pytest.mark.parametrize(
    ("L", "J"),
    [
        (6, J_75),
        (7, J_75),
        (8, J_75),
    ],
)
def test_compute_lieb_robinson_time(L, J):
    assert np.isclose(compute_lieb_robinson_time(L, J), L / (4 * J))
