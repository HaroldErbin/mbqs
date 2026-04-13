"""
Tests for the MBQS protocol definition.
"""

import numpy as np

from mbqs.protocol.definition import MBQSProtocol
from mbqs.protocol.duration import Duration
from mbqs.simulations.state import State


def test_protocol_init():
    protocol = MBQSProtocol(state="down", L=6, J=1.0)

    assert protocol.state == State("down")
    assert protocol.L == 6
    assert protocol.J == 1.0


def test_protocol_corr_idx():
    protocol = MBQSProtocol(state="down", L=6, J=1.0)

    assert protocol.corr_idx == [(0, 1), (0, 2), (0, 3)]


def test_protocol_surge_time():
    protocol = MBQSProtocol(state="down", L=6, J=1.0)
    assert np.isclose(protocol.surge_time, Duration(L=6, J=1.0).surge_time())


def test_protocol_summary():
    """
    Test the summary of the MBQS protocol.
    """

    protocol = MBQSProtocol(state="down", L=6, J=1.0)
    summary = protocol.summary

    assert summary == {
        "state": "down",
        "L": 6,
        "J": 1.0,
        "time": protocol.surge_time,
        "corr_idx": [(0, 1), (0, 2), (0, 3)],
    }
