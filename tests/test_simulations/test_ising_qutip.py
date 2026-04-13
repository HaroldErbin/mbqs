import numpy as np
import pytest
import qutip

from mbqs.simulations import ising_qutip
from mbqs.simulations.state import State

# Constant for surge time testing
J_75 = 1.2160498936625515


def test_sx() -> None:
    """
    Test sx matrix creation for L=2.
    """

    L = 2
    sx0 = ising_qutip.sx(0, L)
    sx1 = ising_qutip.sx(1, L)

    expected0 = qutip.tensor(qutip.sigmax(), qutip.qeye(2))
    expected1 = qutip.tensor(qutip.qeye(2), qutip.sigmax())

    assert sx0 == expected0
    assert sx1 == expected1


def test_sz() -> None:
    """
    Test sz matrix creation for L=2.
    """

    L = 2
    sz0 = ising_qutip.sz(0, L)
    sz1 = ising_qutip.sz(1, L)

    expected0 = qutip.tensor(qutip.sigmaz(), qutip.qeye(2))
    expected1 = qutip.tensor(qutip.qeye(2), qutip.sigmaz())

    assert sz0 == expected0
    assert sz1 == expected1


@pytest.mark.parametrize("antipodal_only", [False, True])
def test_observables(antipodal_only: bool) -> None:
    """
    Test observables dictionary creation for L=5.
    """

    L = 5
    ops = ising_qutip.observables(L, antipodal_only=antipodal_only)

    sz0 = ising_qutip.sz(0, L)
    antipodal_idx = 2

    assert "sz" in ops
    assert ops["sz"] == sz0

    if antipodal_only is True:
        assert len(ops) == 2
        assert "szsz" in ops
        assert ops["szsz"] == sz0 @ ising_qutip.sz(antipodal_idx, L)
    else:
        print(ops.keys())
        assert len(ops) == 3
        for i in range(1, antipodal_idx + 1):
            assert f"szsz_{i}" in ops
            assert ops[f"szsz_{i}"] == sz0 @ ising_qutip.sz(i, L)


@pytest.mark.parametrize(
    "L, expected",
    [
        (3, 0.831),
        (6, 1.4),
    ],
)
def test_get_surge_time(L: int, expected: float) -> None:
    """
    Test get_surge_time function for L=3 and L=6.
    """

    res = ising_qutip.get_surge_time(L, J_75, State.down)
    assert np.isclose(res, expected, atol=1e-3)
