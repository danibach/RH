# Chebyshev Psi_B Route Toward RH

This note records how far the Bach-derived Chebyshev route gets toward the
Riemann Hypothesis, and where the remaining RH-strength obstacle sits.

## 1. Starting Point: Bach Prime Indicator

Let the divisor wave be:

```latex
\[
D_m(n)
=
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}.
\]
```

At integer inputs:

```latex
\[
D_m(n)
=
\begin{cases}
1, & m\mid n,\\
0, & m\nmid n.
\end{cases}
\]
```

Define the Bach prime indicator:

```latex
\[
Q_B(n)
=
\prod_{m=2}^{n-1}
\left(1-D_m(n)\right).
\]
```

Then:

```latex
\[
Q_B(n)
=
\begin{cases}
1, & n \text{ prime},\\
0, & n \text{ composite}.
\end{cases}
\]
```

Equivalently, with the prime-zero divisor sum:

```latex
\[
B(n)=\sum_{m=2}^{n-1}D_m(n),
\qquad
Q_B(n)=\operatorname{sinc}(B(n)).
\]
```

The product form is better for algebraic expansion; the sinc form is better
for zero-detection notation.

## 2. Bach Von Mangoldt Function

Define:

```latex
\[
\Lambda_B(N)
=
\sum_{\substack{k\ge1\\ n^k=N}}
Q_B(n)\log n.
\]
```

Since `Q_B(n)` selects only primes:

```latex
\[
\Lambda_B(N)
=
\begin{cases}
\log p, & N=p^k \text{ for a prime }p,\\
0, & \text{otherwise}.
\end{cases}
\]
```

Therefore:

```latex
\[
\boxed{\Lambda_B(N)=\Lambda(N)}
\]
```

where `Lambda` is the classical von Mangoldt function.

This step is exact. It does not prove new cancellation; it reconstructs the
classical arithmetic weight from the Bach prime selector.

## 3. Bach Chebyshev Function

Define:

```latex
\[
\psi_B(x)
=
\sum_{N\le x}\Lambda_B(N).
\]
```

Equivalently:

```latex
\[
\psi_B(x)
=
\sum_{k=1}^{\lfloor \log_2 x\rfloor}
\sum_{2\le n\le x^{1/k}}
Q_B(n)\log n.
\]
```

Since `Lambda_B=Lambda`:

```latex
\[
\boxed{\psi_B(x)=\psi(x)}
\]
```

and explicitly:

```latex
\[
\psi_B(x)=
\sum_{p^k\le x}\log p.
\]
```

## 4. RH-Equivalent Target

RH is equivalent to the Chebyshev error estimate:

```latex
\[
\boxed{
\psi(x)-x
=
O\!\left(\sqrt{x}\log^2 x\right)
}
\]
```

Because `psi_B(x)=psi(x)`, this becomes:

```latex
\[
\boxed{
\psi_B(x)-x
=
O\!\left(\sqrt{x}\log^2 x\right)
}
\]
```

Thus the Bach/psi route reduces RH to proving square-root-scale cancellation
in the Bach-derived weighted wave count.

## 5. Dirichlet Transform

Define:

```latex
\[
L_B(s)
=
\sum_{N=1}^{\infty}
\frac{\Lambda_B(N)}{N^s}.
\]
```

For `Re(s)>1`, substitute the definition of `Lambda_B`:

```latex
\[
L_B(s)
=
\sum_{n=2}^{\infty}
Q_B(n)\log n
\sum_{k=1}^{\infty}
\frac{1}{n^{ks}}.
\]
```

So:

```latex
\[
L_B(s)
=
\sum_{n=2}^{\infty}
Q_B(n)\log n
\frac{n^{-s}}{1-n^{-s}}.
\]
```

Since `Q_B` selects primes:

```latex
\[
L_B(s)
=
\sum_p
\log p
\frac{p^{-s}}{1-p^{-s}}
=
-\frac{\zeta'(s)}{\zeta(s)}.
\]
```

Therefore:

```latex
\[
\boxed{
L_B(s)=-\frac{\zeta'(s)}{\zeta(s)}
}
\qquad
(\operatorname{Re}(s)>1).
\]
```

## 6. Analytic RH Reformulation

The logarithmic derivative `-zeta'/zeta` has:

1. a simple pole at `s=1`,
2. poles at nontrivial zeros of `zeta`,
3. poles at trivial zeros.

Therefore an RH-equivalent analytic target is:

```latex
\[
\boxed{
L_B(s)-\frac{1}{s-1}
\text{ has no poles in }
\operatorname{Re}(s)>\frac12
}
\]
```

except for boundary behavior on the critical line itself.

If this pole exclusion could be proven directly from the Bach wave expression
for `Q_B`, the RH would follow.

## 7. Perron Inversion

For `c>1`, Perron inversion gives:

