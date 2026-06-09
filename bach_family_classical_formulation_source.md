# Bach Family of Equations in Classical Form

This document records the Bach family of equations in classical mathematical
notation, following the source-note style used throughout this RH project.

Let

```latex
D_m(n)
=
\frac{1}{m}
\sum_{j=0}^{m-1}
e^{2\pi i j n/m}.
```

Then

```latex
D_m(n)=
\begin{cases}
1, & m\mid n,\\
0, & m\nmid n.
\end{cases}
```

| Short name | Classical formulation | Purpose | Principle |
|---|---|---|---|
| Divisor Wave | `\displaystyle D_m(n)=\frac{1}{m}\sum_{j=0}^{m-1}e^{2\pi i j n/m}` | Detects whether `m` divides `n`. | Roots of unity cancel unless divisibility holds. |
| Bach Divisor Count | `\displaystyle B(n)=\sum_{m=2}^{n-1}D_m(n)=d(n)-2` | Counts proper divisors of `n`, excluding `1` and `n`. | Primality is absence of proper divisors. |
| Prime-Zero Criterion | `\displaystyle B(n)=0 \iff n \text{ is prime}` | Identifies primes as zeros of `B(n)`. | A positive integer `n>=2` is prime exactly when it has no proper divisor. |
| Bach Prime Indicator | `\displaystyle Q_B(n)=\prod_{m=2}^{n-1}\left(1-D_m(n)\right)` | Equals `1` for primes and `0` for composites. | The product vanishes as soon as one proper divisor appears. |
| Sinc Prime Indicator | `\displaystyle I_B(n)=\operatorname{sinc}(B(n))`, where `\displaystyle \operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x}` and `\operatorname{sinc}(0)=1` | Gives a compact zero-detector form of the prime indicator. | Since `B(n)` is an integer, sinc kills every nonzero divisor count. |
| Sine-Wave Bach Form | `\displaystyle B_{\sin}(n)=\sum_{m=2}^{n-1}\left(\frac{\sin(\pi n)}{m\sin(\pi n/m)}\right)^2` | Gives a real sine-based version of the divisor detector. | Sine zeros encode integer divisibility through limiting values. |
| Bach Prime Counting Function | `\displaystyle B_\pi(x)=\sum_{2\le n\le x}Q_B(n)` | Counts primes up to `x`. | Sum the exact Bach prime indicator over all integers up to `x`. |
| Exact Prime Counting Identity | `\displaystyle B_\pi(x)=\pi(x)` | Identifies the Bach count with the classical prime-counting function. | `Q_B(n)` is exactly the characteristic function of the primes. |
| Zeta Divisor Bridge | `\displaystyle \sum_{n=2}^{\infty}\frac{B(n)}{n^s}=(\zeta(s)-1)^2` | Connects Bach's divisor count to the Riemann zeta function. | Proper divisor counting is the coefficient sequence of products `ab=n` with `a,b>=2`. |
| Bach Prime-Zeta Function | `\displaystyle P_B(s)=\sum_{n=2}^{\infty}\frac{I_B(n)}{n^s}=\sum_p\frac{1}{p^s}` | Converts Bach prime detection into the prime zeta function. | Only Bach-zero inputs, namely primes, survive the Dirichlet transform. |
| Log-Zeta Relation | `\displaystyle \log\zeta(s)=\sum_{k=1}^{\infty}\frac{1}{k}P_B(ks)` | Links Bach primes to Euler's product for `\zeta(s)`. | The logarithm of the Euler product expands into prime powers. |
| Mobius Inversion Form | `\displaystyle P_B(s)=\sum_{k=1}^{\infty}\frac{\mu(k)}{k}\log\zeta(ks)` | Recovers the prime-zeta function from `\log\zeta`. | Mobius inversion separates prime contributions from prime-power contributions. |
| LCM Correlation Expansion | `\displaystyle Q_B(n)=\sum_{S\subseteq\{2,\ldots,n-1\}}(-1)^{|S|}D_{\operatorname{lcm}(S)}(n)` | Expands the Bach product into inclusion-exclusion correlations. | Products of divisor waves collapse to least-common-multiple divisor waves. |
| Grouped Correlation Form | `\displaystyle Q_B(n)=\sum_q C_n(q)D_q(n)` | Groups Bach correlations by least common multiple. | Terms with the same lcm act through the same divisor wave. |
| Correlation Coefficients | `\displaystyle C_n(q)=\sum_{\substack{S\subseteq\{2,\ldots,n-1\}\\ \operatorname{lcm}(S)=q}}(-1)^{|S|}` | Measures the net inclusion-exclusion weight at divisor-wave frequency `q`. | Alternating subset counts produce sieve-like cancellation. |
| Prime-Sieve Compression | `\displaystyle \prod_{p\le z}(1-D_p(n))=\sum_{d\mid P(z)}\mu(d)D_d(n)`, where `\displaystyle P(z)=\prod_{p\le z}p` | Reduces Bach's product to the classical squarefree sieve. | Composite divisor tests are redundant once prime divisor tests are present. |
| Legendre-Bach Formula | `\displaystyle \Phi(x,z)=\sum_{d\mid P(z)}\mu(d)\left\lfloor\frac{x}{d}\right\rfloor` | Counts integers up to `x` avoiding all prime divisors `<=z`. | Inclusion-exclusion over prime divisors. |
| Exact Legendre Count | `\displaystyle \pi(x)=\pi(\sqrt{x})-1+\Phi(x,\sqrt{x})` | Gives the classical exact prime-counting formula reached from Bach correlations. | After sieving by primes up to `sqrt(x)`, unsieved integers are `1` or primes above `sqrt(x)`. |
| Bach Theta Function | `\displaystyle \theta_B(x)=\sum_{n\le x}Q_B(n)\log n=\sum_{p\le x}\log p` | Gives a weighted prime count. | Weight the exact Bach prime indicator by `\log n`. |
| RH Theta Target | `\displaystyle \theta_B(x)=x+O(\sqrt{x}\log^2 x)` | Gives an RH-equivalent cancellation target. | RH becomes square-root cancellation in the weighted Bach prime count. |
| Bach Von Mangoldt Function | `\displaystyle \Lambda_B(N)=\sum_{\substack{k\ge1\\ n^k=N}}Q_B(n)\log n` | Reconstructs the von Mangoldt function from Bach primes. | Prime powers inherit their weight from the Bach-selected base prime. |
| Von Mangoldt Identity | `\displaystyle \Lambda_B(N)=\Lambda(N)` | Shows Bach-generated prime powers match the classical von Mangoldt weights. | `Q_B(n)` selects exactly primes, so only prime powers contribute. |
| Bach Log-Derivative Transform | `\displaystyle L_B(s)=\sum_{N=1}^{\infty}\frac{\Lambda_B(N)}{N^s}=-\frac{\zeta'(s)}{\zeta(s)}` | Connects the Bach construction to the logarithmic derivative of zeta. | The von Mangoldt Dirichlet series is the zeta logarithmic derivative. |
| Bach Psi Function | `\displaystyle \psi_B(x)=\sum_{N\le x}\Lambda_B(N)=\sum_{p^k\le x}\log p` | Gives the Bach version of Chebyshev's `\psi` function. | Sum Bach-generated von Mangoldt weights up to `x`. |
| RH Psi Target | `\displaystyle \psi_B(x)-x=O(\sqrt{x}\log^2 x)` | Gives another RH-equivalent error bound. | RH is equivalent to square-root scale cancellation in `\psi(x)-x`. |
| Prime-Zeta Singularity Target | `\displaystyle P_B(s)\text{ has no singularities in }\Re(s)>\frac12\text{ except at }s=1` | Gives an RH-equivalent analytic formulation. | Off-critical-line zeta zeros would create forbidden prime-zeta singularities. |
| Sinc Moment Expansion | `\displaystyle P_B(s)\sim\sum_{j=0}^{\infty}\frac{(-1)^j\pi^{2j}}{(2j+1)!}M_{2j}(s)` | Gives a formal moment route toward analyzing `P_B(s)`. | Expand the sinc zero detector into even powers of the divisor count. |
| Divisor Moment Series | `\displaystyle M_q(s)=\sum_{n=2}^{\infty}\frac{(d(n)-2)^q}{n^s}` | Measures powers of the Bach divisor count inside a Dirichlet series. | Fixed divisor moments have structured Euler-product behavior, but the full sinc reconstruction requires extreme cancellation. |

The central classical chain is:

```latex
D_m(n)
\longrightarrow
B(n)
\longrightarrow
Q_B(n)
\longrightarrow
B_\pi(x)=\pi(x)
\longrightarrow
P_B(s)
\longrightarrow
\zeta(s).
```

The RH-facing chain is:

```latex
Q_B(n)
\longrightarrow
\Lambda_B(n)
\longrightarrow
\psi_B(x)
\longrightarrow
\psi_B(x)-x
=
O(\sqrt{x}\log^2 x).
```
