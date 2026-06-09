"""
Plot real extensions of the Bach prime-zero wave sum.

There are two natural views:

    1. Fixed cutoff:
           Z_N(x) = sum_{m=2}^{N} W_m(x)

       This is a continuous finite wave sum.

    2. Bach moving cutoff:
           Z_B(x) = sum_{m=2}^{floor(x)-1} W_m(x)

       This keeps the original integer formula's upper limit. It is wave-built,
       but piecewise, because the active waves change at integer boundaries.

The same comparison is shown for the sine-wave algebra.
"""

from __future__ import annotations

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


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for candidate in range(2, int(math.sqrt(n)) + 1):
        if n % candidate == 0:
            return False
    return True


def roots_unity_multiple_wave(m: int, x: float) -> complex:
    return sum(cmath.exp(1j * math.tau * j * x / m) for j in range(m)) / m


def roots_unity_multiple_wave_array(m: int, xs: np.ndarray) -> np.ndarray:
    values = np.zeros(xs.shape, dtype=complex)
    for j in range(m):
        values += np.exp(1j * math.tau * j * xs / m)
    return values / m


def sine_multiple_wave_array(
    m: int, xs: np.ndarray, tolerance: float = 1e-12
) -> np.ndarray:
    numerator = np.sin(np.pi * xs)
    denominator = m * np.sin(np.pi * xs / m)
    values = np.zeros(xs.shape, dtype=float)

    safe = np.abs(denominator) > tolerance
    values[safe] = (numerator[safe] / denominator[safe]) ** 2

    removable = ~safe
    if np.any(removable):
        nearest_integer = np.rint(xs[removable]).astype(int)
        values[removable] = np.where(nearest_integer % m == 0, 1.0, 0.0)

    return values


def roots_prime_zero_integer(n: int) -> int:
    if n < 2:
        return 0
    value = sum(roots_unity_multiple_wave(m, n) for m in range(2, n))
    return int(round(value.real))


def sine_prime_zero_integer(n: int) -> int:
    if n < 2:
        return 0
    return sum(1 for m in range(2, n) if n % m == 0)


def roots_fixed_cutoff(xs: np.ndarray, cutoff: int) -> np.ndarray:
    values = np.zeros(xs.shape, dtype=complex)
    for m in range(2, cutoff + 1):
        values += roots_unity_multiple_wave_array(m, xs)
    return values


def sine_fixed_cutoff(xs: np.ndarray, cutoff: int) -> np.ndarray:
    values = np.zeros(xs.shape, dtype=float)
    for m in range(2, cutoff + 1):
        values += sine_multiple_wave_array(m, xs)
    return values


def roots_moving_cutoff(xs: np.ndarray) -> np.ndarray:
    values = np.zeros(xs.shape, dtype=complex)
    floors = np.floor(xs).astype(int)
    max_m = int(np.max(floors)) - 1
    for m in range(2, max_m + 1):
        active = floors >= m + 1
        if np.any(active):
            values[active] += roots_unity_multiple_wave_array(m, xs[active])
    return values


def sine_moving_cutoff(xs: np.ndarray) -> np.ndarray:
    values = np.zeros(xs.shape, dtype=float)
    floors = np.floor(xs).astype(int)
    max_m = int(np.max(floors)) - 1
    for m in range(2, max_m + 1):
        active = floors >= m + 1
        if np.any(active):
            values[active] += sine_multiple_wave_array(m, xs[active])
    return values


