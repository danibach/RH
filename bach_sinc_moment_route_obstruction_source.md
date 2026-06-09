# Sinc Moment Route: Finite Structure and Obstruction

## Setup

The Bach prime indicator is:

```latex
I_B(n)=\operatorname{sinc}(B(n)),
\qquad
B(n)=d(n)-2.
```

For integer `n >= 2`:

```latex
I_B(n)=
\begin{cases}
1, & n \text{ prime},\\
0, & n \text{ composite}.
\end{cases}
```

Its Dirichlet transform is:

```latex
P_B(s)=
\sum_{n=2}^{\infty}
\frac{I_B(n)}{n^s}.
```

The sinc expansion gives formally:

```latex
\operatorname{sinc}(x)=
\sum_{j=0}^{\infty}
\frac{(-1)^j\pi^{2j}x^{2j}}{(2j+1)!}.
```

So one might hope to write:

```latex
P_B(s)=
\sum_{j=0}^{\infty}
\frac{(-1)^j\pi^{2j}}{(2j+1)!}
M_{2j}(s),
```

where:

```latex
M_q(s)=
\sum_{n=2}^{\infty}
\frac{(d(n)-2)^q}{n^s}.
```

## Finite Moment Structure

For fixed `q`, define:

```latex
D_q(s)=
\sum_{n=1}^{\infty}
\frac{d(n)^q}{n^s}.
```

Since `d(n)^q` is multiplicative:

```latex
D_q(s)=
\prod_p
\sum_{a=0}^{\infty}
\frac{(a+1)^q}{p^{as}}.
```

Let:

```latex
F_q(x)=
\sum_{a=0}^{\infty}(a+1)^q x^a.
```

Then:

```latex
F_q(x)=1+2^q x+O_q(x^2).
```

Therefore:

```latex
D_q(s)=\zeta(s)^{2^q}H_q(s),
```

where:

```latex
H_q(s)=
\prod_p F_q(p^{-s})(1-p^{-s})^{2^q}
```

is analytic for:

```latex
\operatorname{Re}(s)>1/2.
```

Thus each fixed finite moment has no singularities in the open half-plane
`Re(s)>1/2`, except possibly at `s=1`.

Since:

```latex
(d(n)-2)^q=
\sum_{\ell=0}^{q}
\binom{q}{\ell}
(-2)^{q-\ell}d(n)^\ell,
```

each fixed `M_q(s)` is a finite linear combination of the `D_l(s)-1`.

Therefore every finite moment piece has the desired half-plane singularity
profile.

## The Obstruction

The formal sinc-moment expansion cannot be used as an ordinary convergent
series of transformed moments.

In fact, the terms fail to tend to zero even at `s=2`.

Let:

```latex
q=2j,
```

and:

```latex
M_q(2)=
\sum_{n=2}^{\infty}
\frac{(d(n)-2)^q}{n^2}.
```

Choose `N_L` to be the product of the first `L` primes. Then `N_L` is
squarefree and:

```latex
d(N_L)=2^L.
```

Hence:

```latex
M_q(2)\ge
\frac{(2^L-2)^q}{N_L^2}.
```

Using the standard growth:

```latex
\log N_L \sim L\log L,
```

choose, for example:

```latex
L=\left\lfloor 2^{q/4}\right\rfloor.
```

Then:

```latex
\log M_q(2)
\ge
c\,q\,2^{q/4}
```

for large `q` and some positive constant `c`.

The magnitude of the `j`-th sinc-moment term at `s=2` is at least:

```latex
\frac{\pi^q}{(q+1)!}M_q(2).
```

Its logarithm is bounded below by:

```latex
c\,q\,2^{q/4}
-O(q\log q),
```

which tends to `+infinity`.

Therefore the transformed sinc-power terms do not tend to zero. The ordinary
series:

```latex
\sum_{j=0}^{\infty}
\frac{(-1)^j\pi^{2j}}{(2j+1)!}
M_{2j}(s)
```

diverges even at `s=2`.

## Consequence

The finite moment pieces are analytically well-structured, but the naive
termwise sinc expansion cannot prove singularity exclusion.

Any viable version of this route must introduce a nontrivial resummation,
regularization, grouping, or cancellation mechanism before taking the Dirichlet
transform.

The Bach route is therefore not blocked because the finite pieces are bad. It
is blocked because reconstructing the zero detector from those pieces requires
extreme cancellation.

That cancellation is the RH-level difficulty.
