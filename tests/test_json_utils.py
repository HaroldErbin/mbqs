import pytest

from mbqs.json_utils import json_decode_keys, json_encode_keys


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        # Simple dict
        ({"a": 1, 2: 3}, {"a": 1, 2: 3}),
        # Tuple keys
        ({(0, 1): "val"}, {"(0, 1)": "val"}),
        # Nested dicts
        ({"nested": {(1, 2): 3}}, {"nested": {"(1, 2)": 3}}),
        # Non-dict input
        ([1, 2, 3], [1, 2, 3]),
    ],
)
def test_json_encode_keys(data, expected):
    """
    Test recursive encoding of dict keys to strings.
    """

    assert json_encode_keys(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        # Integer keys
        ({"1": "a", "2": "b"}, {1: "a", 2: "b"}),
        # Float keys
        ({"1.5": "a", ".5": "b", "2.": "c"}, {1.5: "a", 0.5: "b", 2.0: "c"}),
        # Tuple keys
        ({"(0, 1)": "a"}, {(0, 1): "a"}),
        # Bitstring keys (length >= 2, only 0 and 1)
        ({"00": "val1", "11": "val2"}, {"00": "val1", "11": "val2"}),
        # Mixed keys (not all bitstrings)
        ({"00": "val1", "abc": "val2"}, {0: "val1", "abc": "val2"}),
        # Redundant quotes in strings
        ({"'quoted'": "val"}, {"quoted": "val"}),
        # Non-dict input
        ([1, 2, 3], [1, 2, 3]),
        # Nested dictionary decoding
        ({"outer": {"1": "inner"}}, {"outer": {1: "inner"}}),
        # Tuples containing quoted strings
        ({"('a', 'b')": 1}, {("a", "b"): 1}),
    ],
)
def test_json_decode_keys(data, expected):
    """
    Test recursive decoding of dict keys from strings.
    """

    assert json_decode_keys(data) == expected
