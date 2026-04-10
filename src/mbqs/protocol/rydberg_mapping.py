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

In particular, it provides the values of:

- $a$ (interatomic distance) in terms of the Ising coupling $J$;
- $J$ (Ising coupling) in terms of the interatomic distance $a$;
- $\delta$ (detuning) to cancel the longitudinal field induced by the $n_i n_j$ term;
- $\Omega$ (amplitude) to reach the critical point.
"""

from collections.abc import Mapping

import numpy as np
from pulser.devices.interaction_coefficients import c6_dict

from mbqs.protocol.lattice import ring_coordinates


class RydbergMapping:
    """
    Map the Rydberg Hamiltonian to the critical Ising Hamiltonian.
    """

    def __init__(
        self,
        /,
        L: int,
        J: float | None = None,
        a: float | None = None,
        level: int = 60,
    ):
        """
        Initialize the Rydberg mapping.

        Args:
            L: Number of qubits.
            J: Ising coupling.
            a: Interatomic distance.
            level: Rydberg level.

        """

        self.L = L
        self.level = level

        if J is None:
            if a is None:
                raise ValueError("Either J or a must be provided.")

            self._a = a
            self._J = self.compute_J(a, level)
        else:
            if a is not None:
                raise ValueError("Only one of J or a must be provided.")

            self._J = J
            self._a = self.compute_a(J, level)

    @property
    def a(self) -> float:
        """
        Get the interatomic distance.
        """

        return self._a

    @property
    def J(self) -> float:
        """
        Get the Ising coupling.
        """

        return self._J

    @property
    def Omega(self) -> float:
        """
        Get the amplitude needed to reach the critical point.
        """

        return self.compute_Omega(self.J)

    @property
    def delta(self) -> float:
        """
        Get the detuning needed to cancel the longitudinal field.
        """

        return self.compute_delta(self.L, self.J)

    @property
    def summary(self) -> Mapping:
        """
        Get a summary of the Rydberg mapping.

        Returns:
            Mapping: Summary of the Rydberg mapping.

        """

        return {
            "L": self.L,
            "J": self.J,
            "a": self.a,
            "Omega": self.Omega,
            "delta": self.delta,
        }

    @staticmethod
    def compute_J(a: float, level: int = 60) -> float:
        """
        Compute the Ising coupling in terms of the interatomic distance.
        """

        if a == 0:
            return np.inf

        # unit: rad µm^6 / µs
        C6: float = c6_dict[level]

        return C6 / (4 * a**6)

    @staticmethod
    def compute_a(J: float, level: int = 60) -> float:
        """
        Compute the interatomic distance in terms of the Ising coupling.
        """

        # the case J = 0 is special, so we set a = infinity
        if J == 0:
            return np.inf

        # unit: rad µm^6 / µs
        C6: float = c6_dict[level]

        return (C6 / (4 * J)) ** (1 / 6)

    @staticmethod
    def compute_Omega(J: float) -> float:
        """
        Compute the amplitude needed to reach the critical point.
        """

        # unit: rad / µs
        return 2 * J

    @staticmethod
    def compute_delta(L: int, J: float, level: int = 60) -> float:
        """
        Compute the detuning needed to cancel the longitudinal field.
        """

        # unit: rad / µs
        return 2 * J * RydbergMapping.compute_hz(L, J, level)

    @staticmethod
    def compute_hz(L: int, J: float, level: int = 60) -> float:
        """
        Compute the longitudinal field.
        """

        a = RydbergMapping.compute_a(J, level)
        coords = ring_coordinates(L, a)
        distances = np.linalg.norm(coords[0] - coords[1:], axis=1)

        return np.sum((distances[0] / distances) ** 6)
