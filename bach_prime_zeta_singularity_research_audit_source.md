# Bach Prime-Zeta Singularity Route: Research Audit

This note audits the prime-zeta singularity route toward RH from the Bach
wave-prime construction. It separates what is already proven from the missing
RH-strength step.

## 1. Starting Object

Let the Bach divisor-wave sum be:

```latex
\[
B(n)
=
\sum_{m=2}^{n-1}
\frac{1}{m}
\sum_{r=0}^{m-1}
e^{2\pi i r n/m}.
\]
```

At integer `n >= 2`:

```latex
\[
B(n)=d(n)-2.
\]
```

Thus:

```latex
\[
B(n)=0
\iff
n \text{ is prime}.
\]
```

Using:

```latex
\[
\operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x},
\qquad
\operatorname{sinc}(0)=1,
\]
```

define:

```latex
\[
I_B(n)=\operatorname{sinc}(B(n)).
\]
```

Then `I_B(n)` is exactly the prime indicator:

```latex
\[
I_B(n)=
\begin{cases}
1, & n \text{ prime},\\
0, & n \text{ composite}.
\end{cases}
\]
```

## 2. Prime-Zeta Transform

Define the Bach prime-zeta transform:

```latex
\[
P_B(s)
=
\sum_{n=2}^{\infty}
\frac{I_B(n)}{n^s}.
\]
```

For `Re(s)>1`, this is:

```latex
\[
P_B(s)=\sum_p p^{-s}.
\]
```

So `P_B(s)` is the classical prime zeta function, but reached through the
Bach wave prime indicator.

## 3. Known Zeta Relation

For `Re(s)>1`:

```latex
\[
\log\zeta(s)
=
\sum_{k=1}^{\infty}
\frac{1}{k}P_B(ks).
\]
```

Möbius inversion gives:

```latex
\[
P_B(s)
=
\sum_{k=1}^{\infty}
\frac{\mu(k)}{k}
\log\zeta(ks).
\]
```

This identity is the standard analytic bridge from the Bach prime selector to
the Riemann zeta function.

## 4. RH-Equivalent Singularity Target

The target is:

```latex
\[
\boxed{
P_B(s)
\text{ has no singularities in }
\operatorname{Re}(s)>\frac12
\text{ except at }s=1.
}
\]
```

This is RH-equivalent.

### Reason

The Möbius inversion formula shows that singularities of `P_B(s)` come from:

```latex
\[
\log\zeta(ks).
\]
```

The pole of `zeta` at `1` creates singularities at:

```latex
\[
s=\frac{1}{k}.
\]
```

Only `k=1` lies in `Re(s)>1/2`, giving the expected singularity at `s=1`.

A nontrivial zero `rho` of `zeta` creates a logarithmic singularity at:

```latex
\[
s=\frac{\rho}{k}.
\]
```

If RH is true, then `Re(rho)=1/2`, so all zero-generated singularities satisfy
`Re(rho/k)<=1/2`. Thus none appear inside `Re(s)>1/2`.

Conversely, if there is a zero `rho` with `Re(rho)>1/2`, then the `k=1` term
creates a singularity of `P_B(s)` at `s=rho`. For `k>=2`, `Re(k rho)>1`, where
`zeta` has no zeros, so this singularity cannot be cancelled by higher terms.
Thus singularity exclusion in `Re(s)>1/2` rules out all zeros to the right of
the critical line. By the functional equation symmetry, this is equivalent to
RH.

## 5. What This Route Already Achieves

The Bach prime-zeta route already gives:

1. An exact wave-built prime selector `I_B(n)`.
2. A Dirichlet transform that is exactly the prime zeta function.
3. A precise RH-equivalent analytic target.
4. A concrete instruction for a proof: obtain the singularity exclusion from
   the internal Bach wave structure, not by importing the zeta-zero theorem one
   wants to prove.

This is a valid reformulation of RH. It is not yet a proof.

## 6. Main Missing Step

The missing step is:

```latex
\[
\text{prove directly from }
I_B(n)=\operatorname{sinc}(B(n))
\text{ that }P_B(s)
\text{ continues without singularities in }
\operatorname{Re}(s)>\frac12,
\ s\ne1.
\]
```

Equivalently, prove enough cancellation in:

```latex
\[
\sum_{n\le x} I_B(n)
\quad\text{or}\quad
\sum_{N\le x}\Lambda_B(N)
\]
```

to reach an RH-strength error term.

