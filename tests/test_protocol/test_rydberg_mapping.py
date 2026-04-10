import numpy as np
import pytest

from mbqs.protocol.rydberg_mapping import RydbergMapping

# J for a = 7.5
J_75 = 1.2160498936625515


@pytest.mark.parametrize(
    ("L", "J", "a", "level"),
    [
        (2, 1.0, None, 60),
        (2, None, 5.0, 60),
    ],
)
def test_rydberg_mapping_init(L, J, a, level):
    mapping = RydbergMapping(L, J=J, a=a, level=level)

    assert mapping.L == L
    assert mapping.level == level

    if J is not None:
        assert mapping.J == J
    if a is not None:
        assert mapping.a == a


@pytest.mark.parametrize(
    ("L", "J", "a"),
    [
        (2, None, None),
        (2, 1.0, 1.0),
    ],
)
def test_rydberg_mapping_errors(L, J, a):
    with pytest.raises(ValueError):
        RydbergMapping(L, J=J, a=a)


def test_rydberg_mapping_properties_a():
    mapping = RydbergMapping(L=6, J=J_75, level=60)
    assert np.isclose(mapping.a, 7.5)


def test_rydberg_mapping_properties_j():
    mapping = RydbergMapping(L=6, a=7.5, level=60)
    assert np.isclose(mapping.J, 1.2160498936625515)


def test_rydberg_mapping_properties_omega():
    mapping = RydbergMapping(L=6, J=J_75, level=60)
    assert np.isclose(mapping.Omega, 2.432099787325103)


def test_rydberg_mapping_properties_delta():
    mapping = RydbergMapping(L=6, J=J_75, level=60)
    assert np.isclose(mapping.delta, 5.082356725289227)


def test_rydberg_mapping_summary():
    mapping = RydbergMapping(L=6, J=J_75, level=60)
    summary = mapping.summary

    assert summary.keys() == {"L", "J", "a", "Omega", "delta"}

    assert summary["L"] == 6
    assert np.isclose(summary["J"], J_75)
    assert np.isclose(summary["a"], 7.5)
    assert np.isclose(summary["Omega"], 2.432099787325103)
    assert np.isclose(summary["delta"], 5.082356725289227)


@pytest.mark.parametrize(
    ("J", "level", "expected_a"),
    [
        (J_75, 60, 7.5),
        (0.0, 60, np.inf),
    ],
)
def test_compute_a(J, level, expected_a):
    assert np.isclose(RydbergMapping.compute_a(J, level), expected_a)


@pytest.mark.parametrize(
    ("a", "level", "expected_J"),
    [
        (7.5, 60, 1.2160498936625515),
        (0.0, 60, np.inf),
    ],
)
def test_compute_J(a, level, expected_J):
    assert np.isclose(RydbergMapping.compute_J(a, level), expected_J)


@pytest.mark.parametrize(
    ("J", "expected_omega"),
    [
        (1.0, 2.0),
        (J_75, 2.432099787325103),
    ],
)
def test_compute_omega(J, expected_omega):
    assert np.isclose(RydbergMapping.compute_Omega(J), expected_omega)


@pytest.mark.parametrize(
    ("L", "J", "level", "expected_delta"),
    [
        (6, J_75, 60, 5.082356725289227),
    ],
)
def test_compute_delta(L, J, level, expected_delta):
    assert np.isclose(RydbergMapping.compute_delta(L, J, level), expected_delta)


@pytest.mark.parametrize(
    ("L", "J", "level", "expected_hz"),
    [
        (6, J_75, 60, 2.089699095315064),
    ],
)
def test_compute_hz(L, J, level, expected_hz):
    assert np.isclose(RydbergMapping.compute_hz(L, J, level), expected_hz)
