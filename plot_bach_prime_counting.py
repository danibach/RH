"""
Plot the Bach-form prime counting function.

This script plots

    pi_B(x) = sum_{2 <= n <= x} product_{m=2}^{n-1}
              (1 - (1/m) * sum_{j=0}^{m-1} exp(2*pi*i*j*n/m))

At integer n, the inner roots-of-unity average is 1 when m divides n
and 0 otherwise. Therefore the product is 1 exactly when n is prime.

Python: 3.9+
Dependencies:
    pip install matplotlib
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


def divisibility_wave(m, n):
    """
    Literal roots-of-unity divisibility detector:

        (1/m) * sum_{j=0}^{m-1} exp(2*pi*i*j*n/m)

    Mathematically this is exactly 1 if m divides n, and exactly 0 otherwise.
    Numerically it may return tiny floating-point noise near 0.
    """
    total = 0j
    for j in range(m):
        total += cmath.exp(2j * math.pi * j * n / m)
    return total / m


def bach_prime_indicator_literal(n, tolerance=1e-8):
    """
    Direct numerical version of the boxed formula's product.

    Returns 1 if the product is numerically near 1, otherwise 0.
    This mirrors the algebraic formula, but it is slower than the exact version.
    """
    if n < 2:
        return 0

    product = 1 + 0j
    for m in range(2, n):
        product *= 1 - divisibility_wave(m, n)

    return 1 if abs(product - 1) < tolerance else 0


def bach_prime_indicator_exact(n):
    """
    Exact integer version of the same Bach product.

    The factor for m is:
        1 - 1 = 0 if m divides n
        1 - 0 = 1 otherwise

    So the product is 1 exactly when no m from 2 to n - 1 divides n.
    """
    if n < 2:
        return 0

    for m in range(2, n):
        if n % m == 0:
            return 0

    return 1


def bach_prime_count_values(limit, use_literal_formula=False):
    """
    Return x-values and pi_B(x)-values for x = 0, 1, ..., limit.
    """
    indicator = (
        bach_prime_indicator_literal
        if use_literal_formula
        else bach_prime_indicator_exact
    )

    xs = list(range(limit + 1))
    counts = []
    running_total = 0

    for n in xs:
        running_total += indicator(n)
        counts.append(running_total)

    return xs, counts


def main():
    parser = argparse.ArgumentParser(
        description="Plot Bach's algebraic prime counting function."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Largest x-value to plot. Default: 100",
    )
    parser.add_argument(
        "--literal",
        action="store_true",
        help=(
            "Use the literal complex roots-of-unity product. "
            "This is slower and intended for small limits."
        ),
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional output path, for example bach_prime_counting.png",
    )
    args, _unknown_args = parser.parse_known_args()

    if args.limit < 2:
        raise ValueError("--limit must be at least 2")

    if args.literal and args.limit > 80:
        print(
            "Warning: --literal is slow for large limits. "
            "Consider using --limit 80 or less."
        )

    xs, counts = bach_prime_count_values(args.limit, args.literal)

    primes_x = []
    primes_y = []
    for x, count in zip(xs, counts):
        if bach_prime_indicator_exact(x):
            primes_x.append(x)
            primes_y.append(count)

    plt.figure(figsize=(11, 6))
    plt.step(xs, counts, where="post", linewidth=2.0, label=r"$\pi_B(x)$")
    plt.scatter(primes_x, primes_y, color="crimson", s=28, zorder=3, label="prime jumps")

    plt.title("Bach-Form Prime Counting Function")
    plt.xlabel("x")
    plt.ylabel(r"$\pi_B(x)$")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    if args.save:
        plt.savefig(args.save, dpi=180)
        print(f"Saved plot to {args.save}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
