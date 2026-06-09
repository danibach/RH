# Wave-Based Prime-Zero and Prime Counting Functions

This note records the three-step wave plan for identifying and counting primes
using only finite wave sums.

## A. Multiple Wave For Each Integer

For integers `m >= 2` and `n`, define the roots-of-unity multiple wave:

```latex
\[
W_m(n)
=
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}.
\]
```

The roots of unity cancel unless the wave completes an integer number of full
turns. Thus, at integer `n`,

```latex
\[
W_m(n)
=
\begin{cases}
1, & m\mid n,\\
0, & m\nmid n.
\end{cases}
\]
```

So each integer `m` has its own wave: it is zero at integer non-multiples of
`m` and equals `1` at integer multiples of `m`.

## B. Prime-Zero Wave Sum

To make primes vanish, the wave for `n` itself must not be included at input
`n`. Therefore define the proper-multiple wave sum:

```latex
\[
Z_{\mathrm{wave}}(n)
=
\sum_{m=2}^{n-1}W_m(n).
\]
```

Equivalently, expanded:

```latex
\[
Z_{\mathrm{wave}}(n)
=
\sum_{m=2}^{n-1}
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}.
\]
```

At integer `n >= 2`, `Z_wave(n)` counts the proper divisors of `n`, excluding
`1` and `n`. Therefore:

```latex
\[
\boxed{
Z_{\mathrm{wave}}(n)=0
\iff
n \text{ is prime}
}
\]
```

This is the prime-zero function: primes are the zero samples.

## C. Prime Counting From The Prime-Zero Function

Since `Z_wave(n)` is zero at primes and a positive integer at composites, a
sine wave turns it into a `0/1` prime indicator:

```latex
\[
P_{\mathrm{wave}}(n)
=
\operatorname{sinc}\!\left(Z_{\mathrm{wave}}(n)\right),
\qquad
\operatorname{sinc}(y)=\frac{\sin(\pi y)}{\pi y},
\quad
\operatorname{sinc}(0)=1.
\]
```

Thus:

```latex
\[
P_{\mathrm{wave}}(n)
=
\begin{cases}
1, & n \text{ is prime},\\
0, & n \text{ is composite}.
\end{cases}
\]
```

Now define the wave-based prime-counting function:

```latex
\[
\boxed{
B_{\pi,\mathrm{wave}}(x)
=
\sum_{2\le n\le x}
P_{\mathrm{wave}}(n)
}
\]
```

or, fully expanded from the waves:

```latex
\[
B_{\pi,\mathrm{wave}}(x)
=
\sum_{2\le n\le x}
\operatorname{sinc}
\left(
\sum_{m=2}^{n-1}
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
\right).
\]
```

Therefore:

```latex
\[
\boxed{
B_{\pi,\mathrm{wave}}(x)=\pi(x)
}
\]
```

## Equivalent Product Indicator

The sinc step can also be replaced by the Bach product indicator:

```latex
\[
Q_{\mathrm{wave}}(n)
=
\prod_{m=2}^{n-1}
\left(1-W_m(n)\right).
\]
```

Expanded:

```latex
\[
Q_{\mathrm{wave}}(n)
=
\prod_{m=2}^{n-1}
\left(
1-
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
\right).
\]
```

This is the same wave-only prime indicator: it equals `1` at primes and `0` at
composites.

The accompanying Python module `bach_wave_prime_functions.py` implements these
literal formulas. It is meant as a faithful wave construction rather than an
efficient prime-counting algorithm.
