# Bach Prime Identification and Counting Formulas

## Bach Prime Identification Formula

For an integer `n >= 2`, define:

```latex
\[
B(n)=
\sum_{m=2}^{n-1}
\left(
\frac1m
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
\right).
\]
```

The inner term is a divisibility detector:

```latex
\[
\frac1m
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
=
\begin{cases}
1, & m\mid n,\\
0, & m\nmid n.
\end{cases}
\]
```

So `B(n)` counts the divisors of `n` between `2` and `n - 1`.

Therefore:

```latex
\[
\boxed{
B(n)=0
\iff
n \text{ is prime}
}
\]
```

So primes are exactly the integers where Bach's formula vanishes.

## Bach Prime Counting Formula

Define the prime indicator:

```latex
\[
Q_B(n)=
\prod_{m=2}^{n-1}
\left(
1-
\frac1m
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
\right).
\]
```

Then:

```latex
\[
Q_B(n)=
\begin{cases}
1, & n \text{ is prime},\\
0, & n \text{ is composite}.
\end{cases}
\]
```

So the prime counting function becomes:

```latex
\[
\boxed{
\pi(x)=
\sum_{2\le n\le x}
\prod_{m=2}^{n-1}
\left(
1-
\frac1m
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
\right)
}
\]
```

## Explanation

Bach's identification formula detects whether one number is prime.

Bach's counting formula adds that detector over all integers up to `x`, so it
counts how many primes are less than or equal to `x`.
