r"""
Compute the protocol duration (surge time).

The protocol duration is given by the surge time. It is defined as the time it takes
for the information to propagate to the antipodal site. It is also the approximate time
for which all connected 2-point correlation functions are maximum.

The surge time $t_*$ is computed by evolving the antipodal connected 2-point
correlation function using the free fermion formalism, and finding the time at which
it is maximum.

The surge time can be approximated using the Lieb-Robinson velocity
$v_{\text{LR}}$:

$$
t_* \approx \frac{L}{2 * v_{\text{LR}}}
$$

This can be used to provide a window where to restrict the time evolution for
efficiency.
"""


class Duration:
    """
    Compute the protocol duration (surge time).
    """

    def __init__(self, L: int, J: float):
        """
        Initialize the duration.

        Args:
            L: Number of qubits.
            J: Ising coupling.

        """

        self.L = L
        self.J = J

    @property
    def surge_time(self) -> float:
        """
        Compute the surge time.
        """

        return self.compute_surge_time(self.L, self.J)

    @property
    def lieb_robinson_time(self) -> float:
        """
        Approximation of the surge time using the Lieb-Robinson velocity.
        """

        return self.compute_lieb_robinson_time(self.L, self.J)

    @staticmethod
    def compute_surge_time(L: int, J: float) -> float:
        """
        Compute the surge time.
        """

        raise NotImplementedError

        return 0.0

    @staticmethod
    def compute_lieb_robinson_time(L: int, J: float) -> float:
        """
        Approximation of the surge time using the Lieb-Robinson velocity.
        """

        velocity = 2 * J
        distance = L / 2

        return distance / velocity
