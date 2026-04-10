import numpy as np
import pytest

from mbqs.protocol.duration import Duration

# J for a = 7.5
J_75 = 1.2160498936625515


@pytest.mark.parametrize(
    ("L", "J"),
    [
        (2, 1.0),
    ],
)
def test_duration_init(L, J):
    duration = Duration(L, J)

    assert duration.L == L
    assert duration.J == J


@pytest.mark.xfail(raises=NotImplementedError)
def test_duration_properties_surge_time():
    duration = Duration(L=6, J=J_75)
    assert np.isclose(duration.surge_time, 1.4)


def test_duration_properties_lieb_robinson_time():
    duration = Duration(L=6, J=J_75)
    assert np.isclose(duration.lieb_robinson_time, 6 / (4 * J_75))


@pytest.mark.xfail(raises=NotImplementedError)
@pytest.mark.parametrize(
    ("L", "J", "expected_surge_time"),
    [
        (2, J_75, 0.0),
        (3, J_75, 1.292),
        (4, J_75, 1.064),
        (5, J_75, 1.235),
        (6, J_75, 1.4),
        (7, J_75, 1.585),
        (8, J_75, 1.724),
        (20, J_75, 4.495),
    ],
)
def test_compute_surge_time(L, J, expected_surge_time):
    assert np.isclose(Duration.compute_surge_time(L, J), expected_surge_time)


@pytest.mark.parametrize(
    ("L", "J"),
    [
        (6, J_75),
        (7, J_75),
        (8, J_75),
    ],
)
def test_compute_lieb_robinson_time(L, J):
    assert np.isclose(Duration.compute_lieb_robinson_time(L, J), L / (4 * J))
