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

from mbqs.simulations import ising_qutip
from mbqs.simulations.lieb_robinson import compute_lieb_robinson_time
from mbqs.simulations.state import State


class Duration:
    """
    Compute the protocol duration (surge time).
    """

    def __init__(self, L: int, J: float, state=State.down):
        """
        Initialize the duration.

        Args:
            L: Number of qubits.
            J: Ising coupling.
            state: Initial state.

        """

        self.L = L
        self.J = J
        self.state = state

    def surge_time(self, method: str = "qutip") -> float:
        """
        Compute the surge time.
        """

        return self.compute_surge_time(self.L, self.J, self.state, method)

    @property
    def lieb_robinson_time(self) -> float:
        """
        Approximation of the surge time using the Lieb-Robinson velocity.
        """

        return self.compute_surge_time(
            self.L, self.J, self.state, method="lieb_robinson"
        )

    @property
    def qutip_surge_time(self) -> float:
        """
        Surge time using qutip simulations.
        """

        return self.compute_surge_time(self.L, self.J, self.state, method="qutip")

    @property
    def fermions_surge_time(self) -> float:
        """
        Surge time using free fermions.
        """

        return self.compute_surge_time(self.L, self.J, self.state, method="fermions")

    @staticmethod
    def compute_surge_time(L: int, J: float, state=State.down, method="qutip") -> float:
        """
        Compute the surge time.
        """

        match method:
            case "fermions":
                raise NotImplementedError
            case "qutip":
                surge_time = ising_qutip.get_surge_time(L, J, state)
            case "lieb_robinson":
                surge_time = compute_lieb_robinson_time(L, J)
            case _:
                raise ValueError(f"Unknown method to compute surge time: {method}")

        return round(surge_time, 3)
