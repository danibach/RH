# LCM Wave-Correlation Route Toward RH

This note records how far the LCM wave-correlation expansion gets toward a
Riemann Hypothesis route, and where the remaining RH-strength difficulty
enters.

## 1. Divisor Wave Algebra

Let:

```latex
\[
D_m(n)=
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}.
\]
```

At integer `n`:

```latex
\[
D_m(n)=
\begin{cases}
1, & m\mid n,\\
0, & m\nmid n.
\end{cases}
\]
```

The key product rule is:

```latex
\[
D_a(n)D_b(n)
=
D_{\operatorname{lcm}(a,b)}(n)
\]
```

at integer inputs. Thus products of divisibility waves collapse to a single
wave indexed by a least common multiple.

## 2. Bach Prime Indicator

The product-wave prime indicator is:

```latex
\[
Q_B(n)=
\prod_{m=2}^{n-1}
\left(1-D_m(n)\right).
\]
```

Then:

```latex
\[
Q_B(n)=
\begin{cases}
1, & n \text{ prime},\\
0, & n \text{ composite}.
\end{cases}
\]
```

## 3. LCM Correlation Expansion

Expand the product:

```latex
\[
Q_B(n)=
\sum_{S\subseteq\{2,\ldots,n-1\}}
(-1)^{|S|}
\prod_{m\in S}D_m(n).
\]
```

Using the product rule:

```latex
\[
\prod_{m\in S}D_m(n)
=
D_{\operatorname{lcm}(S)}(n).
\]
```

Therefore:

```latex
\[
\boxed{
Q_B(n)=
\sum_{S\subseteq\{2,\ldots,n-1\}}
(-1)^{|S|}
D_{\operatorname{lcm}(S)}(n)
}
\]
```

Group by LCM:

```latex
\[
Q_B(n)=
\sum_q C_n(q)D_q(n),
\]
```

where:

```latex
\[
C_n(q)=
\sum_{\substack{
S\subseteq\{2,\ldots,n-1\}\\
\operatorname{lcm}(S)=q}}
(-1)^{|S|}.
\]
```

The coefficients `C_n(q)` are the LCM wave-correlation coefficients.

## 4. Mobius Structure

For `q < n`, all divisors of `q` are available inside the set
`\{2,\ldots,n-1\}`. The exact-LCM coefficient is:

```latex
\[
C_n(q)=\mu(q).
\]
```

Thus the LCM correlation expansion exposes Mobius cancellation inside the Bach
prime indicator.

The coefficient dependence on `n` matters only at and beyond the moving cutoff.
This moving cutoff is one of the main analytic obstacles.

## 5. Prime-Wave Compression

Composite divisor waves are redundant for detecting compositeness. If a
composite `m` divides `n`, then some prime `p\mid m` also divides `n`.

For a fixed cutoff `z`, define:

```latex
\[
Q_z(n)=
\prod_{p\le z}
\left(1-D_p(n)\right).
\]
```

Expanding only over prime waves gives:

```latex
\[
\boxed{
Q_z(n)=
\sum_{d\mid P(z)}
\mu(d)D_d(n)
}
\]
```

where:

```latex
\[
P(z)=\prod_{p\le z}p.
\]
```

This is the classical squarefree sieve written in divisor-wave notation.

## 6. Exact Prime Counting Reached From LCM Correlations

Define:

```latex
\[
\Phi(x,z)=
\sum_{n\le x}Q_z(n).
\]
```

Then:

```latex
\[
\Phi(x,z)=
\sum_{d\mid P(z)}
\mu(d)
\left\lfloor\frac{x}{d}\right\rfloor.
\]
```

Taking `z=\sqrt{x}` gives Legendre's exact formula:

```latex
\[
\boxed{
\pi(x)=
\pi(\sqrt{x})-1+\Phi(x,\sqrt{x})
}
\]
```

So the LCM wave-correlation expansion reaches an exact classical
prime-counting formula. This is a rigorous algebraic reduction, but it is not
yet an RH proof.

