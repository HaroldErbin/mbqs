"""
Simulations for the protocol using the Ising Hamiltonian.
"""

import numpy as np
import qutip
from qutip import Qobj, basis, sesolve, tensor

from mbqs.simulations.time_analysis import get_first_peak_time

from .lattice import get_antipodal_idx
from .lieb_robinson import compute_lieb_robinson_time
from .state import State, StateType


def sx(j: int, L: int) -> Qobj:
    """
    Pauli matrix acting on spin j along x.
    """

    prod = [qutip.qeye(2) for _ in range(L)]
    prod[j] = qutip.sigmax()
    return qutip.tensor(*prod)


def sz(j: int, L: int) -> Qobj:
    """
    Pauli matrix acting on spin j along z.
    """

    prod = [qutip.qeye(2) for _ in range(L)]
    prod[j] = qutip.sigmaz()
    return qutip.tensor(*prod)


def observables(L: int, antipodal_only: bool = False) -> dict[str, Qobj]:
    """
    List of observables to compute.
    """

    corr_1pt = sz(0, L)
    antipodal_idx = get_antipodal_idx(L)

    if antipodal_only is True:
        return {"sz": corr_1pt, "szsz": corr_1pt @ sz(antipodal_idx, L)}

    return {
        "sz": corr_1pt,
        **{f"szsz_{j}": corr_1pt @ sz(j, L) for j in range(1, antipodal_idx + 1)},
    }


def ising_hamiltonian(J, L):
    """
    Ising Hamiltonian at the critical point.
    """

    H = (
        J * sum(sz(i, L) @ sz(i + 1, L) for i in range(L - 1))
        + J * sum(sx(i, L) for i in range(L))
        + J * sz(0, L) * sz(L - 1, L)
    )

    return H


def state_down(L):
    """
    Definition of the down state.

    Eigenstate of sigma_z with eigenvalue -1.
    """

    return tensor(basis(2, 1) for _ in range(L))  # type: ignore


def state_plus(L):
    """
    Definition of the plus state.

    Eigenstate of sigma_x with eigenvalue 1.
    """

    state = tensor(basis(2, 0) + basis(2, 1) for _ in range(L))  # type: ignore
    return state / state.norm()


def select_state(L: int, state: StateType) -> Qobj:
    """
    Select the initial state.
    """

    try:
        state = State(state)
    except ValueError as e:
        raise ValueError(f"Cannot create state {state}.") from e

    if state == State.plus:
        return state_plus(L)

    return state_down(L)


def make_quench(
    *,
    J: float = 1.0,
    state: StateType = State.down,
    L: int,
    duration: float,
    dt: float = 0.001,
    antipodal_only: bool = False,
):
    """
    Perform a quench for the Ising Hamiltonian.
    """

    psi = select_state(L, state)
    H = ising_hamiltonian(J, L)
    ops = observables(L, antipodal_only)

    if antipodal_only is True:
        # compute observable only in a window around the approximated surge time
        if L <= 5:
            factor = 0.3
        else:
            factor = 0.1

        window = 2 * factor * duration

        times = np.linspace(duration, duration + window, int(window / dt) + 1)
        times = np.insert(times, 0, 0.0)
    else:
        # compute observable only at the surge time
        times = [0.0, duration]

    results = sesolve(H, psi, times, e_ops=ops)

    obs = {key: np.array(values) for key, values in results.e_data.items()}

    obs.update(
        {
            key.replace("szsz", "szsz_c"): (
                np.array(results.e_data[key]) - np.array(results.e_data["sz"]) ** 2
            )
            for key in ops.keys()
            if key.startswith("szsz")
        }
    )

    return times, obs


def get_surge_time(
    *,
    L: int,
    J: float = 1.0,
    state: StateType = State.down,
    dt: float = 0.001,
    interpolate=True,
):
    """
    Compute the surge time for the Ising Hamiltonian.
    """

    duration = compute_lieb_robinson_time(L, J)

    times, obs = make_quench(
        J=J, state=state, L=L, duration=duration, dt=dt, antipodal_only=True
    )

    if L <= 3 and state == State.down:
        # szsz_c has a plateau for L = 3, so define peak time using 1-point function
        surge_time = get_first_peak_time(times, obs["sz"], interpolate=True)
    else:
        surge_time = get_first_peak_time(times, obs["szsz_c"], interpolate=True)

    return surge_time
