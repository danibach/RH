"""
Plot finite Bach prime-zeta partial sums in the complex s-plane.

The target expression is

    P_B(s) =
        sum_{n=2}^infinity n^{-s}
        product_{m=2}^{n-1}
        (
            1 - (1/m) sum_{r=0}^{m-1} exp(2*pi*i*r*n/m)
        ).

At integer n, the inner roots-of-unity average is 1 when m divides n and 0
otherwise. Therefore the product is exactly the Bach prime indicator Q_B(n).
For computation, this script uses the equivalent exact sieve form:

    P_{B,N}(s) = sum_{2 <= n <= N} Q_B(n)n^{-s}
               = sum_{p <= N} p^{-s}.

Important: a finite partial sum is an entire function, so this plot cannot
prove or disprove singularities. It visualizes the finite Bach prime-zeta
surface and marks the RH singularity-exclusion region Re(s)>1/2, with the
expected singular point at s=1.

Python: 3.9+
Dependencies:
    pip install matplotlib numpy

Example:
    python3 plot_bach_prime_zeta_singularity.py --n-max 5000 --save bach_prime_zeta_singularity.png
"""

import argparse
import cmath
import math
import os
import sys

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib-cache"))

if "--save" in sys.argv:
    import matplotlib

    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def divisibility_wave_literal(m, n):
    """
    Literal roots-of-unity divisor detector:

        D_m(n) = (1/m) sum_{r=0}^{m-1} exp(2*pi*i*r*n/m).

    Mathematically this equals 1 if m divides n and 0 otherwise. Numerically,
    non-divisors may leave tiny floating-point noise near 0.
    """
    total = 0j

    for r in range(m):
        total += cmath.exp(2j * math.pi * r * n / m)

    return total / m


def bach_prime_indicator_literal(n, tolerance=1e-8):
    """
    Direct numerical version of the selected Bach product.

    This mirrors the algebraic formula exactly, but it is intentionally kept
    for small checks because it is much slower than the sieve version.
    """
    if n < 2:
        return 0

    product = 1 + 0j

    for m in range(2, n):
        product *= 1 - divisibility_wave_literal(m, n)

    return 1 if abs(product - 1) < tolerance else 0


def bach_prime_flags(limit):
    """
    Return Q_B(n) for n = 0, 1, ..., limit.

    This is the efficient exact implementation of the Bach product:
    Q_B(n)=1 iff no integer m with 2 <= m < n divides n.
    """
    if limit < 2:
        return np.zeros(limit + 1, dtype=bool)

    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False

    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            is_prime[p * p : limit + 1 : p] = False

    return is_prime


def primes_up_to(limit):
    flags = bach_prime_flags(limit)
    return np.flatnonzero(flags).astype(float)


def bach_prime_zeta_partial_grid(sigmas, ts, primes):
    """
    Evaluate P_{B,N}(sigma + it) = sum_{p <= N} p^(-sigma-it).
    """
    log_primes = np.log(primes)
    values = np.empty((len(ts), len(sigmas)), dtype=np.complex128)

    for row, t in enumerate(ts):
        s_values = sigmas + 1j * t
        values[row, :] = np.exp(-np.outer(log_primes, s_values)).sum(axis=0)

    return values


def bach_prime_zeta_partial_line(sigmas, primes):
    """
    Evaluate P_{B,N}(sigma) along the real axis t=0.
    """
    return np.power(primes[:, None], -sigmas[None, :]).sum(axis=0)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Plot finite Bach prime-zeta partial sums over s=sigma+it and "
            "mark the RH singularity-exclusion region."
        )
    )
    parser.add_argument(
        "--n-max",
        type=int,
        default=5000,
        help="Prime/Bach cutoff N in P_{B,N}(s). Default: 5000.",
    )
    parser.add_argument(
        "--sigma-min",
        type=float,
        default=0.35,
        help="Minimum real part sigma for the heatmap. Default: 0.35.",
    )
    parser.add_argument(
        "--sigma-max",
        type=float,
        default=1.6,
        help="Maximum real part sigma for the heatmap. Default: 1.6.",
    )
    parser.add_argument(
        "--t-max",
        type=float,
        default=35.0,
        help="Plot -t_max <= Im(s) <= t_max. Default: 35.",
    )
    parser.add_argument(
        "--sigma-points",
        type=int,
        default=260,
        help="Number of sigma samples. Default: 260.",
    )
    parser.add_argument(
        "--t-points",
        type=int,
        default=260,
        help="Number of t samples. Default: 260.",
    )
    parser.add_argument(
        "--line-cutoffs",
        default="100,1000,5000",
        help=(
            "Comma-separated N values for the real-axis comparison panel. "
            "Default: 100,1000,5000."
        ),
    )
    parser.add_argument(
        "--literal-check",
        type=int,
        default=0,
        help=(
            "If positive, compare the literal Bach product against the sieve "
            "for n=2,...,literal_check before plotting."
        ),
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional image output path, for example bach_prime_zeta_singularity.png.",
    )
    return parser.parse_args()


