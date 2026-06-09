# Three Wave-Based Prime Functions

This note records the three core wave-based functions:

1. the integer multiple wave,
2. the prime-zero indicator function,
3. the prime counting function built from the prime-zero indicator.

## 1. Integer Multiple Wave

For each integer `m >= 2`, define:

```latex
\[
W_m(n)
=
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}.
\]
```

At integer `n`,

```latex
\[
W_m(n)
=
\begin{cases}
1, & m \mid n,\\
0, & m \nmid n.
\end{cases}
\]
```

Thus `W_m(n)` is a wave-based detector for multiples of `m`.

## 2. Prime-Zero Indicator Function

Define:

```latex
\[
Z(n)
=
\sum_{m=2}^{n-1} W_m(n).
\]
```

Expanded:

```latex
\[
Z(n)
=
\sum_{m=2}^{n-1}
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}.
\]
```

Then:

```latex
\[
Z(n)=0
\iff
n \text{ is prime}.
\]
```

So `Z(n)` is the prime-zero indicator function.

## 3. Prime Counting Function

Convert the zero indicator into a `1`-at-primes indicator using:

```latex
\[
\operatorname{sinc}(x)
=
\frac{\sin(\pi x)}{\pi x},
\qquad
\operatorname{sinc}(0)=1.
\]
```

Then:

```latex
\[
P(n)
=
\operatorname{sinc}(Z(n)).
\]
```

So:

```latex
\[
P(n)
=
\begin{cases}
1, & n \text{ is prime},\\
0, & n \text{ is composite}.
\end{cases}
\]
```

Therefore the prime counting function is:

```latex
\[
\boxed{
\pi(x)
=
\sum_{2\le n\le x}
\operatorname{sinc}
\left(
\sum_{m=2}^{n-1}
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i jn/m}
\right)
}
\]
```

or simply:

```latex
\[
\boxed{
\pi(x)=\sum_{2\le n\le x} P(n).
}
\]
```

# Sine-Based Version Of The Same Three Functions

The same three functions can be written using a real sine-based wave instead
of the complex roots-of-unity wave.

## 1. Sine-Based Integer Multiple Wave

For each integer `m >= 2`, define:

```latex
\[
S_m(n)
=
\left(
\frac{\sin(\pi n)}
{m\sin(\pi n/m)}
\right)^2.
\]
```

At values where both numerator and denominator vanish, use the removable-limit
value. At integer `n`,

```latex
\[
S_m(n)
=
\begin{cases}
1, & m \mid n,\\
0, & m \nmid n.
\end{cases}
\]
```

So `S_m(n)` gives the same integer-sample behavior as `W_m(n)`, but in real
sine-wave form.

## 2. Sine-Based Prime-Zero Function

Define:

```latex
\[
Z_{\sin}(n)
=
\sum_{m=2}^{n-1}S_m(n).
\]
```

Expanded:

```latex
\[
Z_{\sin}(n)
=
\sum_{m=2}^{n-1}
\left(
\frac{\sin(\pi n)}
{m\sin(\pi n/m)}
\right)^2.
\]
```

Then:

```latex
\[
Z_{\sin}(n)=0
\iff
n \text{ is prime}.
\]
```

So primes are still exactly the zero samples.

## 3. Sine-Based Prime Counting Function

Use the same zero-to-one conversion:

```latex
\[
P_{\sin}(n)
=
\operatorname{sinc}\!\left(Z_{\sin}(n)\right),
\]
```

where:

```latex
\[
\operatorname{sinc}(x)
=
\frac{\sin(\pi x)}{\pi x},
\qquad
\operatorname{sinc}(0)=1.
\]
```

Then:

```latex
\[
P_{\sin}(n)
=
\begin{cases}
1, & n \text{ is prime},\\
0, & n \text{ is composite}.
\end{cases}
\]
```

Therefore:

```latex
\[
\boxed{
\pi(x)
=
\sum_{2\le n\le x}
\operatorname{sinc}
\left(
\sum_{m=2}^{n-1}
\left(
\frac{\sin(\pi n)}
{m\sin(\pi n/m)}
\right)^2
\right)
}
\]
```

This keeps the exact same integer behavior as the roots-of-unity version, but
uses only sine waves.
