# Bach and Riemann Critical-Line Prime Counting Equation

## Prime Counting Equality

Writing the Bach prime-counting side as `B_pi(x)` and the Riemann
critical-line side as `R_RH(x)`:

```latex
\[
\boxed{
B_\pi(x)=R_{\mathrm{RH}}(x)
}
\]
```

where

```latex
\[
\boxed{
B_\pi(x)=
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

and, assuming RH so that every nontrivial zero is

```latex
\[
\rho=\frac12+i\gamma,
\]
```

we have

```latex
\[
\boxed{
R_{\mathrm{RH}}(x)=
\sum_{k=1}^{\lfloor \log_2 x\rfloor}
\frac{\mu(k)}{k}
\left[
\operatorname{Li}(x^{1/k})
-
2\sum_{\gamma>0}
\Re\left(
\operatorname{Li}
\left(
x^{(1/2+i\gamma)/k}
\right)
\right)
-\log 2
+
\int_{x^{1/k}}^\infty
\frac{dt}{t(t^2-1)\log t}
\right]
}
\]
```

## Interpretation

The left side is the exact Bach-form prime counting function:

```latex
\[
B_\pi(x)=\pi(x).
\]
```

The right side is the Riemann explicit-formula reconstruction of prime
counting using only critical-line nontrivial zeros:

```latex
\[
\rho=\frac12+i\gamma.
\]
```

Thus:

```latex
\[
\boxed{
B_\pi(x)=R_{\mathrm{RH}}(x)
}
\]
```

is an RH-equivalent prime-counting formulation.
