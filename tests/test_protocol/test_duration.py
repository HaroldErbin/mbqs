import numpy as np
import pytest

from mbqs.protocol.duration import Duration
from mbqs.simulations.state import State

# J for a = 7.5
J_75 = 1.2160498936625515
ATOL = 1e-3


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


def test_duration_properties_surge_time():
    duration = Duration(L=6, J=J_75)
    assert np.isclose(duration.surge_time(), 1.4, atol=ATOL)


def test_duration_properties_lieb_robinson_time():
    duration = Duration(L=6, J=J_75)
    assert np.isclose(duration.lieb_robinson_time, 6 / (4 * J_75), atol=ATOL)


def test_duration_properties_qutip_surge_time():
    duration = Duration(L=6, J=J_75)
    assert np.isclose(duration.qutip_surge_time, 1.4, atol=ATOL)


def test_compute_surge_time_invalid_method():
    with pytest.raises(ValueError, match="Unknown method"):
        Duration.compute_surge_time(L=3, J=J_75, method="invalid")


@pytest.mark.xfail(reason="Not implemented yet")
def test_duration_properties_fermions_surge_time():
    assert np.isclose(Duration(L=6, J=J_75).fermions_surge_time, 1.4, atol=ATOL)


@pytest.mark.parametrize(
    ("L", "J", "expected_surge_time"),
    [
        (3, J_75, 0.831),
        (4, J_75, 1.064),
        (5, J_75, 1.234),
        (6, J_75, 1.4),
        (7, J_75, 1.585),
        (8, J_75, 1.724),
    ],
)
def test_compute_surge_time_down(L, J, expected_surge_time):

    duration = Duration.compute_surge_time(L, J, state=State.down)
    assert np.isclose(duration, expected_surge_time, atol=ATOL)


@pytest.mark.parametrize(
    ("L", "J", "expected_surge_time"),
    [
        (3, J_75, 0.646),
        (4, J_75, 0.928),
        (5, J_75, 1.153),
        (6, J_75, 1.359),
        (7, J_75, 1.597),
        (8, J_75, 1.819),
    ],
)
def test_compute_surge_time_plus(L, J, expected_surge_time):

    duration = Duration.compute_surge_time(L, J, state=State.plus)
    assert np.isclose(duration, expected_surge_time, atol=ATOL)
