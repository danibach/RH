# Bach-Derived Psi Function and RH Error Bound Route

## Bach Prime Indicator

Let Bach's divisor wave be:

```latex
B(n)=
\sum_{m=2}^{n-1}
\left(
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
\right).
```

For integer `n >= 2`, the inner roots-of-unity average is `1` when `m`
divides `n`, and `0` otherwise. Thus `B(n)` counts the proper divisors of
`n`, excluding `1` and `n`.

Therefore:

```latex
B(n)=0 \iff n \text{ is prime}.
```

Define the Bach prime indicator:

```latex
Q_B(n)=\operatorname{sinc}(B(n)).
```

Since `B(n)` is a nonnegative integer and:

```latex
\operatorname{sinc}(k)=0
\quad \text{for every integer } k\ne 0,
```

we get:

```latex
Q_B(n)=
\begin{cases}
1, & n \text{ prime},\\
0, & n \text{ composite}.
\end{cases}
```

## Bach-Derived Von Mangoldt Function

Using `Q_B`, define:

```latex
\Lambda_B(N)=
\sum_{\substack{k\ge 1\\ n^k=N}}
Q_B(n)\log n.
```

Since `Q_B(n)` selects only primes, this becomes:

```latex
\Lambda_B(N)=
\begin{cases}
\log p, & N=p^k \text{ for a prime } p \text{ and } k\ge 1,\\
0, & \text{otherwise}.
\end{cases}
```

Thus:

```latex
\Lambda_B(N)=\Lambda(N),
```

the classical von Mangoldt function.

## Bach-Derived Chebyshev Psi Function

Define:

```latex
\psi_B(x)=
\sum_{N\le x}\Lambda_B(N).
```

Equivalently:

```latex
\psi_B(x)=
\sum_{k=1}^{\lfloor \log_2 x\rfloor}
\sum_{2\le n\le x^{1/k}}
Q_B(n)\log n.
```

Since `Q_B` selects primes:

```latex
\psi_B(x)=
\sum_{p^k\le x}\log p
=
\psi(x).
```

## RH-Equivalent Target

The Riemann Hypothesis is equivalent to the error bound:

```latex
\psi(x)-x=O\left(x^{1/2}\log^2 x\right).
```

Because `psi_B(x)=psi(x)`, the same target becomes:

```latex
\boxed{
\psi_B(x)-x=O\left(x^{1/2}\log^2 x\right)
}
```

This is the Bach prime-zero wave route toward an RH-equivalent formulation.

The hard part is not proving that `psi_B(x)=psi(x)`, which follows from the
exact Bach prime indicator. The hard part is deriving the RH-scale error bound
from the internal wave/divisor structure of `B(n)`, without assuming RH.

For the fuller analytic route, including the Dirichlet transform,
Perron-inversion target, LCM wave-correlation expansion, and the precise
remaining obstruction, see:

```text
bach_chebyshev_psi_b_rh_route_deep_dive_source.md
```
