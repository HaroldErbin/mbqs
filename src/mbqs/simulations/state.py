"""
Define the allowed states for the protocol.
"""

from enum import StrEnum


class State(StrEnum):
    """
    Define the allowed states for the protocol.
    """

    down = "down"
    plus = "plus"
