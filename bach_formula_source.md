# Bach's Formula

## Definition

For integer `n` from `2` to infinity, Bach's formula is written as:

```text
B(n) =
sum from m = 2 to n - 1 of
(
    (1 / m) * sum from j = 0 to m - 1 of exp(2*pi*i*j*n/m)
)
```

In mathematical notation:

```latex
B(n)=
\sum_{m=2}^{n-1}
\left(
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i j n/m}
\right),
\qquad n\in \mathbb{N},\ n\ge 2
```

## Prime Criterion

For integers `n >= 2`:

```latex
B(n)=0 \iff n \text{ is prime}
```

## Infinite Sequence Form

Equivalently, Bach's formula may be viewed as an infinite sequence:

```latex
\{B(n)\}_{n=2}^{\infty}
```

where each term is given by:

```latex
B(n)=
\sum_{m=2}^{n-1}
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i j n/m}
```

The first values are:

```text
B(2) = 0
B(3) = 0
B(4) = 1
B(5) = 0
B(6) = 2
B(7) = 0
B(8) = 1
...
```

## Interpretation

The inner expression

```latex
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i j n/m}
```

acts as a divisibility detector. It equals `1` when `m` divides `n`, and `0` otherwise.

Therefore, `B(n)` counts the divisors of `n` excluding `1` and `n`.

Thus, prime numbers are exactly the integer values `n >= 2` where Bach's formula equals zero.
