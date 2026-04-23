import numpy as np
import pytest

from mbqs.correlations.surge_correlations import SurgeCorrelations
from mbqs.simulations.state import State


@pytest.mark.parametrize(
    ("J", "state", "L", "method"),
    [
        (1.0, State.down, 2, "qutip"),
        (1.2, "plus", 3, "qutip"),
    ],
)
def test_surge_correlations_init(J, state, L, method) -> None:
    """
    Test SurgeCorrelations initialization and correlations computation.
    """

    sc = SurgeCorrelations(J=J, state=state, L=L, method=method)

    assert sc.J == J
    assert sc.state == state
    assert sc.L == L
    assert sc.method == method

    # surge_time property
    st = sc.surge_time
    assert isinstance(st, float)
    assert st >= 0

    # correlations should be a dict containing sz and szsz_c
    assert isinstance(sc.correlations, dict)
    assert "sz" in sc.correlations
    assert "szsz_c" in sc.correlations
    assert isinstance(sc.correlations["szsz_c"], dict)
    assert len(sc.correlations["szsz_c"]) > 0

    for k, v in sc.correlations["szsz_c"].items():
        assert isinstance(k, tuple)
        assert len(k) == 2
        assert isinstance(v, (float, np.float64))


def test_surge_correlations_default() -> None:
    """
    Test SurgeCorrelations with default parameters.
    """

    sc = SurgeCorrelations(L=2)
    assert sc.J == 1.0
    assert sc.state == State.down
    assert sc.method == "qutip"