def style_axes(ax: plt.Axes) -> None:
    ax.grid(True, color="#d1d5db", alpha=0.65, linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#6b7280")
    ax.spines["bottom"].set_color("#6b7280")
    ax.tick_params(colors="#374151", labelsize=9)


def mark_integer_samples(ax: plt.Axes, limit: int, algebra: str) -> None:
    integers = np.arange(2, limit + 1)
    if algebra == "roots":
        z_values = np.array([roots_prime_zero_integer(int(n)) for n in integers])
    else:
        z_values = np.array([sine_prime_zero_integer(int(n)) for n in integers])

    primes = np.array([is_prime(int(n)) for n in integers])
    ax.scatter(
        integers[~primes],
        z_values[~primes],
        color="#111827",
        s=18,
        zorder=4,
        label="composite integer samples",
    )
    ax.scatter(
        integers[primes],
        z_values[primes],
        color="#dc2626",
        s=30,
        zorder=5,
        label="prime zero samples",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot real extensions of Bach prime-zero wave sums."
    )
    parser.add_argument(
        "--x-max",
        type=float,
        default=40.0,
        help="Maximum real x-value. Default: 40.",
    )
    parser.add_argument(
        "--fixed-cutoff",
        type=int,
        default=12,
        help="Fixed cutoff N for Z_N(x). Default: 12.",
    )
    parser.add_argument(
        "--samples-per-unit",
        type=int,
        default=180,
        help="Real-curve samples per unit interval. Default: 180.",
    )
    parser.add_argument(
        "--save",
        default="bach_prime_zero_real_extensions.png",
        help="Output image path. Default: bach_prime_zero_real_extensions.png.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.x_max < 8:
        raise ValueError("--x-max must be at least 8")
    if args.fixed_cutoff < 2:
        raise ValueError("--fixed-cutoff must be at least 2")
    if args.samples_per_unit < 20:
        raise ValueError("--samples-per-unit must be at least 20")

    xs = np.linspace(2, args.x_max, int((args.x_max - 2) * args.samples_per_unit) + 1)
    integer_limit = math.floor(args.x_max)

    root_fixed = roots_fixed_cutoff(xs, args.fixed_cutoff)
    sine_fixed = sine_fixed_cutoff(xs, args.fixed_cutoff)
    root_moving = roots_moving_cutoff(xs)
    sine_moving = sine_moving_cutoff(xs)

    fig, axes = plt.subplots(2, 2, figsize=(16, 8.8))

    axes[0, 0].plot(xs, root_fixed.real, color="#2563eb", linewidth=1.15, label="real")
    axes[0, 0].plot(
        xs, root_fixed.imag, color="#f97316", linewidth=1.0, alpha=0.9, label="imag"
    )
    axes[0, 0].plot(
        xs, np.abs(root_fixed), color="#16a34a", linewidth=1.0, label="magnitude"
    )
    axes[0, 0].set_title(
        rf"Fixed roots-of-unity wave sum  $Z_{{{args.fixed_cutoff}}}(x)=\sum_{{m=2}}^{{{args.fixed_cutoff}}}W_m(x)$",
        fontsize=11,
    )
    axes[0, 0].set_ylabel(r"$Z_N(x)$")
    axes[0, 0].legend(loc="upper right", fontsize=8)
    style_axes(axes[0, 0])

    axes[0, 1].plot(xs, sine_fixed, color="#7c3aed", linewidth=1.15)
    axes[0, 1].set_title(
        rf"Fixed sine-wave sum  $Z_{{\sin,{args.fixed_cutoff}}}(x)=\sum_{{m=2}}^{{{args.fixed_cutoff}}}S_m(x)$",
        fontsize=11,
    )
    axes[0, 1].set_ylabel(r"$Z_{\sin,N}(x)$")
    style_axes(axes[0, 1])

    axes[1, 0].plot(
        xs,
        root_moving.real,
        color="#0891b2",
        linewidth=1.15,
        label="real part",
    )
    axes[1, 0].plot(
        xs,
        root_moving.imag,
        color="#ea580c",
        linewidth=0.95,
        alpha=0.85,
        label="imag part",
    )
    axes[1, 0].plot(
        xs,
        np.abs(root_moving),
        color="#16a34a",
        linewidth=1.0,
        alpha=0.9,
        label="magnitude",
    )
    mark_integer_samples(axes[1, 0], integer_limit, "roots")
    axes[1, 0].set_title(
        r"Moving Bach roots-of-unity extension  $Z_B(x)=\sum_{m=2}^{\lfloor x\rfloor-1}W_m(x)$",
        fontsize=11,
    )
    axes[1, 0].set_xlabel(r"$x$")
    axes[1, 0].set_ylabel(r"$Z_B(x)$")
    axes[1, 0].legend(loc="upper left", fontsize=8)
    style_axes(axes[1, 0])

    axes[1, 1].plot(xs, sine_moving, color="#be123c", linewidth=1.15)
    mark_integer_samples(axes[1, 1], integer_limit, "sine")
    axes[1, 1].set_title(
        r"Moving Bach sine extension  $Z_{\sin,B}(x)=\sum_{m=2}^{\lfloor x\rfloor-1}S_m(x)$",
        fontsize=11,
    )
    axes[1, 1].set_xlabel(r"$x$")
    axes[1, 1].set_ylabel(r"$Z_{\sin,B}(x)$")
    axes[1, 1].legend(loc="upper left", fontsize=8)
    style_axes(axes[1, 1])

    fig.suptitle(
        "Prime-Zero Function as a Real Wave Sum",
        fontsize=16,
        fontweight="bold",
        y=0.985,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.955])

    plt.savefig(args.save, dpi=180)
    print(f"Saved plot to {args.save}")
    print(f"x_max = {args.x_max}")
    print(f"fixed cutoff = {args.fixed_cutoff}")


if __name__ == "__main__":
    main()
