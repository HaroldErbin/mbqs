"""
Results using Lieb-Robinson velocity.
"""


def compute_lieb_robinson_time(L: int, J: float) -> float:
    """
    Approximation of the surge time using the Lieb-Robinson velocity.
    """

    velocity = 2 * J
    distance = L / 2

    return distance / velocity
