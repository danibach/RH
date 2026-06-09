"""
Plot the three Bach wave-based prime functions in two algebras.

The figure compares:

    1. the integer multiple wave for m = 5,
    2. the prime-zero function,
    3. the prime-counting function,

for both the roots-of-unity algebra and the sine-wave algebra.

Example:
    python3 plot_bach_three_wave_representations.py --limit 60 --save bach_three_wave_representations.png
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


def roots_unity_multiple_wave(m: int, x: float) -> complex:
    """Return W_m(x) = (1/m) sum_{j=0}^{m-1} exp(2*pi*i*j*x/m)."""
    return sum(cmath.exp(1j * math.tau * j * x / m) for j in range(m)) / m


def roots_unity_multiple_wave_array(m: int, xs: np.ndarray) -> np.ndarray:
    """Vectorized roots-of-unity multiple wave."""
    values = np.zeros(xs.shape, dtype=complex)
    for j in range(m):
        values += np.exp(1j * math.tau * j * xs / m)
    return values / m


def sine_multiple_wave_array(
    m: int, xs: np.ndarray, tolerance: float = 1e-12
) -> np.ndarray:
    """
    Return S_m(x) = (sin(pi*x) / (m*sin(pi*x/m)))^2.

    The removable 0/0 values are filled with the integer-sample limit.
    """
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


def roots_unity_prime_zero(n: int) -> int:
    """Return the integer sample of Z(n) = sum_{m=2}^{n-1} W_m(n)."""
    if n < 2:
        return 0
    value = sum(roots_unity_multiple_wave(m, n) for m in range(2, n))
    return int(round(value.real))


def sine_prime_zero(n: int) -> int:
    """Return the integer sample of Z_sin(n) with the removable-limit rule."""
    if n < 2:
        return 0
    return sum(1 for m in range(2, n) if n % m == 0)


def sinc_zero_indicator(z: int) -> int:
    """Return sinc(z), specialized to integer z."""
    return 1 if z == 0 else 0


def cumulative_counts(z_values: list[int]) -> np.ndarray:
    """Convert prime-zero values into cumulative Bach prime counts."""
    return np.cumsum([sinc_zero_indicator(z) for z in z_values])


def build_values(limit: int) -> dict[str, np.ndarray]:
    integers = np.arange(2, limit + 1)
    root_z = np.array([roots_unity_prime_zero(int(n)) for n in integers])
    sine_z = np.array([sine_prime_zero(int(n)) for n in integers])
    root_count = cumulative_counts(root_z.tolist())
    sine_count = cumulative_counts(sine_z.tolist())

    return {
        "integers": integers,
        "root_z": root_z,
        "sine_z": sine_z,
        "root_count": root_count,
        "sine_count": sine_count,
    }


def style_axes(ax: plt.Axes) -> None:
    ax.grid(True, color="#d1d5db", alpha=0.65, linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#6b7280")
    ax.spines["bottom"].set_color("#6b7280")
    ax.tick_params(colors="#374151", labelsize=9)


def plot_multiple_wave_panels(
    axes: np.ndarray,
    m: int,
    wave_x_max: float,
    samples_per_unit: int,
) -> None:
    xs = np.linspace(0, wave_x_max, int(wave_x_max * samples_per_unit) + 1)
    integer_xs = np.arange(0, math.floor(wave_x_max) + 1)

    root_values = roots_unity_multiple_wave_array(m, xs)
    root_integer_values = np.array(
        [roots_unity_multiple_wave(m, int(n)).real for n in integer_xs]
    )
    root_multiples = integer_xs[integer_xs % m == 0]

    axes[0].plot(xs, root_values.real, color="#2563eb", linewidth=1.25, label="real")
    axes[0].plot(
        xs, root_values.imag, color="#f97316", linewidth=1.05, alpha=0.9, label="imag"
    )
    axes[0].plot(
        xs,
        np.abs(root_values),
        color="#16a34a",
        linewidth=1.1,
        alpha=0.85,
        label="magnitude",
    )
    axes[0].scatter(
        integer_xs,
        root_integer_values,
        color="#111827",
        s=16,
        zorder=4,
        label="integer samples",
    )
    axes[0].scatter(
        root_multiples,
        np.ones_like(root_multiples, dtype=float),
        color="#dc2626",
        s=32,
        zorder=5,
        label=f"multiples of {m}",
    )
    axes[0].set_title(
        "Roots-of-unity multiple wave  "
        rf"$W_{m}(x)=\frac{{1}}{{{m}}}\sum_{{j=0}}^{{{m - 1}}}e^{{2\pi ijx/{m}}}$",
        fontsize=11,
    )
    axes[0].set_ylabel(rf"$W_{m}(x)$")
    axes[0].legend(loc="upper right", fontsize=8, ncols=2)
    style_axes(axes[0])

    sine_values = sine_multiple_wave_array(m, xs)
    sine_integer_values = sine_multiple_wave_array(m, integer_xs.astype(float))

    axes[1].plot(xs, sine_values, color="#7c3aed", linewidth=1.25)
    axes[1].scatter(
        integer_xs,
        sine_integer_values,
        color="#111827",
        s=16,
        zorder=4,
        label="integer samples",
    )
    axes[1].scatter(
        root_multiples,
        np.ones_like(root_multiples, dtype=float),
        color="#dc2626",
        s=32,
        zorder=5,
        label=f"multiples of {m}",
    )
    axes[1].set_title(
        "Sine multiple wave  "
        rf"$S_{m}(x)=\left(\frac{{\sin(\pi x)}}{{{m}\sin(\pi x/{m})}}\right)^2$",
        fontsize=11,
    )
    axes[1].set_ylabel(rf"$S_{m}(x)$")
    axes[1].legend(loc="upper right", fontsize=8)
    style_axes(axes[1])


def plot_prime_zero_panels(axes: np.ndarray, values: dict[str, np.ndarray]) -> None:
    integers = values["integers"]

    for ax, z_values, title, ylabel, color in [
        (
            axes[0],
            values["root_z"],
            r"Roots-of-unity prime-zero function  $Z(n)=\sum_{m=2}^{n-1}W_m(n)$",
            r"$Z(n)$",
            "#0891b2",
        ),
        (
            axes[1],
            values["sine_z"],
            r"Sine prime-zero function  $Z_{\sin}(n)=\sum_{m=2}^{n-1}S_m(n)$",
            r"$Z_{\sin}(n)$",
            "#9333ea",
        ),
    ]:
        prime_mask = z_values == 0
        composite_mask = ~prime_mask
        ax.vlines(integers, 0, z_values, color=color, linewidth=0.9, alpha=0.65)
        ax.scatter(
            integers[composite_mask],
            z_values[composite_mask],
            color="#111827",
            s=18,
            label="composites",
            zorder=3,
        )
        ax.scatter(
            integers[prime_mask],
            z_values[prime_mask],
            color="#dc2626",
            s=28,
            label="prime zeros",
            zorder=4,
        )
        ax.axhline(0, color="#6b7280", linewidth=0.9)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel(ylabel)
        ax.legend(loc="upper left", fontsize=8)
        style_axes(ax)


def plot_prime_count_panels(axes: np.ndarray, values: dict[str, np.ndarray]) -> None:
    integers = values["integers"]

    for ax, count_values, title, ylabel, color in [
        (
            axes[0],
            values["root_count"],
            r"Roots-of-unity Bach prime count  $B_\pi(x)=\sum_{2\leq n\leq x}\mathrm{sinc}(Z(n))$",
            r"$B_\pi(x)$",
            "#0f766e",
        ),
        (
            axes[1],
            values["sine_count"],
            r"Sine Bach prime count  $B_{\pi,\sin}(x)=\sum_{2\leq n\leq x}\mathrm{sinc}(Z_{\sin}(n))$",
            r"$B_{\pi,\sin}(x)$",
            "#be123c",
        ),
    ]:
        step_x = np.r_[1, integers]
        step_y = np.r_[0, count_values]
        ax.step(step_x, step_y, where="post", color=color, linewidth=2.0)
        ax.scatter(
            integers,
            count_values,
            color="#111827",
            s=12,
            alpha=0.85,
            zorder=3,
        )
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(ylabel)
        style_axes(ax)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot Bach wave functions in roots-of-unity and sine-wave forms."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=60,
        help="Largest integer for prime-zero and prime-count panels. Default: 60.",
    )
    parser.add_argument(
        "--multiple",
        type=int,
        default=5,
        help="Integer multiple wave to show. Default: 5.",
    )
    parser.add_argument(
        "--wave-x-max",
        type=float,
        default=30.0,
        help="Maximum x-value for the multiple-wave panels. Default: 30.",
    )
    parser.add_argument(
        "--samples-per-unit",
        type=int,
        default=140,
        help="Real-curve samples per unit for the multiple-wave panels. Default: 140.",
    )
    parser.add_argument(
        "--save",
        default="bach_three_wave_representations.png",
        help="Output image path. Default: bach_three_wave_representations.png.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.limit < 5:
        raise ValueError("--limit must be at least 5")
    if args.multiple < 2:
        raise ValueError("--multiple must be at least 2")
    if args.wave_x_max < args.multiple:
        raise ValueError("--wave-x-max must be at least --multiple")
    if args.samples_per_unit < 20:
        raise ValueError("--samples-per-unit must be at least 20")

    values = build_values(args.limit)

    if not np.array_equal(values["root_z"], values["sine_z"]):
        raise AssertionError("roots-of-unity and sine prime-zero samples differ")
    if not np.array_equal(values["root_count"], values["sine_count"]):
        raise AssertionError("roots-of-unity and sine prime-count samples differ")

    fig, axes = plt.subplots(3, 2, figsize=(16, 11))
    plot_multiple_wave_panels(
        axes[0], args.multiple, args.wave_x_max, args.samples_per_unit
    )
    plot_prime_zero_panels(axes[1], values)
    plot_prime_count_panels(axes[2], values)

    fig.suptitle(
        "Bach Wave-Based Prime Functions: Roots-of-Unity Algebra and Sine-Wave Algebra",
        fontsize=16,
        fontweight="bold",
        y=0.985,
    )
    fig.tight_layout(rect=[0, 0.025, 1, 0.955])

    plt.savefig(args.save, dpi=180)
    print(f"Saved plot to {args.save}")
    print(f"limit = {args.limit}")
    print(f"prime count at limit = {int(values['root_count'][-1])}")


if __name__ == "__main__":
    main()