## 7. RH-Facing Weighted Target

The weighted Bach theta function is:

```latex
\[
\theta_B(x)=
\sum_{n\le x}Q_B(n)\log n.
\]
```

Since `Q_B(n)` is exactly the prime indicator:

```latex
\[
\theta_B(x)=
\theta(x)=
\sum_{p\le x}\log p.
\]
```

RH is equivalent to the estimate:

```latex
\[
\boxed{
\theta_B(x)-x=
O\!\left(\sqrt{x}\log^2 x\right)
}
\]
```

Equivalently, using the LCM expansion:

```latex
\[
\sum_{n\le x}
\log n
\sum_q C_n(q)D_q(n)
-
x
=
O\!\left(\sqrt{x}\log^2 x\right).
\]
```

This is the direct LCM-correlation cancellation target.

## 8. Psi Version

The von Mangoldt route gives an even closer RH-equivalent target. Define:

```latex
\[
\Lambda_B(N)=
\sum_{\substack{k\ge1\\ n^k=N}}
Q_B(n)\log n.
\]
```

Then:

```latex
\[
\Lambda_B(N)=\Lambda(N),
\]
```

and:

```latex
\[
\psi_B(x)=
\sum_{N\le x}\Lambda_B(N)=\psi(x).
\]
```

RH is equivalent to:

```latex
\[
\boxed{
\psi_B(x)-x=
O\!\left(\sqrt{x}\log^2 x\right)
}
\]
```

The LCM route would need to prove this bound from:

```latex
\[
Q_B(n)=
\sum_q C_n(q)D_q(n)
\]
```

without importing the known zeta-zero explicit formula.

## 9. What The Route Proves Now

The LCM expansion currently proves:

1. Products of divisor waves collapse to LCM waves.
2. The Bach product expands into LCM-indexed correlations.
3. The grouped coefficients expose Mobius structure.
4. Prime-wave compression recovers the squarefree sieve.
5. The exact Legendre prime-counting formula follows.
6. The RH-facing target becomes a concrete cancellation estimate over
   LCM/Mobius correlations.

This is substantial structure, but it does not yet prove RH.

## 10. Main Obstruction

After grouping, the route lands on classical Mobius/sieve cancellation. The
remaining missing estimate is essentially:

```latex
\[
\sum_{n\le x}
\log n
\sum_q C_n(q)D_q(n)
=
x+O\!\left(\sqrt{x}\log^2 x\right).
\]
```

or the corresponding `psi_B` estimate.

The algebra makes the cancellation visible, but the current formulation does
not yet bound it.

## 11. Most Concrete Next Attack

The next useful problem is to search for a stable grouping that removes or
controls the moving cutoff `m<n`.

A possible analytic form is:

```latex
\[
\sum_A
(-1)^{|A|}
\operatorname{lcm}(A)^{-s}
\zeta\!\left(
s,
\left\lfloor
\frac{\max A}{\operatorname{lcm}(A)}
\right\rfloor+1
\right),
\]
```

where the sum is over finite sets `A` of integers greater than `1`.

Each fixed set contributes a Hurwitz-zeta type term with only the expected
pole at `s=1`. The hard problem is to prove enough cancellation in the outer
LCM/inclusion-exclusion sum to obtain locally uniform convergence in
`\operatorname{Re}(s)>1/2`, away from `s=1`.

If that could be proven from the wave-correlation structure, it would give an
RH-level singularity-exclusion result for the Bach/prime-zeta transform.

## 12. LCM/Max Cutoff Refinement

To isolate the moving cutoff, define the global cutoff coefficients:

```latex
\[
F_M(q)=
\sum_{\substack{
S\subseteq\{2,\ldots,M\}\\
\operatorname{lcm}(S)=q}}
(-1)^{|S|}.
\]
```

Then:

```latex
\[
\prod_{m=2}^{M}(1-D_m(n))
=
\sum_q F_M(q)D_q(n).
\]
```

Define the cutoff layer:

