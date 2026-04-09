r"""
Map the Rydberg Hamiltonian to the critical Ising Hamiltonian.

This module translates the values of the parameters between the Rydberg effective
Hamiltonian

$$
H_{\text{Rydberg}}
    \sim \sum_{i < j} \frac{C_6}{\vec r_{ij}^6} \, n_i n_j
        + \frac{\hbar \Omega(t)}{2} \, \sum_i \sigma^x_i
        - \hbar \delta(t) \, \sum_i n_i,
$$

where $n_i = (\sigma^z_i + 1) / 2$,and the critical Ising Hamiltonian

$$
H_{\text{Ising}}
    = J \sum_{\braket{i,j}} \, \sigma^z_i \sigma^z_j
        - J g \, \sum_i \sigma^x_i
$$

In particular, it provides the values
of:
- $\delta$ (detuning) to cancel the longitudinal field induced by the $n_i n_j$ term;
- $\Omega$ (amplitude) to reach the critical point;
- $a$ (interatomic distance) in terms of the Ising coupling $J$.
"""


class RydbergMapping:
    """
    Map the Rydberg Hamiltonian to the critical Ising Hamiltonian.
    """

    def __init__(self, L: int, J: float):
        """
        Initialize the Rydberg mapping.

        Args:
            L: Number of qubits.
            J: Ising coupling.

        """

        self.J = J
        self.L = L

    @property
    def delta(self) -> float:
        """
        Compute the detuning needed to cancel the longitudinal field.
        """

        return 0.0

    @property
    def Omega(self) -> float:
        """
        Compute the amplitude needed to reach the critical point.
        """

        return 0.0

    @property
    def a(self) -> float:
        """
        Compute the interatomic distance in terms of the Ising coupling.
        """

        return 0.0

    @staticmethod
    def compute_delta(L: int, a: float) -> float:
        """
        Compute the detuning needed to cancel the longitudinal field.
        """

        return 0.0

    @staticmethod
    def compute_Omega(L: int, a: float) -> float:
        """
        Compute the amplitude needed to reach the critical point.
        """

        return 0.0

    @staticmethod
    def compute_J(a: float) -> float:
        """
        Compute the Ising coupling in terms of the interatomic distance.
        """

        return 0.0

    @staticmethod
    def compute_hz(L: int, a: float) -> float:
        """
        Compute the longitudinal field.
        """

        return 0.0
