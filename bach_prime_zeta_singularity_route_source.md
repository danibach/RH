# Bach Prime-Zeta Singularity Route to RH

## Bach Prime Indicator

Let `B(n)` be Bach's divisor wave:

```latex
B(n)=
\sum_{m=2}^{n-1}
\frac{1}{m}
\sum_{r=0}^{m-1}
e^{2\pi i r n/m}.
```

For integer `n >= 2`, this counts the proper divisors of `n`, excluding `1`
and `n`:

```latex
B(n)=d(n)-2.
```

Therefore:

```latex
B(n)=0 \iff n \text{ is prime}.
```

Using normalized sinc,

```latex
\operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x},
\qquad
\operatorname{sinc}(0)=1,
```

the Bach prime indicator is:

```latex
I_B(n)=\operatorname{sinc}(B(n)).
```

For integer `n >= 2`:

```latex
I_B(n)=
\begin{cases}
1, & n \text{ prime},\\
0, & n \text{ composite}.
\end{cases}
```

## Prime-Zeta Transform

Define the Dirichlet transform:

```latex
P_B(s)=
\sum_{n=2}^{\infty}
\frac{I_B(n)}{n^s}.
```

For `Re(s)>1`, only prime inputs survive:

```latex
P_B(s)=
\sum_p p^{-s}.
```

Thus `P_B(s)` is the prime zeta function.

## Relation to Riemann Zeta

For `Re(s)>1`, Euler's product gives:

```latex
\log \zeta(s)
=
\sum_p \sum_{k=1}^{\infty}\frac{p^{-ks}}{k}
=
\sum_{k=1}^{\infty}\frac{1}{k}P_B(ks).
```

Möbius inversion yields:

```latex
P_B(s)=
\sum_{k=1}^{\infty}
\frac{\mu(k)}{k}
\log\zeta(ks).
```

This identity provides the analytic continuation of `P_B(s)`, with logarithmic
singularities inherited from the pole and zeros of `zeta`.

## Singularity Target

The RH-equivalent target is:

```latex
\boxed{
P_B(s)
\text{ has no singularities in }
\operatorname{Re}(s)>1/2
\text{ except at }s=1.
}
```

## Why This Is RH-Equivalent

The singularities of `P_B(s)` arise from:

```latex
\log \zeta(ks).
```

The pole of `zeta` at `1` creates singularities at:

```latex
s=\frac{1}{k}.
```

Only `k=1` lies in the open half-plane `Re(s)>1/2`, giving the singularity at
`s=1`.

A nontrivial zero `rho` of `zeta` creates a logarithmic singularity at:

```latex
s=\frac{\rho}{k}.
```

If RH is true, then every nontrivial zero has:

```latex
\operatorname{Re}(\rho)=1/2.
```

Thus all zero-generated singularities satisfy:

```latex
\operatorname{Re}(\rho/k)\le 1/2,
```

so none lie inside `Re(s)>1/2`.

Conversely, suppose `zeta` had a nontrivial zero `rho` with:

```latex
\operatorname{Re}(\rho)>1/2.
```

Then the `k=1` term,

```latex
\log\zeta(s),
```

would create a logarithmic singularity of `P_B(s)` at:

```latex
s=\rho.
```

For `k>=2`, `Re(k rho)>1`, where `zeta` has no zeros. Therefore this
singularity cannot be cancelled by another term in the Möbius sum.

So absence of singularities in `Re(s)>1/2`, except at `s=1`, rules out all
zeros with real part greater than `1/2`.

By the functional equation symmetry of zeta zeros, ruling out zeros with real
part greater than `1/2` also rules out zeros with real part less than `1/2`.
Therefore all nontrivial zeros must lie on the critical line.

Hence the singularity target is equivalent to RH.

## What Remains To Prove

Using the identity

```latex
P_B(s)=
\sum_{k=1}^{\infty}
\frac{\mu(k)}{k}
\log\zeta(ks)
```

shows the equivalence, but does not prove RH.

To prove RH through the Bach route, one would need to prove the singularity
exclusion directly from the Bach representation:

```latex
P_B(s)=
\sum_{n=2}^{\infty}
\frac{\operatorname{sinc}(B(n))}{n^s},
```

or from the internal root-of-unity structure of `B(n)`, without assuming the
desired analytic behavior of `zeta`.

That is the central proof obligation of this route.