```latex
\[
G_M(q)=F_M(q)-F_{M-1}(q).
\]
```

This groups the correlations whose largest selected wave index is exactly
`M`.

The prime-wave compression gives the exact identity:

```latex
\[
G_M(q)=0
\qquad
\text{when }M\text{ is composite}.
\]
```

When `M=p` is prime:

```latex
\[
G_p(q)=
\begin{cases}
\mu(q),
& q\mid P(p),\ p\mid q,\\
0,
& \text{otherwise},
\end{cases}
\]
```

where:

```latex
\[
P(p)=\prod_{\ell\le p}\ell.
\]
```

Thus the moving cutoff does not create genuinely new layers at every integer.
After LCM grouping, it changes only when a new prime wave enters.

This is a useful simplification, but it also means the route has returned to
the classical squarefree prime sieve. The remaining RH-level difficulty is
still the cumulative Mobius/squarefree cancellation.

## 13. Least-Prime-Factor Interpretation

At integer samples, the prime layer has a direct interpretation. Let:

```latex
\[
G_p(n)=
\sum_q G_p(q)D_q(n).
\]
```

Then:

```latex
\[
\boxed{
G_p(n)=
-D_p(n)
\prod_{\ell<p}
\left(1-D_\ell(n)\right)
}
\]
```

where the product runs over primes `ell < p`.

Therefore:

```latex
\[
G_p(n)=
\begin{cases}
-1, & p \text{ is the least prime factor of } n,\\
0, & \text{otherwise}.
\end{cases}
\]
```

The Bach prime indicator becomes:

```latex
\[
\boxed{
Q_B(n)=
1+
\sum_{p<n}G_p(n)
}
\]
```

For prime `n`, no prime `p<n` divides `n`, so the sum is zero and
`Q_B(n)=1`. For composite `n`, exactly one prime is the least prime factor,
so the sum contributes `-1` and `Q_B(n)=0`.

This is a strong structural endpoint for the LCM/max route:

```latex
\[
\text{LCM wave correlations}
\longrightarrow
\text{prime layers}
\longrightarrow
\text{least-prime-factor sieve}.
\]
```

It is exact, but it is still a sieve decomposition. To reach RH, one would
need strong cancellation estimates for the cumulative weighted form of this
least-prime-factor decomposition.

## 14. Current Assessment

The LCM wave-correlation route is not a shortcut around the RH difficulty. It
is a re-expression of the difficulty as an explicit cancellation problem over
LCM-indexed divisor-wave correlations.

Its value is that it gives a concrete object to attack:

```latex
\[
C_n(q)
\quad\text{and}\quad
\sum_q C_n(q)D_q(n).
\]
```

The route becomes genuinely new only if one can prove cancellation for these
correlations more directly than through the classical zeta-zero machinery.

## 15. Computational Check

The script `explore_bach_correlations.py` checks the finite identities behind
this route. For example:

```bash
python3 explore_bach_correlations.py \
  --n 30 \
  --theta-limit 120 \
  --verify-limit 120 \
  --verify-global-limit 30 \
  --verify-layer-limit 30 \
  --verify-least-factor-limit 80 \
  --dirichlet-swap-limit 20 \
  --legendre-x 1000
```

This verifies:

1. The LCM-coefficient indicator equals the prime indicator through
   `n = 120`.
2. Contributing coefficients below `n` match the Mobius function.
3. The top coefficient at `q=n` matches `mu(n)` for composites.
4. The global cutoff coefficients `F_M(q)` give the same prime indicator.
5. The cutoff layers `G_M(q)` vanish at composite `M` and match the
   squarefree prime layer at prime `M`.
6. The prime layers are exactly least-prime-factor layers through `n = 80`.
7. The finite LCM/max Dirichlet swap agrees with the direct finite sum.
8. The Legendre/Bach prime-wave compression gives `pi(1000)=168`.

These are finite algebraic checks. They support the reduction to the classical
sieve, but they do not address the missing RH-scale cancellation estimate.
