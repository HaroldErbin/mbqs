import pytest

from mbqs.correlations.utils import convert_2pt_dict


@pytest.mark.parametrize(
    ("corr", "expected"),
    [
        (
            {"sz": -0.1, "szsz_1": 0.2, "szsz_2": 0.3},
            {"sz": -0.1, "szsz": {(0, 1): 0.2, (0, 2): 0.3}},
        ),
        (
            {"sz_err": 0.01, "szsz_1_err": 0.02},
            {"sz_err": 0.01, "szsz_err": {(0, 1): 0.02}},
        ),
    ],
)
def test_convert_2pt_dict(corr: dict, expected: dict) -> None:
    """
    Test the conversion of the 2-point correlation dictionary.
    """

    assert convert_2pt_dict(corr) == expected
