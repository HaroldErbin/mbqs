import pytest

from mbqs.protocol.data_utils import find_data_type


@pytest.mark.parametrize(
    ("data", "expected_return"),
    [
        (
            {
                "J": 1.0,
            },
            (
                "protocol",
                {
                    "J": 1.0,
                },
            ),
        ),
        ({"01": 10}, "samples"),
        ({(0, 1): 0.5}, "correlations"),
        (
            {
                3: {"010": 10, "111": 10},
                4: {"0100": 10, "1111": 10},
            },
            "samples_sequence",
        ),
        (
            {
                3: {(0, 1): 0.5},
                4: {(0, 1): 0.3, (0, 2): 0.7},
            },
            "correlations_sequence",
        ),
        (
            {
                "J": 1.0,
                "samples": {"01": 10},
            },
            (
                "protocol_samples",
                {
                    "J": 1.0,
                },
            ),
        ),
        (
            {
                "J": 1.0,
                "correlations": {(0, 1): 0.5},
            },
            (
                "protocol_correlations",
                {
                    "J": 1.0,
                },
            ),
        ),
        (
            {
                "J": 1.0,
                "samples": {
                    3: {"010": 10, "111": 10},
                    4: {"0100": 10, "1111": 10},
                },
            },
            (
                "protocol_samples_sequence",
                {
                    "J": 1.0,
                },
            ),
        ),
        (
            {
                "J": 1.0,
                "correlations": {
                    3: {(0, 1): 0.5},
                    4: {(0, 1): 0.3, (0, 2): 0.7},
                },
            },
            (
                "protocol_correlations_sequence",
                {
                    "J": 1.0,
                },
            ),
        ),
    ],
)
def test_find_data_type(data, expected_return):
    assert find_data_type(data) == expected_return


@pytest.mark.parametrize(
    ("data", "expected_exception"),
    [
        ("test", TypeError),
        ({1: 1, "correlations": {(0, 1): 1}}, ValueError),
        ({1: 1, "samples": {(0, 1): 1}}, ValueError),
    ],
)
def test_find_data_type_raises_error(data, expected_exception):
    with pytest.raises(expected_exception):
        find_data_type(data)