def parse_cutoffs(raw_cutoffs, n_max):
    cutoffs = []

    for piece in raw_cutoffs.split(","):
        piece = piece.strip()
        if not piece:
            continue
        value = int(piece)
        if value >= 2:
            cutoffs.append(min(value, n_max))

    if n_max not in cutoffs:
        cutoffs.append(n_max)

    return sorted(set(cutoffs))


def run_literal_check(limit):
    flags = bach_prime_flags(limit)

    for n in range(2, limit + 1):
        literal = bach_prime_indicator_literal(n)
        exact = int(flags[n])

        if literal != exact:
            raise AssertionError(
                f"literal Bach product mismatch at n={n}: {literal} != {exact}"
            )

    print(f"Literal Bach product check passed for n = 2,...,{limit}.")


def main():
    args = parse_args()

    if args.n_max < 2:
        raise ValueError("--n-max must be at least 2")
    if args.sigma_max <= args.sigma_min:
        raise ValueError("--sigma-max must be greater than --sigma-min")
    if args.t_max <= 0:
        raise ValueError("--t-max must be positive")
    if args.sigma_points < 20 or args.t_points < 20:
        raise ValueError("--sigma-points and --t-points must be at least 20")

    if args.literal_check > 0:
        if args.literal_check > 120:
            raise ValueError("--literal-check is slow; use 120 or less")
        run_literal_check(args.literal_check)

    primes = primes_up_to(args.n_max)
    if len(primes) == 0:
        raise ValueError("No primes found for the requested --n-max")

    sigmas = np.linspace(args.sigma_min, args.sigma_max, args.sigma_points)
    ts = np.linspace(-args.t_max, args.t_max, args.t_points)

    print(f"Evaluating P_B,N(s) with N={args.n_max} and {len(primes)} primes...")
    values = bach_prime_zeta_partial_grid(sigmas, ts, primes)
    magnitude = np.abs(values)
    heat_values = np.log10(1 + magnitude)

    line_sigmas = np.linspace(max(0.05, args.sigma_min), args.sigma_max, 500)
    cutoffs = parse_cutoffs(args.line_cutoffs, args.n_max)

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(15, 6.8),
        gridspec_kw={"width_ratios": [1.24, 1.0]},
    )

    heatmap = axes[0].imshow(
        heat_values,
        extent=[args.sigma_min, args.sigma_max, -args.t_max, args.t_max],
        origin="lower",
        aspect="auto",
        cmap="viridis",
    )
    axes[0].axvline(0.5, color="white", linewidth=1.7, linestyle="--", label=r"$\Re(s)=1/2$")
    axes[0].axvline(1.0, color="crimson", linewidth=1.4, alpha=0.9)
    axes[0].scatter([1.0], [0.0], color="crimson", s=60, zorder=4, label=r"$s=1$")
    axes[0].set_title(r"Finite Bach prime-zeta surface $\log_{10}(1+|P_{B,N}(s)|)$")
    axes[0].set_xlabel(r"$\sigma=\Re(s)$")
    axes[0].set_ylabel(r"$t=\Im(s)$")
    axes[0].legend(loc="upper right")
    axes[0].grid(False)

    colorbar = fig.colorbar(heatmap, ax=axes[0], fraction=0.046, pad=0.04)
    colorbar.set_label(r"$\log_{10}(1+|P_{B,N}(s)|)$")

    for cutoff in cutoffs:
        cutoff_primes = primes[primes <= cutoff]
        line_values = bach_prime_zeta_partial_line(line_sigmas, cutoff_primes)
        axes[1].plot(
            line_sigmas,
            line_values.real,
            linewidth=1.6,
            label=fr"$N={cutoff}$",
        )

    axes[1].axvline(0.5, color="gray", linewidth=1.3, linestyle="--")
    axes[1].axvline(1.0, color="crimson", linewidth=1.3)
    axes[1].set_title(r"Real-axis growth of $P_{B,N}(\sigma)$")
    axes[1].set_xlabel(r"$\sigma$")
    axes[1].set_ylabel(r"$P_{B,N}(\sigma)$")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    fig.suptitle(
        (
            r"$P_{B,N}(s)=\sum_{n=2}^{N}n^{-s}"
            r"\prod_{m=2}^{n-1}\left(1-D_m(n)\right)"
            rf"=\sum_{{p\leq {args.n_max}}}p^{{-s}}$"
        ),
        fontsize=14,
        y=0.98,
    )
    fig.text(
        0.5,
        0.02,
        (
            "Finite partial sums are entire; the infinite singularity target is "
            "Re(s)>1/2 with only the expected singularity at s=1."
        ),
        ha="center",
        fontsize=10,
    )
    plt.tight_layout(rect=[0, 0.05, 1, 0.93])

    if args.save:
        plt.savefig(args.save, dpi=180)
        print(f"Saved plot to {args.save}")
    else:
        plt.show()

    print(f"N = {args.n_max}")
    print(f"number of Bach-selected primes = {len(primes)}")
    print(f"sigma range = [{args.sigma_min}, {args.sigma_max}]")
    print(f"t range = [{-args.t_max}, {args.t_max}]")


if __name__ == "__main__":
    main()
