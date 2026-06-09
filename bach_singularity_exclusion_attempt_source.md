# Bach-Only Singularity Exclusion Attempt

## Target

The RH-equivalent target is:

```latex
P_B(s)=
\sum_{n=2}^{\infty}
\frac{\operatorname{sinc}(B(n))}{n^s}
```

has no singularities in:

```latex
\operatorname{Re}(s)>1/2
```

except at:

```latex
s=1.
```

Here:

```latex
B(n)=d(n)-2
```

and:

```latex
\operatorname{sinc}(B(n))
=
\begin{cases}
1, & n \text{ prime},\\
0, & n \text{ composite}.
\end{cases}
```

Thus `P_B(s)` is the prime zeta function:

```latex
P_B(s)=\sum_p p^{-s}.
```

The goal is to prove the singularity exclusion from the Bach/root-of-unity
structure, not from known zeta-zero information.

## Attempt 1: Fourier Integral of the Zero Detector

Because `B(n)` is an integer:

```latex
\operatorname{sinc}(B(n))
=
\int_{-1/2}^{1/2} e^{2\pi i t B(n)}\,dt.
```

Since:

```latex
B(n)=d(n)-2,
```

we get:

```latex
P_B(s)=
\int_{-1/2}^{1/2}
e^{-4\pi i t}
\left(
\sum_{n=2}^{\infty}
\frac{e^{2\pi i t d(n)}}{n^s}
\right)\,dt.
```

So the problem becomes understanding:

```latex
D_t(s)=
\sum_{n=2}^{\infty}
\frac{e^{2\pi i t d(n)}}{n^s}.
```

### Obstruction

The divisor function `d(n)` is multiplicative, but `e^{2π i t d(n)}` is not
multiplicative in general. Therefore `D_t(s)` does not have a simple Euler
product.

Without an Euler product or another analytic continuation mechanism for
`D_t(s)`, this route does not yet prove the desired half-plane analyticity.

## Attempt 2: Power Series Expansion of sinc

Use:

```latex
\operatorname{sinc}(x)=
\sum_{j=0}^{\infty}
\frac{(-1)^j\pi^{2j}x^{2j}}{(2j+1)!}.
```

Then formally:

```latex
P_B(s)=
\sum_{j=0}^{\infty}
\frac{(-1)^j\pi^{2j}}{(2j+1)!}
\sum_{n=2}^{\infty}
\frac{(d(n)-2)^{2j}}{n^s}.
```

For each fixed `j`, the inner Dirichlet series can be expanded into finitely
many series involving powers of `d(n)`.

For fixed `q`, the Dirichlet series:

```latex
D_q(s)=
\sum_{n=1}^{\infty}
\frac{d(n)^q}{n^s}
```

has Euler product:

```latex
D_q(s)=
\prod_p
\sum_{a=0}^{\infty}
\frac{(a+1)^q}{p^{as}}.
```

Since:

```latex
\sum_{a=0}^{\infty}(a+1)^q x^a
=1+2^q x+O_q(x^2),
```

we can factor:

```latex
D_q(s)=\zeta(s)^{2^q}H_q(s),
```

where `H_q(s)` is analytic for `Re(s)>1/2`.

Thus each finite power piece has no singularities in `Re(s)>1/2` except
possibly at `s=1`.

### Obstruction

To conclude the desired result, one would need to justify interchanging the
infinite sinc power series with the Dirichlet transform and prove locally
uniform convergence in `Re(s)>1/2`, away from `s=1`.

This is not currently justified. The finite pieces can grow extremely rapidly
with `j`, because factors like:

```latex
\zeta(s)^{2^{2j}}
```

appear. The factorial denominator in the sinc expansion is not enough under
naive estimates.

So this route identifies a possible analytic mechanism, but the needed
uniform-convergence estimate is essentially RH-strength.

## Attempt 3: Inclusion-Exclusion over Divisibility Detectors

At integer `n`, the prime indicator can be written as:

```latex
I_B(n)=
\prod_{m=2}^{n-1}
\left(1-C_m(n)\right),
```

where:

```latex
C_m(n)=
\frac{1}{m}\sum_{r=0}^{m-1}e^{2\pi i r n/m}
```

equals `1` if `m|n` and `0` otherwise.

Expanding:

```latex
I_B(n)=
\sum_{A\subseteq\{2,\ldots,n-1\}}
(-1)^{|A|}
\prod_{m\in A}C_m(n).
```

But:

```latex
\prod_{m\in A}C_m(n)
=
1_{\operatorname{lcm}(A)\mid n}.
```

So, formally:

```latex
P_B(s)=
\sum_A
(-1)^{|A|}
\sum_{\substack{n>\max A\\ \operatorname{lcm}(A)\mid n}}
\frac{1}{n^s}.
```

For each fixed finite set `A`, the inner sum is a shifted Hurwitz-zeta type
series:

```latex
\operatorname{lcm}(A)^{-s}
\zeta\left(s,\left\lfloor \frac{\max A}{\operatorname{lcm}(A)}\right\rfloor+1\right),
```

which is meromorphic with only a pole at `s=1`.

### Obstruction

The outer sum over all finite sets `A` is enormous and alternating. Absolute
convergence fails, and the required cancellation is exactly the hard part.

If one could prove locally uniform convergence of a correctly grouped version
of this inclusion-exclusion expansion in `Re(s)>1/2`, away from `s=1`, the
singularity target would follow.

## Current Status

The Bach representation gives several natural analytic routes, and each route
reduces RH to a concrete cancellation or convergence problem:

1. Continue the Fourier-twisted divisor series `D_t(s)`.
2. Control the infinite sinc-power expansion after transforming.
3. Prove half-plane convergence of the inclusion-exclusion/lcm expansion.

None of these steps is currently proven here.

The most promising-looking route is Attempt 2, because each finite divisor-power
piece already has the desired singularity structure. The missing ingredient is a
new uniform-convergence or cancellation estimate strong enough to pass from the
finite pieces to the full sinc zero detector.

That missing estimate would be an RH-level result.
