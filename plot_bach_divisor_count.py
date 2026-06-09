"""
Plot the Bach divisor count built from divisor waves.

The divisor wave is

    D_m(n) = (1/m) sum_{j=0}^{m-1} exp(2*pi*i*j*n/m).

At integer n, this equals 1 when m divides n and 0 otherwise. The Bach
divisor count is

    B(n) = sum_{m=2}^{n-1} D_m(n) = d(n) - 2.

This script plots:

    1. The divisor-wave grid D_m(n), with only the terms m < n included.
    2. The resulting Bach divisor count B(n), with prime zeros highlighted.

Python: 3.9+
Dependencies:
    pip install matplotlib numpy

Example:
    python3 plot_bach_divisor_count.py --n-max 120 --save bach_divisor_count.png
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


def divisor_wave_literal(m, n):
    """
    Literal roots-of-unity divisor wave D_m(n).

    Mathematically this is exactly 1 when m divides n and 0 otherwise.
    Floating-point evaluation may leave tiny numerical noise near 0.
    """
    total = 0j

    for j in range(m):
        total += cmath.exp(2j * math.pi * j * n / m)

    return total / m


def divisor_wave_exact(m, n):
    """
    Exact integer value of D_m(n) at integer n.
    """
    return 1 if n % m == 0 else 0


def bach_divisor_count(n):
    """
    Exact Bach divisor count B(n)=sum_{m=2}^{n-1}D_m(n)=d(n)-2.
    """
    if n < 2:
        return 0

    count = 0

    for m in range(2, n):
        if n % m == 0:
            count += 1

    return count


def is_prime(n):
    if n < 2:
        return False

    for candidate in range(2, int(math.sqrt(n)) + 1):
        if n % candidate == 0:
            return False

    return True


def divisor_wave_grid(n_max):
    """
    Build a matrix of D_m(n) values.

    Rows are m=2,...,n_max-1 and columns are n=2,...,n_max. Terms with
    m >= n are outside the Bach sum and are stored as NaN for gray masking.
    """
    rows = np.arange(2, n_max)
    cols = np.arange(2, n_max + 1)
    grid = np.full((len(rows), len(cols)), np.nan)

    for row_index, m in enumerate(rows):
        for col_index, n in enumerate(cols):
            if m < n:
                grid[row_index, col_index] = divisor_wave_exact(m, n)

    return rows, cols, grid


def run_literal_check(limit):
    """
    Check the literal roots-of-unity formula against exact divisibility.
    """
    for n in range(2, limit + 1):
        for m in range(2, n):
            literal = divisor_wave_literal(m, n)
            exact = divisor_wave_exact(m, n)

            if abs(literal - exact) > 1e-8:
                raise AssertionError(
                    f"D_{m}({n}) mismatch: literal={literal}, exact={exact}"
                )

    print(f"Literal divisor-wave check passed for n = 2,...,{limit}.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot B(n)=sum_{m=2}^{n-1}D_m(n)=d(n)-2."
    )
    parser.add_argument(
        "--n-max",
        type=int,
        default=120,
        help="Largest integer n to plot. Default: 120.",
    )
    parser.add_argument(
        "--literal-check",
        type=int,
        default=0,
        help=(
            "If positive, compare the literal roots-of-unity formula against "
            "exact divisibility for n=2,...,literal_check before plotting."
        ),
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional output path, for example bach_divisor_count.png.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.n_max < 3:
        raise ValueError("--n-max must be at least 3")
    if args.literal_check > 120:
        raise ValueError("--literal-check is slow; use 120 or less")

    if args.literal_check > 0:
        run_literal_check(args.literal_check)

    rows, cols, grid = divisor_wave_grid(args.n_max)
    bach_values = np.array([bach_divisor_count(int(n)) for n in cols])
    primes = np.array([n for n in cols if is_prime(int(n))])
    prime_values = np.array([bach_divisor_count(int(n)) for n in primes])

    composites = np.array([n for n in cols if n > 1 and not is_prime(int(n))])
    composite_values = np.array([bach_divisor_count(int(n)) for n in composites])

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(14, 9),
        sharex=True,
        gridspec_kw={"height_ratios": [1.15, 1.0]},
    )

    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("#f1f5f9")

    image = axes[0].imshow(
        grid,
        origin="lower",
        aspect="auto",
        interpolation="nearest",
        extent=[cols[0] - 0.5, cols[-1] + 0.5, rows[0] - 0.5, rows[-1] + 0.5],
        cmap=cmap,
        vmin=0,
        vmax=1,
    )
    axes[0].set_title(r"Divisor waves $D_m(n)$ included in $B(n)$")
    axes[0].set_ylabel(r"divisor-wave index $m$")
    axes[0].grid(False)

    colorbar = fig.colorbar(image, ax=axes[0], fraction=0.025, pad=0.015)
    colorbar.set_ticks([0, 1])
    colorbar.set_ticklabels([r"$m\nmid n$", r"$m\mid n$"])

    axes[1].vlines(cols, 0, bach_values, color="#2563eb", linewidth=1.1, alpha=0.7)
    axes[1].scatter(
        composites,
        composite_values,
        color="#1f2937",
        s=24,
        label=r"composites: $B(n)>0$",
        zorder=3,
    )
    axes[1].scatter(
        primes,
        prime_values,
        color="#dc2626",
        s=34,
        label=r"primes: $B(n)=0$",
        zorder=4,
    )
    axes[1].axhline(0, color="#64748b", linewidth=1)
    axes[1].set_title(r"Bach divisor count $B(n)=\sum_{m=2}^{n-1}D_m(n)=d(n)-2$")
    axes[1].set_xlabel(r"integer $n$")
    axes[1].set_ylabel(r"$B(n)$")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc="upper left")

    fig.suptitle(
        r"Prime-zero structure of the Bach divisor count",
        fontsize=15,
        y=0.985,
    )
    fig.text(
        0.5,
        0.02,
        (
            r"At integer inputs, each $D_m(n)$ is a roots-of-unity divisor "
            r"detector, so $B(n)$ counts proper divisors and vanishes at primes."
        ),
        ha="center",
        fontsize=10,
    )
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    if args.save:
        plt.savefig(args.save, dpi=180)
        print(f"Saved plot to {args.save}")
    else:
        plt.show()

    print(f"n_max = {args.n_max}")
    print(f"prime zeros shown = {len(primes)}")
    print(f"max B(n) on plot = {int(np.max(bach_values))}")


if __name__ == "__main__":
    main()
