# Bach Product Correlation Expansion

## 1. Bach Prime Indicator

Start with the exact Bach-form prime indicator:

```latex
\[
Q_B(n)=
\prod_{m=2}^{n-1}
\left(
1-
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
\right).
\]
```

Write the divisibility wave as:

```latex
\[
D_m(n)=
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}.
\]
```

At integer `n`,

```latex
\[
D_m(n)=
\begin{cases}
1, & m\mid n,\\
0, & m\nmid n.
\end{cases}
\]
```

So:

```latex
\[
Q_B(n)=
\prod_{m=2}^{n-1}(1-D_m(n)).
\]
```

This equals `1` if `n` is prime and `0` if `n` is composite.

## 2. Full Correlation Expansion

Expanding the product gives:

```latex
\[
Q_B(n)=
\sum_{S\subseteq\{2,\dots,n-1\}}
(-1)^{|S|}
\prod_{m\in S}D_m(n).
\]
```

Since each `D_m(n)` is a divisibility detector,

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
Q_B(n)=
\sum_{S\subseteq\{2,\dots,n-1\}}
(-1)^{|S|}
D_{\operatorname{lcm}(S)}(n).
\]
```

Grouping terms by their least common multiple gives:

```latex
\[
Q_B(n)=
\sum_{q}
C_n(q)D_q(n),
\]
```

where

```latex
\[
C_n(q)=
\sum_{\substack{S\subseteq\{2,\dots,n-1\}\\
\operatorname{lcm}(S)=q}}
(-1)^{|S|}.
\]
```

These `C_n(q)` are the divisor-wave correlation coefficients.

## 3. What the Coefficients Become

For `q < n`, the coefficient is the Mobius function:

```latex
\[
C_n(q)=\mu(q).
\]
```

This happens because the subsets with lcm dividing `q` form the product

```latex
\[
\prod_{\substack{d\mid q\\d>1}}(1-1)=0,
\qquad q>1,
\]
```

and Mobius inversion recovers the exact-lcm coefficient.

For composite `n`, the missing top divisor `n` is replaced by correlations of
proper divisors. The coefficient at `q=n` becomes:

```latex
\[
C_n(n)=\mu(n).
\]
```

For prime `n`, there is no proper divisor system that can produce lcm `n`, so
the empty product remains:

```latex
\[
Q_B(n)=1.
\]
```

## 4. Prime-Only Compression

The composite waves are redundant. If a composite `m` divides `n`, then at
least one prime `p\mid m` also divides `n`.

Thus the product

```latex
\[
\prod_{m=2}^{z}(1-D_m(n))
\]
```

has the same zero/nonzero behavior as

```latex
\[
\prod_{p\le z}(1-D_p(n)).
\]
```

Expanding only over primes gives the squarefree sieve:

```latex
\[
\prod_{p\le z}(1-D_p(n))
=
\sum_{d\mid P(z)}\mu(d)D_d(n),
\]
```

where

```latex
\[
P(z)=\prod_{p\le z}p.
\]
```

This is exactly the Eratosthenes-Legendre inclusion-exclusion structure.

## 5. Exact Counting Version

For a fixed cutoff `z`, define

```latex
\[
\Phi(x,z)=
\sum_{n\le x}\prod_{p\le z}(1-D_p(n)).
\]
```

Then:

```latex
\[
\Phi(x,z)=
\sum_{d\mid P(z)}\mu(d)\left\lfloor\frac{x}{d}\right\rfloor.
\]
```

Taking `z=\sqrt{x}` gives Legendre's exact prime-counting formula:

```latex
\[
\pi(x)=
\pi(\sqrt{x})-1+\Phi(x,\sqrt{x}).
\]
```

So the Bach product, after correlation expansion and prime-wave compression,
lands on the classical exact sieve formula.

## 6. RH-Scale Target

The weighted Bach count is:

```latex
\[
\theta_B(x)=
\sum_{n\le x}Q_B(n)\log n.
\]
```

Since `Q_B(n)` is the prime indicator,

```latex
\[
\theta_B(x)=\theta(x)=\sum_{p\le x}\log p.
\]
```

The Riemann Hypothesis is equivalent to the estimate:

```latex
\[
\theta_B(x)=x+O(\sqrt{x}\log^2 x).
\]
```

So a Bach-based RH proof would need to prove square-root cancellation in the
expanded correlation sum:

```latex
\[
\sum_{n\le x}
\log n
\sum_q C_n(q)D_q(n)
=
x+O(\sqrt{x}\log^2 x).
\]
```

## 7. Structural Learning

The expansion reveals this chain:

```latex
\[
\text{Bach divisor waves}
\longrightarrow
\text{lcm correlations}
\longrightarrow
\text{Mobius coefficients}
\longrightarrow
\text{Legendre sieve}
\longrightarrow
\theta(x)-x.
\]
```

The promising structure is the appearance of Mobius cancellation.

The obstacle is that this is exactly the cancellation problem already hiding in
the prime number theorem and RH. The Bach product makes the cancellation
visible, but proving RH would require a new bound on the cumulative correlation
sum strong enough to force:

```latex
\[
\theta_B(x)-x=O(\sqrt{x}\log^2 x).
\]
```
