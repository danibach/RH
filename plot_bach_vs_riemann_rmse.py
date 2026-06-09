"""
Compare Bach's exact prime-counting curve with finite-zero Riemann curves.

The script computes:

    B_pi(x) = pi(x)

from the exact Bach prime detector, implemented efficiently as a sieve, and
compares it with R_RH,N(x), the Riemann explicit-formula approximation using
the first N positive critical-line zeros:

    rho = 1/2 + i gamma.

By default it compares N = 5 and N = 50 zeros, prints RMSE values, and plots:

    1. Exact Bach/pi(x) curve versus Riemann finite-zero curves
    2. Error curves B_pi(x) - R_RH,N(x)
    3. Bar chart of RMSE values

Python: 3.9+
Dependencies:
    pip install matplotlib mpmath scipy

VS Code/Jupyter note:
    This uses parse_known_args(), so it ignores hidden Jupyter arguments like
    --f=/.../kernel.json.
"""

import argparse
import math
import os
import sys

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib-cache"))

if "--save" in sys.argv:
    import matplotlib

    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import mpmath as mp

try:
    from scipy.special import expi as scipy_expi
except ImportError:
    scipy_expi = None


DEFAULT_X_MAX = 1000
ZERO_COUNTS = (5, 50)
SAMPLE_OFFSET = 0.5


def mobius(n):
    """Return the Mobius function mu(n)."""
    if n == 1:
        return 1

    result = 1
    remaining = n
    p = 2

    while p * p <= remaining:
        if remaining % p == 0:
            remaining //= p
            result *= -1

            if remaining % p == 0:
                return 0

            while remaining % p == 0:
                remaining //= p

        p += 1 if p == 2 else 2

    if remaining > 1:
        result *= -1

    return result


def prime_counts_up_to(limit):
    """
    Return pi(n) for n = 0, 1, ..., limit.

    This is the efficient computational version of the Bach detector:
    B(n)=0 exactly at primes, so counting those zeros gives pi(n).
    """
    if limit < 2:
        return [0] * (limit + 1)

    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False

    counts = []
    running = 0
    for n in range(limit + 1):
        if is_prime[n]:
            running += 1
        counts.append(running)

    return counts


def first_positive_zeta_gammas(count):
    """Return the first `count` positive imaginary parts gamma of zeta zeros."""
    return [float(mp.im(mp.zetazero(i))) for i in range(1, count + 1)]


def expi(z):
    """Fast exponential integral Ei(z), using SciPy when available."""
    if scipy_expi is not None:
        return scipy_expi(z)

    return complex(mp.ei(z))


def trivial_zero_correction(y, max_terms=40, tolerance=1e-30):
    """
    Compute the correction from the trivial zeros.

    In Riemann's J(x) formula:

        integral_y^infinity dt / (t(t^2-1)log(t))

    equals:

        -sum_{r>=1} Li(y^(-2r)).

    This series converges quickly for y >= 2.
    """
    total = 0.0
    log_y = math.log(float(y))

    for r in range(1, max_terms + 1):
        term = -expi(-2 * r * log_y).real
        total += float(term)

        if abs(term) < tolerance:
            break

    return total


def riemann_J_finite(y, gammas):
    """
    Approximate Riemann's prime-power counting function J(y) using finite zeros.
    """
    y = float(y)
    log_y = math.log(y)

    total = float(expi(log_y).real)

    for gamma in gammas:
        rho = complex(0.5, gamma)
        # In the explicit formula, Li(y^rho) is understood as Ei(rho log y).
        # Calling li(exp(rho log y)) would use the principal logarithm after
        # wrapping around the complex plane, which gives the wrong branch.
        total -= 2 * expi(rho * log_y).real

    total -= math.log(2)
    total += trivial_zero_correction(y)

    return total


def riemann_pi_finite(x, gammas):
    """
    Approximate pi(x) by Mobius-inverting finite-zero approximations to J(x).
    """
    x = float(x)
    total = 0.0
    max_k = int(math.floor(math.log(x, 2)))

    for k in range(1, max_k + 1):
        mu_k = mobius(k)
        if mu_k == 0:
            continue

        y = x ** (1.0 / k)
        total += mu_k / k * riemann_J_finite(y, gammas)

    return float(total)


