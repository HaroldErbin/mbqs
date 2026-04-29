import numpy as np
import pytest

from mbqs.simulations import ising_tabulated
from mbqs.simulations.state import State


@pytest.mark.parametrize(
    ("L", "state", "J", "expected"),
    [
        (2, State.plus, 1.0, 0.555),
        (5, State.plus, 1.0, 1.402548),
        (2, State.down, 1.0, 0.7850000000000001),
        (5, State.down, 1.0, 1.501433),
        (10, State.plus, 1.0, 2.742819),
        (10, State.down, 1.0, 2.704268),
        (2, State.plus, 2.0, 0.2775),
        (2, State.down, 0.5, 1.5700000000000002),
    ],
)
def test_get_surge_time(L: int, state: State, J: float, expected: float) -> None:
    """
    Test get_surge_time function with tabulated data.
    """

    res = ising_tabulated.get_surge_time(L=L, state=state, J=J)
    assert res == expected


@pytest.mark.parametrize(
    ("L", "state", "J"),
    [
        (2, State.plus, 1.0),
        (2, State.down, 1.0),
        (5, State.plus, 1.0),
        (5, State.down, 1.0),
    ],
)
def test_get_surge_time_with_unused_params(L: int, state: State, J: float) -> None:
    """
    Test that dt and interpolate parameters don't affect the result.
    """

    res1 = ising_tabulated.get_surge_time(
        L=L, state=state, J=J, dt=0.001, interpolate=False
    )
    res2 = ising_tabulated.get_surge_time(
        L=L, state=state, J=J, dt=0.01, interpolate=True
    )
    assert res1 == res2


@pytest.mark.parametrize(
    ("L", "state", "expected_keys"),
    [
        (2, State.plus, ["sz", "szsz", "szsz_c"]),
        (5, State.plus, ["sz", "szsz", "szsz_c"]),
        (2, State.down, ["sz", "szsz", "szsz_c"]),
        (5, State.down, ["sz", "szsz", "szsz_c"]),
    ],
)
def test_get_correlations_keys(L: int, state: State, expected_keys: list[str]) -> None:
    """
    Test that get_correlations returns the expected keys.
    """

    res = ising_tabulated.get_correlations(L=L, state=state)
    assert set(res.keys()) == set(expected_keys)


@pytest.mark.parametrize(
    ("L", "state", "expected_sz"),
    [
        (2, State.plus, 0.0),
        (3, State.plus, 0.0),
        (2, State.down, -0.5626401165584822),
        (3, State.down, -0.4008284156853297),
    ],
)
def test_get_correlations_sz_value(L: int, state: State, expected_sz: float) -> None:
    """
    Test that get_correlations returns the expected sz value.
    """

    res = ising_tabulated.get_correlations(L=L, state=state)
    assert np.isclose(res["sz"], expected_sz)


@pytest.mark.parametrize(
    ("L", "state", "expected_pair", "expected_value"),
    [
        (2, State.plus, (0, 1), 0.9999989628882864),
        (3, State.plus, (0, 1), 0.999999485731268),
        (2, State.down, (0, 1), 0.6828937219882337),
        (3, State.down, (0, 1), 0.5740313268036638),
    ],
)
def test_get_correlations_szsz_value(
    L: int, state: State, expected_pair: str, expected_value: float
) -> None:
    """
    Test that get_correlations returns the expected szsz correlation value.
    """

    res = ising_tabulated.get_correlations(L=L, state=state)
    assert res["szsz"][expected_pair] == expected_value
