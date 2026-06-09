# Bach-Form Prime Counting Formula

## Exact Prime Counting Formula

The Bach-form version of the prime counting function is:

```latex
\[
\boxed{
\pi(x)=
\sum_{2\le n\le x}
\prod_{m=2}^{n-1}
\left(
1-
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
\right)
}
\]
```

That is the exact Bach-form version of prime counting.

## Interpretation

The inner term

```latex
\[
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
\]
```

acts as a divisibility detector:

```latex
\[
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
=
\begin{cases}
1, & m\mid n,\\
0, & m\nmid n.
\end{cases}
\]
```

Therefore, each factor

```latex
\[
1-
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
\]
```

equals `0` when `m` divides `n`, and equals `1` otherwise.

So the product

```latex
\[
\prod_{m=2}^{n-1}
\left(
1-
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
\right)
\]
```

equals `1` exactly when no integer `m` with `2 <= m <= n - 1` divides `n`.

Hence:

```latex
\[
\prod_{m=2}^{n-1}
\left(
1-
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
\right)
=
\begin{cases}
1, & n \text{ is prime},\\
0, & n \text{ is composite}.
\end{cases}
\]
```

Summing this prime indicator over all integers `2 <= n <= x` gives:

```latex
\[
\pi(x)=
\sum_{2\le n\le x}
\prod_{m=2}^{n-1}
\left(
1-
\frac1m\sum_{j=0}^{m-1}e^{2\pi i jn/m}
\right).
\]
```
