# Algebraic Connection Between Bach's Formula and Riemann's Zeta Function

## Bach's Formula as a Divisor Function

Bach's formula is:

```latex
B(n)=
\sum_{m=2}^{n-1}
\left(
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i j n/m}
\right)
```

The inner term acts as a divisibility detector:

```latex
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i j n/m}
=
\begin{cases}
1, & m \mid n \\
0, & m \nmid n
\end{cases}
```

Therefore, Bach's formula counts all divisors of `n` except `1` and `n`.

Let:

```latex
\tau(n)=\sum_{d\mid n}1
```

where `tau(n)` is the divisor-counting function. Then:

```latex
B(n)=\tau(n)-2
```

So:

```latex
B(n)=0
\iff
\tau(n)=2
\iff
n \text{ is prime}
```

for integers `n >= 2`.

## Dirichlet Series Connection

The Riemann zeta function is:

```latex
\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}
```

The divisor-counting function satisfies:

```latex
\sum_{n=1}^{\infty}\frac{\tau(n)}{n^s}
=
\zeta(s)^2
```

Since:

```latex
B(n)=\tau(n)-2
```

we have:

```latex
\sum_{n=2}^{\infty}\frac{B(n)}{n^s}
=
\sum_{n=2}^{\infty}\frac{\tau(n)-2}{n^s}
```

Equivalently:

```latex
\sum_{n=2}^{\infty}\frac{B(n)}{n^s}
=
(\zeta(s)-1)^2
```

This is a direct algebraic bridge between Bach's formula and the Riemann zeta function.

## Coefficient Interpretation

Because:

```latex
\zeta(s)-1
=
\sum_{n=2}^{\infty}\frac{1}{n^s}
```

then:

```latex
(\zeta(s)-1)^2
=
\sum_{a=2}^{\infty}
\sum_{b=2}^{\infty}
\frac{1}{(ab)^s}
```

The coefficient of `1/n^s` counts how many ways `n` can be written as:

```latex
n=ab,\qquad a,b\ge2
```

That coefficient is exactly `B(n)`.

So Bach's formula is the coefficient sequence of:

```latex
(\zeta(s)-1)^2
```

## Prime-Zeta Connection

If we define the prime-zeta function using the zeros of Bach's formula:

```latex
P_B(s)
=
\sum_{\substack{n\ge2\\B(n)=0}}
\frac{1}{n^s}
```

then since `B(n)=0` exactly at primes:

```latex
P_B(s)
=
\sum_{p}
\frac{1}{p^s}
```

This is the prime-zeta function.

Riemann's zeta function satisfies:

```latex
\log \zeta(s)
=
\sum_{k=1}^{\infty}
\frac{1}{k}
P_B(ks)
```

## Summary

The algebraic chain is:

```latex
B(n)
\longleftrightarrow
\tau(n)-2
\longleftrightarrow
(\zeta(s)-1)^2
```

and the prime-zero part gives:

```latex
B(n)=0
\longleftrightarrow
P_B(s)
\longleftrightarrow
\log \zeta(s)
```

Thus Bach's formula can be connected algebraically to Riemann's zeta function. The key is that Bach's formula is a wave-form version of divisor counting, and divisor counting lives naturally inside `zeta(s)^2`.