## 7. Three Direct Bach Attacks And Their Obstacles

### A. Fourier Integral Of The Zero Detector

Because `B(n)` is integer-valued:

```latex
\[
\operatorname{sinc}(B(n))
=
\int_{-1/2}^{1/2}
e^{2\pi i t B(n)}\,dt.
\]
```

This gives:

```latex
\[
P_B(s)
=
\int_{-1/2}^{1/2}
e^{-4\pi i t}
\sum_{n=2}^{\infty}
\frac{e^{2\pi i t d(n)}}{n^s}
\,dt.
\]
```

Obstacle: `d(n)` is multiplicative, but `e^{2\pi i t d(n)}` is not
multiplicative in general. The inner Dirichlet series does not have a simple
Euler product.

### B. Sinc Moment Expansion

The expansion:

```latex
\[
\operatorname{sinc}(x)
=
\sum_{j=0}^{\infty}
\frac{(-1)^j\pi^{2j}x^{2j}}{(2j+1)!}
\]
```

formally gives:

```latex
\[
P_B(s)
=
\sum_{j=0}^{\infty}
\frac{(-1)^j\pi^{2j}}{(2j+1)!}
\sum_{n=2}^{\infty}
\frac{(d(n)-2)^{2j}}{n^s}.
\]
```

For each fixed power, the Dirichlet series has structured Euler products and
controlled singularities.

Obstacle: proving locally uniform convergence after summing over all powers is
not available by naive bounds. The factors grow too quickly. The missing
uniform estimate is effectively RH-strength.

### C. LCM Inclusion-Exclusion Expansion

The product form:

```latex
\[
I_B(n)
=
\prod_{m=2}^{n-1}(1-D_m(n))
\]
```

expands into LCM-indexed waves because:

```latex
\[
D_a(n)D_b(n)=D_{\operatorname{lcm}(a,b)}(n)
\]
```

at integer inputs.

Each fixed inclusion-exclusion set contributes a Hurwitz-zeta type term after
Dirichlet transformation, with only the expected pole at `s=1`.

Obstacle: the outer inclusion-exclusion sum is enormous and alternating.
Absolute convergence fails. A correct grouping with locally uniform convergence
in `Re(s)>1/2`, away from `s=1`, is not currently proven.

## 8. Most Precise Sufficient Lemma

A direct Bach proof of RH would follow from the following type of lemma.

### Bach Singularity-Exclusion Lemma

For every compact set:

```latex
\[
K\subset\{s:\operatorname{Re}(s)>1/2\}\setminus\{1\},
\]
```

construct a Bach-native expansion of:

```latex
\[
P_B(s)=
\sum_{n=2}^{\infty}
\frac{\operatorname{sinc}(B(n))}{n^s}
\]
```

that converges locally uniformly on `K` to a holomorphic function.

If this lemma is proven without using the RH-equivalent zeta singularity
information, then the singularity target follows and RH follows.

The current notes identify candidate expansions, but not the required locally
uniform convergence estimate.

## 9. Current Assessment

The prime-zeta singularity route is mathematically clean because it turns RH
into a concrete analytic continuation/singularity-exclusion problem for a
wave-built prime transform.

The strongest current path is:

```latex
\[
\text{Bach wave prime indicator}
\to
P_B(s)
\to
\text{prime zeta singularities}
\to
\text{RH-equivalent exclusion region}.
\]
```

The route does not yet bypass the classical difficulty. It relocates the
difficulty into a specific missing estimate: cancellation or locally uniform
convergence for a Bach-native expansion of `P_B(s)` in the half-plane
`Re(s)>1/2`.

That is the object to attack next.

## 10. Numerical Diagnostic

The script `check_bach_prime_zeta_mobius.py` checks the identity:

```latex
\[
P_B(s)
=
\sum_{k=1}^{\infty}
\frac{\mu(k)}{k}\log\zeta(ks)
\]
```

against the direct finite prime sum in the safe region `Re(s)>1`.

Example:

```bash
python3 check_bach_prime_zeta_mobius.py \
  --prime-limit 30000 \
  --k-limit 25 \
  --sigma 1.35 \
  --t 7
```

This also prints diagnostic samples near:

1. the expected singularity at `s=1`,
2. the first critical-line zeta zero approached from `Re(s)>1/2`.

These computations use `zeta` directly and are not evidence for RH. Their
purpose is to verify the analytic bridge and make the singularity mechanism
visible numerically.
