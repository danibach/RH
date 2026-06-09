"""
Plot the sine-wave Bach form.

The sine-wave Bach form is

    B_sin(n) =
        sum_{m=2}^{n-1}
        (sin(pi*n) / (m*sin(pi*n/m)))^2.

At integer inputs this is interpreted with the removable-singularity rule:

    (sin(pi*n) / (m*sin(pi*n/m)))^2 = 1  when m divides n,
                                      = 0  otherwise.

So B_sin(n)=d(n)-2 and B_sin(n)=0 exactly at primes.

For real x, this script plots the natural extension

    B_sin(x) =
        sum_{m=2}^{floor(x)-1}
        (sin(pi*x) / (m*sin(pi*x/m)))^2.

Python: 3.9+
Dependencies:
    pip install matplotlib numpy

Example:
    python3 plot_bach_sine_wave_form.py --x-max 80 --save bach_sine_wave_form.png
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
import numpy as np


def is_prime(n):
    if n < 2:
        return False

    for candidate in range(2, int(math.sqrt(n)) + 1):
        if n % candidate == 0:
            return False

    return True


def bach_sine_at_integer(n):
    """
    Exact integer value B_sin(n)=d(n)-2.
    """
    if n < 2:
        return 0

    return sum(1 for m in range(2, n) if n % m == 0)


def sine_divisor_term(m, x, tolerance=1e-12):
    """
    Evaluate one sine-wave divisor term.

    The formula has removable 0/0 values at integer multiples of m. Near those
    points, use the limiting divisor value.
    """
    numerator = np.sin(np.pi * x)
    denominator = m * np.sin(np.pi * x / m)
    term = np.zeros_like(x, dtype=float)

    safe = np.abs(denominator) > tolerance
    term[safe] = (numerator[safe] / denominator[safe]) ** 2

    removable = ~safe
    if np.any(removable):
        nearest_integer = np.rint(x[removable]).astype(int)
        term[removable] = np.where(nearest_integer % m == 0, 1.0, 0.0)

    return term


def bach_sine_real_extension(x):
    """
    Evaluate the real extension of B_sin(x).
    """
    x = np.asarray(x, dtype=float)
    values = np.zeros_like(x, dtype=float)
    max_m = int(math.floor(np.max(x))) - 1

    if max_m < 2:
        return values

    floors = np.floor(x)

    for m in range(2, max_m + 1):
        active = floors >= m + 1
        if np.any(active):
            values[active] += sine_divisor_term(m, x[active])

    return values


def parse_args():
    parser = argparse.ArgumentParser(description="Plot the sine-wave Bach form.")
    parser.add_argument(
        "--x-min",
        type=float,
        default=2.0,
        help="Minimum real x-value. Default: 2.",
    )
    parser.add_argument(
        "--x-max",
        type=float,
        default=80.0,
        help="Maximum real x-value. Default: 80.",
    )
    parser.add_argument(
        "--samples-per-unit",
        type=int,
        default=160,
        help="Real-curve samples per unit interval. Default: 160.",
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional output path, for example bach_sine_wave_form.png.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.x_max <= args.x_min:
        raise ValueError("--x-max must be greater than --x-min")
    if args.x_max < 3:
        raise ValueError("--x-max must be at least 3")
    if args.samples_per_unit < 10:
        raise ValueError("--samples-per-unit must be at least 10")

    sample_count = int((args.x_max - args.x_min) * args.samples_per_unit) + 1
    xs = np.linspace(args.x_min, args.x_max, sample_count)
    ys = bach_sine_real_extension(xs)

    integer_min = max(2, math.ceil(args.x_min))
    integer_max = math.floor(args.x_max)
    integers = np.arange(integer_min, integer_max + 1)
    integer_values = np.array([bach_sine_at_integer(int(n)) for n in integers])

    primes = np.array([n for n in integers if is_prime(int(n))])
    prime_values = np.array([bach_sine_at_integer(int(n)) for n in primes])
    composites = np.array([n for n in integers if n > 1 and not is_prime(int(n))])
    composite_values = np.array([bach_sine_at_integer(int(n)) for n in composites])

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(14, 8.5),
        sharex=True,
        gridspec_kw={"height_ratios": [1.35, 1.0]},
    )

    axes[0].plot(xs, ys, color="#2563eb", linewidth=1.15, label=r"$B_{\sin}(x)$")
    axes[0].scatter(
        primes,
        prime_values,
        color="#dc2626",
        s=36,
        zorder=4,
        label=r"prime integer samples",
    )
    axes[0].scatter(
        composites,
        composite_values,
        color="#111827",
        s=18,
        zorder=3,
        alpha=0.8,
        label=r"composite integer samples",
    )
    axes[0].axhline(0, color="#64748b", linewidth=1)
    axes[0].set_title(
        r"Real sine-wave Bach form "
        r"$B_{\sin}(x)=\sum_{m=2}^{\lfloor x\rfloor-1}"
        r"\left(\frac{\sin(\pi x)}{m\sin(\pi x/m)}\right)^2$"
    )
    axes[0].set_ylabel(r"$B_{\sin}(x)$")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc="upper left")

    axes[1].vlines(
        integers,
        0,
        integer_values,
        color="#60a5fa",
        linewidth=1.1,
        alpha=0.85,
    )
    axes[1].scatter(
        composites,
        composite_values,
        color="#111827",
        s=24,
        zorder=3,
        label=r"composites: $B_{\sin}(n)>0$",
    )
    axes[1].scatter(
        primes,
        prime_values,
        color="#dc2626",
        s=36,
        zorder=4,
        label=r"primes: $B_{\sin}(n)=0$",
    )
    axes[1].axhline(0, color="#64748b", linewidth=1)
    axes[1].set_title(r"Integer samples: $B_{\sin}(n)=d(n)-2$")
    axes[1].set_xlabel(r"$x$ or integer $n$")
    axes[1].set_ylabel(r"$B_{\sin}(n)$")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc="upper left")

    fig.suptitle("Sine-Wave Bach Form", fontsize=16, y=0.985)
    fig.text(
        0.5,
        0.02,
        (
            r"The removable $0/0$ values at divisors use the limit rule, so "
            r"integer primes are exactly the zero samples."
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

    print(f"x range = [{args.x_min}, {args.x_max}]")
    print(f"integer samples = {len(integers)}")
    print(f"prime zeros shown = {len(primes)}")
    print(f"max integer B_sin(n) = {int(np.max(integer_values))}")


if __name__ == "__main__":
    main()
