#!/usr/bin/env python3
"""
Plot the unfolded Riemann zeta function on the critical line.

This script uses

    F(u) = zeta(1/2 + i T(u))

where T(u) is the inverse of the average zero-counting function

    N_avg(t) = t/(2*pi) * log(t/(2*pi)) - t/(2*pi) + 7/8.

In this unfolded coordinate u, the average density of zeta zeros is roughly
constant: one unit of u corresponds to one expected zero.

Example:
    python3 plot_zeta_unfolded.py --u-min 0 --u-max 10 --points 1000
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from plot_zeta_critical_line import make_svg, zeta_on_vertical_line


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Plot F(u) = zeta(0.5 + i T(u)), where T is the inverse of "
            "the average zero-counting function N_avg."
        )
    )
    parser.add_argument("--u-min", type=float, default=0.0, help="Minimum unfolded input u.")
    parser.add_argument("--u-max", type=float, default=10.0, help="Maximum unfolded input u.")
    parser.add_argument("--points", type=int, default=1000, help="Number of sampled u values.")
    parser.add_argument(
        "--terms",
        type=int,
        default=128,
        help="Euler-transformed eta terms. Increase this for larger u ranges.",
    )
    parser.add_argument("--width", type=int, default=1000, help="SVG width in pixels.")
    parser.add_argument("--height", type=int, default=780, help="SVG height in pixels.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("zeta_unfolded.svg"),
        help="SVG file to write.",
    )
    return parser.parse_args()


def average_zero_count(t: float) -> float:
    """Average Riemann-von Mangoldt zero count up to height t."""
    if t <= 0:
        raise ValueError("t must be positive")

    scaled_t = t / math.tau
    return scaled_t * math.log(scaled_t) - scaled_t + 7 / 8


def inverse_average_zero_count(u: float, iterations: int = 80) -> float:
    """Find T(u), the monotone inverse of N_avg(t) for t >= 2*pi."""
    low = math.tau
    min_u = average_zero_count(low)
    if u < min_u:
        raise ValueError(
            f"u must be at least {min_u:.6g}; below that N_avg is not monotone."
        )
    if u == min_u:
        return low

    high = max(2 * math.tau, 16.0)
    while average_zero_count(high) < u:
        high *= 2

    for _ in range(iterations):
        middle = (low + high) / 2
        if average_zero_count(middle) < u:
            low = middle
        else:
            high = middle

    return (low + high) / 2


def main() -> None:
    args = parse_args()

    if args.points < 2:
        raise ValueError("--points must be at least 2")
    if args.terms < 8:
        raise ValueError("--terms must be at least 8")
    if args.u_max <= args.u_min:
        raise ValueError("--u-max must be greater than --u-min")
    if args.width < 500 or args.height < 400:
        raise ValueError("--width must be at least 500 and --height must be at least 400")

    u_step = (args.u_max - args.u_min) / (args.points - 1)
    u_values = [args.u_min + i * u_step for i in range(args.points)]
    t_values = [inverse_average_zero_count(u) for u in u_values]
    values = [zeta_on_vertical_line(0.5, t, args.terms) for t in t_values]

    title = "Unfolded zeta output F(u) = zeta(0.5 + i T(u))"
    subtitle = (
        f"{u_values[0]:g} <= u <= {u_values[-1]:g}; "
        f"T(u) maps to {t_values[0]:.4g} <= t <= {t_values[-1]:.4g}; "
        f"{len(u_values)} samples"
    )
    svg = make_svg(
        values,
        u_values,
        0.5,
        args.width,
        args.height,
        parameter_label="u",
        title=title,
        subtitle=subtitle,
    )

    args.output.write_text(svg, encoding="utf-8")
    print(f"Saved plot to {args.output.resolve()}")


if __name__ == "__main__":
    main()
