# MBQS: Many-Body Quantum Score – A scalable benchmark for digital and analog quantum processors

This packages provides a set of tools to compute the Many-Body Quantum Score (MBQS), which is designed to benchmark the performance of quantum processors in simulating many-body quantum systems [arXiv:[2601.03461](https://arxiv.org/abs/2601.03461)]. The score is obtained by comparing a given metric, called $P_2(L)$, with a threshold $\epsilon$.

The MBQS metric is parametrized by an initial state $\psi$ and computed according to the following protocol:

1.  Setup a spin chain with $L$ spin-$\frac{1}{2}$ equally spaced on a $1d$ ring.
2.  Initialize the register with the state $\ket{\psi}$.
3.  Evolve the system (quench) with the Ising Hamiltonian at the critical point $g = 1$ for a duration $t_*(L)$ (“surge time”).
4.  Perform measurements $\{ \sigma^z_i \}$ and compute the connected 2-point functions:

    $$
    g^{(2)}_\ell(t)
        := \Braket{\sigma^z_1 \sigma^z_\ell}_c
        := \Braket{\sigma^z_1 \sigma^z_\ell} - \Braket{\sigma^z_1} \Braket{\sigma^z_\ell}.
    $$

5.  Compute the metric (average relative error with respect to the theoretical values in Ising model):

    $$
    P_2(L)
        := \frac{1}{\lfloor L/2 \rfloor - 1} \sum_{\ell = 2}^{\lfloor L/2 \rfloor}
            \left |\frac{g^{(2) \text{exp}}_\ell(t_*) - g^{(2) \text{th}}_\ell(t_*)}{g^{(2) \text{th}}_\ell(t_*)}\right |.
    $$

The MBQS score S with the initial state $\psi$ corresponds to the largest problem size $L$ reached before failing the test with a threshold $\epsilon$, but excluding system sizes below some cut-off:

$$
S
    = L
\quad
\Longrightarrow
\quad
\forall L' \le L:
    \quad
    P_2(L') \le \epsilon.
$$

In this package, we provide the evaluation for the folloling initial states:

- $\ket{+ \cdots +}$
- $\ket{\downarrow \cdots \downarrow}$
