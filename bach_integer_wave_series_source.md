# Bach Integer Wave-Series Encoding

## Project Goal

Construct one wave-like infinite series `f_m(n)` for every integer `m >= 2`
such that:

1. `f_m(n)` is zero at all integer values except proper multiples of `m`.
2. The infinite sum of `f_m(n)` over `n` equals the number `m` itself.
3. The sum of all such waves, from `m = 2` to infinity, is zero at prime
   integer inputs.
4. Ideally, the construction should also have a smooth real-valued extension.

## Key Correction

To make the final combined function zero at primes, each `f_m` must ignore the
first multiple `m` itself. The wave should live on proper multiples:

```latex
2m, 3m, 4m, \ldots
```

not on:

```latex
m, 2m, 3m, \ldots
```

Otherwise, for a prime `p`, the term `f_p(p)` would contribute, so the combined
function would not be zero at primes.

## Discrete Formula

For `m >= 2`, define:

```latex
f_m(n)=
\begin{cases}
\displaystyle
\frac{m}{1-\ln 2}\frac{(-1)^k}{k},
& n=km,\quad k\ge 2,\\[1em]
0,
& \text{otherwise}.
\end{cases}
```

Then:

```latex
\sum_{n=1}^{\infty} f_m(n)=m
```

because:

```latex
\sum_{k=2}^{\infty}\frac{(-1)^k}{k}=1-\ln 2.
```

Thus each integer `m >= 2` is encoded as an infinite series.

## Combined Function

For a finite cutoff `M`:

```latex
F_M(n)=\sum_{m=2}^{M}f_m(n)
```

and:

```latex
\sum_{n=1}^{\infty}F_M(n)
=
\sum_{m=2}^{M}m
=
\frac{M(M+1)}{2}-1.
```

For the infinite version:

```latex
F_\infty(n)=\sum_{m=2}^{\infty}f_m(n)
```

which reduces, at each fixed integer `n`, to the divisor formula:

```latex
F_\infty(n)=
\sum_{\substack{m\mid n\\2\le m<n}}
\frac{m}{1-\ln 2}
\frac{(-1)^{n/m}}{n/m}.
```

Therefore, for a prime `p`, there is no divisor `m` satisfying:

```latex
2\le m<p.
```

So:

```latex
F_\infty(p)=0.
```

The total encoded sum is, in the ordinary sense:

```latex
2+3+4+5+\cdots=\infty.
```

## Smooth Real Extension

A smooth version can be made, with an important caveat: it matches the
arithmetic behavior at integer samples, not at every real value.

Use the root-of-unity detector:

```latex
C_m(x)=\frac{1}{m}\sum_{r=0}^{m-1}
\cos\left(\frac{2\pi r x}{m}\right)
```

and define:

```latex
\tilde f_m(x)=
\frac{m}{1-\ln 2}
C_m(x)
\left[
1-\operatorname{sinc}\left(\frac{x}{m}-1\right)
\right]
\frac{\cos(\pi x/m)}{x/m}.
```

At integer values `x = n`, this reproduces the discrete `f_m(n)`. This gives a
smooth wave-like real function whose integer samples encode the prime-zero
structure.
