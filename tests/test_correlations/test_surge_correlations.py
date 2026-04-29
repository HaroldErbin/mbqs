import numpy as np
import pytest

from mbqs.correlations.surge_correlations import SurgeCorrelations
from mbqs.simulations.state import State

ATOL = 1e-3

# L = 5, down
correlations_expected = (
    {
        "sz": -0.2083918,
        "szsz": {(0, 1): 0.4828433, (0, 2): 0.4539823},
        "szsz_c": {(0, 1): 0.4394162, (0, 2): 0.4105552},
    },
)


@pytest.mark.parametrize(
    ("state", "L", "method"),
    [
        (State.down, 2, "qutip"),
        ("plus", 3, "qutip"),
        (State.down, 5, "tabulated"),
        (State.plus, 5, "tabulated"),
    ],
)
def test_surge_correlations_init(state, L, method) -> None:
    """
    Test SurgeCorrelations initialization and correlations computation.
    """

    sc = SurgeCorrelations(state=state, L=L, method=method)

    assert sc.state == state
    assert sc.L == L
    assert sc.method == method

    # correlations should be a dict containing sz and szsz_c
    assert isinstance(sc.correlations, dict)
    assert "sz" in sc.correlations
    assert "szsz_c" in sc.correlations
    assert isinstance(sc.correlations["szsz_c"], dict)

    for k, v in sc.correlations["szsz_c"].items():
        # make sure that tabulated data has been converted
        assert isinstance(k, tuple)
        assert len(k) == 2
        assert isinstance(v, (float, np.float64))


def test_surge_correlations_surge_time_property() -> None:

    sc = SurgeCorrelations(L=5)

    st = sc.surge_time_J
    assert np.isclose(st, 1.501433, atol=ATOL)


def test_surge_correlations_default() -> None:
    """
    Test SurgeCorrelations with default parameters.
    """

    sc = SurgeCorrelations(L=2)
    assert sc.state == State.down
    assert sc.method == "tabulated"


@pytest.mark.xfail(reason="Not implemented yet")
def test_fermions_correlations_property():
    sc = SurgeCorrelations(state=State.down, L=5, method="qutip")
    corr = sc.fermions_correlations
    assert isinstance(corr, dict)
    assert "szsz_c" in corr


def test_qutip_correlations_property():
    sc = SurgeCorrelations(state=State.down, L=5, method="tabulated")
    corr = sc.qutip_correlations
    assert isinstance(corr, dict)
    assert "szsz_c" in corr


def test_tabulated_correlations_property():
    sc = SurgeCorrelations(state=State.down, L=5, method="qutip")
    corr = sc.tabulated_correlations
    assert isinstance(corr, dict)
    assert "szsz_c" in corr


def test_compute_correlations_tabulated():
    corr = SurgeCorrelations.compute_correlations(
        L=5, state=State.down, method="tabulated"
    )
    assert isinstance(corr, dict)
    assert "szsz_c" in corr


def test_compute_correlations_qutip():
    corr = SurgeCorrelations.compute_correlations(
        L=5, state=State.down, surge_time=None, method="qutip"
    )
    assert isinstance(corr, dict)
    assert "szsz_c" in corr


def test_compute_correlations_invalid_method():
    with pytest.raises(ValueError, match="Unknown method"):
        SurgeCorrelations.compute_correlations(L=5, state=State.down, method="invalid")


@pytest.mark.xfail(reason="NotImplementedError raised when tabulated data not found")
def test_compute_correlations_tabulated_keyerror_fallback():
    """Test KeyError fallback to fermions raises NotImplementedError."""
    SurgeCorrelations.compute_correlations(L=1, state=State.down, method="tabulated")
