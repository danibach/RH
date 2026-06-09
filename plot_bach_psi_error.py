"""
Plot the Bach-derived Chebyshev psi error.

The Bach prime indicator Q_B(n) is exact:

    Q_B(n) = 1 if n is prime, 0 otherwise.

From it, define the Bach-derived Chebyshev function:

    psi_B(x) = sum_{k >= 1} sum_{2 <= n <= x^(1/k)} Q_B(n) log(n)

Since Q_B selects primes, this is exactly:

    psi_B(x) = sum_{p^k <= x} log(p) = psi(x).

The RH-equivalent target is:

    psi_B(x) - x = O(sqrt(x) log^2(x)).

This script plots psi_B(x), psi_B(x)-x, and the normalized error

    (psi_B(x)-x) / (sqrt(x) log^2(x)).

Python: 3.9+
Dependencies:
    pip install matplotlib
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


def bach_prime_flags(limit):
    """
    Return Q_B(n) for n = 0, 1, ..., limit.

    This is the efficient exact implementation of Bach's prime indicator:
    Q_B(n)=1 iff Bach's divisor wave has no proper divisor contribution.
    """
    if limit < 2:
        return [False] * (limit + 1)

    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False

    return is_prime


def bach_lambda_values(limit):
    """
    Return Lambda_B(n) for n = 0, 1, ..., limit.

    Lambda_B(p^k)=log(p), and Lambda_B(n)=0 otherwise. It is derived from
    Bach's prime indicator by adding log(p) to every prime power p^k.
    """
    is_prime = bach_prime_flags(limit)
    lambda_values = [0.0] * (limit + 1)

    for p in range(2, limit + 1):
        if not is_prime[p]:
            continue

        log_p = math.log(p)
        power = p

        while power <= limit:
            lambda_values[power] = log_p
            power *= p

    return lambda_values


def cumulative(values):
    running = 0.0
    totals = []

    for value in values:
        running += value
        totals.append(running)

    return totals


def sampled_indices(limit, max_points):
    """
    Keep plots responsive for very large limits while preserving endpoints.
    """
    if limit <= max_points:
        return list(range(2, limit + 1))

    step = max(1, limit // max_points)
    indices = list(range(2, limit + 1, step))

    if indices[-1] != limit:
        indices.append(limit)

    return indices


def main():
    parser = argparse.ArgumentParser(
        description="Plot psi_B(x)-x and its RH-scale normalized error."
    )
    parser.add_argument(
        "--x-max",
        type=int,
        default=100000,
        help="Largest integer x-value to sample. Default: 100000",
    )
    parser.add_argument(
        "--max-points",
        type=int,
        default=20000,
        help="Maximum plotted points for large x ranges. Default: 20000",
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional output path, for example bach_psi_error.png",
    )
    args, _unknown_args = parser.parse_known_args()

    if args.x_max < 3:
        raise ValueError("--x-max must be at least 3")

    print(f"Building Lambda_B and psi_B up to x = {args.x_max}...")

    lambda_values = bach_lambda_values(args.x_max)
    psi_values = cumulative(lambda_values)

    xs = sampled_indices(args.x_max, args.max_points)
    psi_sample = [psi_values[x] for x in xs]
    error_sample = [psi_values[x] - x for x in xs]
    normalized_error = [
        (psi_values[x] - x) / (math.sqrt(x) * math.log(x) ** 2)
        for x in xs
    ]

    final_error = psi_values[args.x_max] - args.x_max
    final_scale = math.sqrt(args.x_max) * math.log(args.x_max) ** 2
    max_abs_normalized = max(abs(value) for value in normalized_error)

    fig, axes = plt.subplots(3, 1, figsize=(13, 12), sharex=True)

    axes[0].plot(xs, psi_sample, linewidth=1.6, label=r"$\psi_B(x)=\psi(x)$")
    axes[0].plot(xs, xs, color="black", linewidth=1.0, alpha=0.75, label=r"$x$")
    axes[0].set_title("Bach-Derived Chebyshev Function")
    axes[0].set_ylabel("value")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(xs, error_sample, color="crimson", linewidth=1.4, label=r"$\psi_B(x)-x$")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title("Error Term")
    axes[1].set_ylabel("error")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    axes[2].plot(
        xs,
        normalized_error,
        color="darkgreen",
        linewidth=1.4,
        label=r"$(\psi_B(x)-x)/(\sqrt{x}\log^2 x)$",
    )
    axes[2].axhline(0, color="black", linewidth=0.8)
    axes[2].set_title("RH-Scale Normalized Error")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("normalized error")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()

    if args.save:
        plt.savefig(args.save, dpi=180)
        print(f"Saved plot to {args.save}")
    else:
        plt.show()

    print(f"psi_B({args.x_max}) = {psi_values[args.x_max]:.8f}")
    print(f"psi_B({args.x_max}) - {args.x_max} = {final_error:.8f}")
    print(f"sqrt(x) log^2(x) at x={args.x_max} = {final_scale:.8f}")
    print(f"normalized final error = {final_error / final_scale:.8f}")
    print(f"max absolute normalized error on plotted samples = {max_abs_normalized:.8f}")


if __name__ == "__main__":
    main()
