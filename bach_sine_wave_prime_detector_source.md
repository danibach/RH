# Bach's Formula in Sine-Wave Form

## Prime-Zero Detector

Using the sine-wave form, Bach's prime-zero detector becomes:

```latex
B_{\sin}(n)=
\sum_{m=2}^{n-1}
\left(
\frac{\sin(\pi n)}
{m\sin(\pi n/m)}
\right)^2
```

with the limiting rule:

```latex
\left(
\frac{\sin(\pi n)}
{m\sin(\pi n/m)}
\right)^2
=
1
\quad \text{when } m\mid n
```

So for integers `n >= 2`:

```latex
B_{\sin}(n)=0 \iff n \text{ is prime}
```

## Divisor-Wave Interpretation

This is equivalent to Bach's original formula at integer values, because each sine-wave term is also a divisor detector:

```latex
w_m(n)=
\begin{cases}
1, & m\mid n \\
0, & m\nmid n
\end{cases}
```

Therefore:

```latex
B_{\sin}(n)=
\sum_{m=2}^{n-1} w_m(n)
```

where:

```latex
w_m(n)=
\left(
\frac{\sin(\pi n)}
{m\sin(\pi n/m)}
\right)^2
```

## Real-Valued Extension

For real values `x`, a natural extension is:

```latex
B_{\sin}(x)=
\sum_{m=2}^{\lfloor x\rfloor-1}
\left(
\frac{\sin(\pi x)}
{m\sin(\pi x/m)}
\right)^2
```

At integer points, this gives:

```text
B_sin(2) = 0
B_sin(3) = 0
B_sin(4) = 1
B_sin(5) = 0
B_sin(6) = 2
...
```

Thus, primes are exactly the integer inputs where the output is zero.