```latex
\[
\psi_B(x)
=
\frac{1}{2\pi i}
\int_{c-i\infty}^{c+i\infty}
L_B(s)\frac{x^s}{s}\,ds.
\]
```

If one can move the contour left to `Re(s)=1/2+epsilon` with only the pole at
`s=1`, then:

```latex
\[
\psi_B(x)=x+\text{controlled error}.
\]
```

The RH-scale target requires enough control to reach:

```latex
\[
\psi_B(x)-x
=
O\!\left(\sqrt{x}\log^2 x\right).
\]
```

This is the analytic form of the problem.

## 8. Internal Wave Expansion

The product-wave indicator expands as:

```latex
\[
Q_B(n)
=
\prod_{m=2}^{n-1}(1-D_m(n)).
\]
```

Using the integer-input rule:

```latex
\[
D_a(n)D_b(n)
=
D_{\operatorname{lcm}(a,b)}(n),
\]
```

one obtains the LCM expansion:

```latex
\[
Q_B(n)
=
\sum_{S\subseteq\{2,\ldots,n-1\}}
(-1)^{|S|}
D_{\operatorname{lcm}(S)}(n).
\]
```

Substitute this into the psi formula:

```latex
\[
\psi_B(x)
=
\sum_{k=1}^{\lfloor \log_2 x\rfloor}
\sum_{2\le n\le x^{1/k}}
\log n
\sum_{S\subseteq\{2,\ldots,n-1\}}
(-1)^{|S|}
D_{\operatorname{lcm}(S)}(n).
\]
```

The RH target becomes:

```latex
\[
\sum_{k=1}^{\lfloor \log_2 x\rfloor}
\sum_{2\le n\le x^{1/k}}
\log n
\sum_{S\subseteq\{2,\ldots,n-1\}}
(-1)^{|S|}
D_{\operatorname{lcm}(S)}(n)
-x
=
O\!\left(\sqrt{x}\log^2 x\right).
\]
```

This is the most direct Bach-wave cancellation target for the `psi_B` route.

## 9. Main Obstacle

The route reaches an exact RH-equivalent target, but it does not yet prove the
target.

The central obstruction is the moving cutoff:

```latex
\[
S\subseteq\{2,\ldots,n-1\}.
\]
```

The expansion coefficients depend on the evaluated integer `n`. This prevents
the expression from immediately becoming a fixed Dirichlet convolution with
stable coefficients.

After grouping by LCM, the problem becomes a cancellation problem over
LCM-indexed correlations. That is close to classical sieve/Mobius
cancellation, but RH requires a square-root-scale bound, not just exact
prime selection.

## 10. What Has Been Achieved

The `psi_B` route currently achieves:

1. exact Bach reconstruction of the prime indicator,
2. exact Bach reconstruction of the von Mangoldt function,
3. exact identity `psi_B(x)=psi(x)`,
4. exact identity `L_B(s)=-zeta'(s)/zeta(s)` for `Re(s)>1`,
5. an RH-equivalent target in terms of `psi_B(x)-x`,
6. an internal wave-correlation expression for the target.

This is a valid RH-equivalent reformulation.

## 11. What Remains Missing

The missing theorem is:

```latex
\[
\boxed{
\text{Prove }
\psi_B(x)-x
=
O\!\left(\sqrt{x}\log^2 x\right)
\text{ directly from the Bach wave/LCM structure.}
}
\]
```

Equivalently:

```latex
\[
\boxed{
\text{Prove that }L_B(s)-\frac{1}{s-1}
\text{ has no poles in }\operatorname{Re}(s)>\frac12
\text{ from the wave expansion.}
}
\]
```

This is exactly where the RH-level difficulty remains.

## 12. Practical Next Attacks

The most concrete next steps are:

1. **LCM coefficient estimates**: estimate the grouped coefficients in
   `Q_B(n)=sum_q C_n(q)D_q(n)` strongly enough after `log n` weighting.
2. **Moving-cutoff removal**: find a stable transform that replaces
   `m<n` by fixed coefficient families plus a controllable boundary term.
3. **Smoothed psi sums**: replace the sharp cutoff `N<=x` by a smooth weight,
   then study the Mellin transform of the Bach wave expansion.
4. **Prime-power separation**: isolate the `k=1` theta contribution and prove
   that `k>=2` terms are lower-order at RH scale.
5. **Numerical correlation diagnostics**: measure whether grouped LCM
   coefficients show stable cancellation patterns before importing zeta zeros.

## 13. Current Assessment

The Chebyshev `psi_B` route is stronger than the plain prime-counting route
because the von Mangoldt weight is the natural object behind the logarithmic
derivative of zeta.

It does not prove RH as-is. It converts RH into a precise wave-correlation
cancellation problem. The best chance for progress is not the exact identity
`psi_B=psi`, but a new estimate on the internal LCM/Mobius correlation
structure of the Bach prime indicator.