def rmse(exact_values, approximate_values):
    total = 0.0

    for exact, approximate in zip(exact_values, approximate_values):
        total += (exact - approximate) ** 2

    return math.sqrt(total / len(exact_values))


def main():
    parser = argparse.ArgumentParser(
        description="Plot Bach/pi(x) against finite-zero Riemann approximations."
    )
    parser.add_argument(
        "--x-max",
        type=int,
        default=DEFAULT_X_MAX,
        help=f"Largest integer n to sample. Default: {DEFAULT_X_MAX}",
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional image output path, for example bach_vs_riemann_rmse.png",
    )
    args, _unknown_args = parser.parse_known_args()

    if args.x_max < 10:
        raise ValueError("--x-max must be at least 10")

    mp.mp.dps = 30

    print(f"Building exact Bach/pi(x) curve up to x = {args.x_max}...")
    pi_counts = prime_counts_up_to(args.x_max)

    sample_ns = list(range(2, args.x_max + 1))
    sample_xs = [n + SAMPLE_OFFSET for n in sample_ns]
    exact_values = [pi_counts[n] for n in sample_ns]

    max_zero_count = max(ZERO_COUNTS)
    print(f"Computing first {max_zero_count} zeta zeros on the critical line...")
    all_gammas = first_positive_zeta_gammas(max_zero_count)

    approximations = {}
    errors = {}
    rmses = {}

    for zero_count in ZERO_COUNTS:
        gammas = all_gammas[:zero_count]
        print(f"Computing R_RH,{zero_count}(x)...")

        approx_values = [riemann_pi_finite(x, gammas) for x in sample_xs]
        approximations[zero_count] = approx_values
        errors[zero_count] = [
            exact - approximate
            for exact, approximate in zip(exact_values, approx_values)
        ]
        rmses[zero_count] = rmse(exact_values, approx_values)

    print()
    print(f"RMSE over sample points x = n + {SAMPLE_OFFSET}, n = 2,...,{args.x_max}")
    print("-" * 58)
    for zero_count in ZERO_COUNTS:
        print(f"{zero_count:>3} zeros: RMSE = {rmses[zero_count]:.6f}")

    fig, axes = plt.subplots(3, 1, figsize=(13, 12), sharex=True)

    axes[0].step(
        sample_xs,
        exact_values,
        where="post",
        color="black",
        linewidth=2,
        label="Bach exact pi(x)",
    )

    colors = {5: "royalblue", 50: "crimson"}
    for zero_count in ZERO_COUNTS:
        axes[0].plot(
            sample_xs,
            approximations[zero_count],
            color=colors.get(zero_count),
            linewidth=1.6,
            label=f"R_RH(x), {zero_count} zeros",
        )

    axes[0].set_title("Bach Exact Prime Count vs Finite-Zero Riemann Curves")
    axes[0].set_ylabel("prime count")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    for zero_count in ZERO_COUNTS:
        axes[1].plot(
            sample_xs,
            errors[zero_count],
            color=colors.get(zero_count),
            linewidth=1.4,
            label=f"B_pi(x) - R_RH,{zero_count}(x)",
        )

    axes[1].axhline(0, color="black", linewidth=1)
    axes[1].set_title("Error Curves")
    axes[1].set_ylabel("error")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    bar_labels = [str(zero_count) for zero_count in ZERO_COUNTS]
    bar_values = [rmses[zero_count] for zero_count in ZERO_COUNTS]
    bar_colors = [colors.get(zero_count) for zero_count in ZERO_COUNTS]

    axes[2].bar(bar_labels, bar_values, color=bar_colors)
    axes[2].set_title("RMSE")
    axes[2].set_xlabel("number of critical-line zeros used")
    axes[2].set_ylabel("RMSE")
    axes[2].grid(True, axis="y", alpha=0.3)

    for label, value in zip(bar_labels, bar_values):
        axes[2].text(label, value, f"{value:.3f}", ha="center", va="bottom")

    plt.xlabel("x")
    plt.tight_layout()

    if args.save:
        plt.savefig(args.save, dpi=180)
        print(f"\nSaved plot to {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
