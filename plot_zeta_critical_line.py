#!/usr/bin/env python3
"""
Plot values of the Riemann zeta function on the critical line.

The input points are s = sigma + i t, with sigma defaulting to 0.5.
The generated SVG shows the output zeta(s) in the complex plane.

This script uses only Python's standard library. It evaluates zeta(s) through
the Dirichlet eta function:

    zeta(s) = eta(s) / (1 - 2^(1 - s))

and accelerates the alternating eta series with Euler's transformation.

Example:
    python3 plot_zeta_critical_line.py --t-min 0 --t-max 50 --points 1000
"""

from __future__ import annotations

import argparse
import cmath
import html
import math
from pathlib import Path


VIRIDIS_STOPS = (
    (68, 1, 84),
    (59, 82, 139),
    (33, 145, 140),
    (94, 201, 98),
    (253, 231, 37),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot zeta(0.5 + i t) as t varies, in the output complex plane."
    )
    parser.add_argument("--sigma", type=float, default=0.5, help="Real part of s.")
    parser.add_argument("--t-min", type=float, default=0.0, help="Minimum imaginary part.")
    parser.add_argument("--t-max", type=float, default=50.0, help="Maximum imaginary part.")
    parser.add_argument("--points", type=int, default=1000, help="Number of sampled t values.")
    parser.add_argument(
        "--terms",
        type=int,
        default=96,
        help="Euler-transformed eta terms. Increase this for large t ranges.",
    )
    parser.add_argument("--width", type=int, default=1000, help="SVG width in pixels.")
    parser.add_argument("--height", type=int, default=780, help="SVG height in pixels.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("zeta_critical_line.svg"),
        help="SVG file to write.",
    )
    return parser.parse_args()


def eta_euler(sigma: float, t: float, terms: int) -> complex:
    """Evaluate eta(sigma + i t) using Euler's transformation."""
    diffs = [
        (n + 1) ** (-sigma) * cmath.exp(-1j * t * math.log(n + 1))
        for n in range(terms)
    ]

    total = 0j
    scale = 0.5
    for k in range(terms):
        total += scale * diffs[0]
        for j in range(terms - k - 1):
            diffs[j] -= diffs[j + 1]
        scale *= 0.5

    return total


def zeta_on_vertical_line(sigma: float, t: float, terms: int) -> complex:
    s = complex(sigma, t)
    denominator = 1 - cmath.exp((1 - s) * math.log(2))
    return eta_euler(sigma, t, terms) / denominator


def color_at(fraction: float) -> str:
    fraction = max(0.0, min(1.0, fraction))
    scaled = fraction * (len(VIRIDIS_STOPS) - 1)
    index = min(int(scaled), len(VIRIDIS_STOPS) - 2)
    local = scaled - index

    r1, g1, b1 = VIRIDIS_STOPS[index]
    r2, g2, b2 = VIRIDIS_STOPS[index + 1]
    r = round(r1 + (r2 - r1) * local)
    g = round(g1 + (g2 - g1) * local)
    b = round(b1 + (b2 - b1) * local)
    return f"#{r:02x}{g:02x}{b:02x}"


def nice_ticks(low: float, high: float, target_count: int = 8) -> list[float]:
    span = high - low
    if span <= 0:
        return [low]

    raw_step = span / target_count
    magnitude = 10 ** math.floor(math.log10(raw_step))
    normalized = raw_step / magnitude

    if normalized <= 1:
        step = magnitude
    elif normalized <= 2:
        step = 2 * magnitude
    elif normalized <= 5:
        step = 5 * magnitude
    else:
        step = 10 * magnitude

    first = math.ceil(low / step) * step
    ticks = []
    current = first
    while current <= high + step * 0.5:
        ticks.append(0.0 if abs(current) < step * 1e-9 else current)
        current += step
    return ticks


def format_tick(value: float) -> str:
    if abs(value) >= 1000 or (0 < abs(value) < 0.001):
        return f"{value:.1e}"
    return f"{value:.3g}"


def make_svg(
    values: list[complex],
    t_values: list[float],
    sigma: float,
    width: int,
    height: int,
) -> str:
    margin_left = 92
    margin_right = 120
    margin_top = 68
    margin_bottom = 78
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    real_values = [value.real for value in values]
    imag_values = [value.imag for value in values]
    min_x, max_x = min(real_values), max(real_values)
    min_y, max_y = min(imag_values), max(imag_values)

    x_padding = max((max_x - min_x) * 0.08, 0.5)
    y_padding = max((max_y - min_y) * 0.08, 0.5)
    min_x -= x_padding
    max_x += x_padding
    min_y -= y_padding
    max_y += y_padding

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    x_span = max_x - min_x
    y_span = max_y - min_y
    scale = min(plot_width / x_span, plot_height / y_span)

    def screen_x(x: float) -> float:
        return margin_left + plot_width / 2 + (x - center_x) * scale

    def screen_y(y: float) -> float:
        return margin_top + plot_height / 2 - (y - center_y) * scale

    visible_min_x = center_x - plot_width / (2 * scale)
    visible_max_x = center_x + plot_width / (2 * scale)
    visible_min_y = center_y - plot_height / (2 * scale)
    visible_max_y = center_y + plot_height / (2 * scale)

    x_ticks = nice_ticks(visible_min_x, visible_max_x)
    y_ticks = nice_ticks(visible_min_y, visible_max_y)

    title = f"zeta(s) output for s = {sigma:g} + i t"
    subtitle = f"{t_values[0]:g} <= t <= {t_values[-1]:g}, {len(t_values)} samples"

    pieces = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<linearGradient id="t-gradient" x1="0%" y1="100%" x2="0%" y2="0%">',
    ]

    for i, stop in enumerate(VIRIDIS_STOPS):
        offset = 100 * i / (len(VIRIDIS_STOPS) - 1)
        color = f"#{stop[0]:02x}{stop[1]:02x}{stop[2]:02x}"
        pieces.append(f'<stop offset="{offset:.1f}%" stop-color="{color}"/>')

    pieces.extend(
        [
            "</linearGradient>",
            "</defs>",
            '<rect width="100%" height="100%" fill="#f8fafc"/>',
            f'<text x="{width / 2:.1f}" y="30" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="23" font-weight="700" fill="#0f172a">{html.escape(title)}</text>',
            f'<text x="{width / 2:.1f}" y="55" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#475569">{html.escape(subtitle)}</text>',
            f'<rect x="{margin_left}" y="{margin_top}" width="{plot_width}" height="{plot_height}" fill="#ffffff" stroke="#cbd5e1"/>',
        ]
    )

    for tick in x_ticks:
        x = screen_x(tick)
        pieces.append(f'<line x1="{x:.2f}" y1="{margin_top}" x2="{x:.2f}" y2="{margin_top + plot_height}" stroke="#e2e8f0" stroke-width="1"/>')
        pieces.append(f'<text x="{x:.2f}" y="{margin_top + plot_height + 24}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#475569">{format_tick(tick)}</text>')

    for tick in y_ticks:
        y = screen_y(tick)
        pieces.append(f'<line x1="{margin_left}" y1="{y:.2f}" x2="{margin_left + plot_width}" y2="{y:.2f}" stroke="#e2e8f0" stroke-width="1"/>')
        pieces.append(f'<text x="{margin_left - 12}" y="{y + 4:.2f}" text-anchor="end" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#475569">{format_tick(tick)}</text>')

    if visible_min_y <= 0 <= visible_max_y:
        y_zero = screen_y(0)
        pieces.append(f'<line x1="{margin_left}" y1="{y_zero:.2f}" x2="{margin_left + plot_width}" y2="{y_zero:.2f}" stroke="#334155" stroke-width="1.4"/>')
    if visible_min_x <= 0 <= visible_max_x:
        x_zero = screen_x(0)
        pieces.append(f'<line x1="{x_zero:.2f}" y1="{margin_top}" x2="{x_zero:.2f}" y2="{margin_top + plot_height}" stroke="#334155" stroke-width="1.4"/>')

    points = [(screen_x(value.real), screen_y(value.imag)) for value in values]
    segment_count = len(points) - 1
    for i, ((x1, y1), (x2, y2)) in enumerate(zip(points, points[1:])):
        color = color_at(i / max(segment_count - 1, 1))
        pieces.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="1.7" stroke-linecap="round"/>')

    start_x, start_y = points[0]
    end_x, end_y = points[-1]
    pieces.append(f'<circle cx="{start_x:.2f}" cy="{start_y:.2f}" r="5" fill="#16a34a" stroke="#ffffff" stroke-width="2"/>')
    pieces.append(f'<circle cx="{end_x:.2f}" cy="{end_y:.2f}" r="5" fill="#dc2626" stroke="#ffffff" stroke-width="2"/>')

    pieces.extend(
        [
            f'<text x="{margin_left + plot_width / 2:.1f}" y="{height - 25}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#0f172a">Re(zeta(s))</text>',
            f'<text x="24" y="{margin_top + plot_height / 2:.1f}" text-anchor="middle" transform="rotate(-90 24 {margin_top + plot_height / 2:.1f})" font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#0f172a">Im(zeta(s))</text>',
            f'<rect x="{width - margin_right + 42}" y="{margin_top}" width="18" height="{plot_height}" fill="url(#t-gradient)" stroke="#cbd5e1"/>',
            f'<text x="{width - margin_right + 70}" y="{margin_top + 4}" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#475569">{format_tick(t_values[-1])}</text>',
            f'<text x="{width - margin_right + 70}" y="{margin_top + plot_height}" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#475569">{format_tick(t_values[0])}</text>',
            f'<text x="{width - margin_right + 51}" y="{margin_top + plot_height / 2:.1f}" text-anchor="middle" transform="rotate(-90 {width - margin_right + 51} {margin_top + plot_height / 2:.1f})" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#0f172a">input t</text>',
            f'<text x="{start_x + 10:.2f}" y="{start_y - 10:.2f}" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#166534">start</text>',
            f'<text x="{end_x + 10:.2f}" y="{end_y - 10:.2f}" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#991b1b">end</text>',
            "</svg>",
        ]
    )

    return "\n".join(pieces)


def main() -> None:
    args = parse_args()

    if args.points < 2:
        raise ValueError("--points must be at least 2")
    if args.terms < 8:
        raise ValueError("--terms must be at least 8")
    if args.t_max <= args.t_min:
        raise ValueError("--t-max must be greater than --t-min")
    if args.width < 500 or args.height < 400:
        raise ValueError("--width must be at least 500 and --height must be at least 400")

    t_step = (args.t_max - args.t_min) / (args.points - 1)
    t_values = [args.t_min + i * t_step for i in range(args.points)]
    values = [zeta_on_vertical_line(args.sigma, t, args.terms) for t in t_values]

    svg = make_svg(values, t_values, args.sigma, args.width, args.height)
    args.output.write_text(svg, encoding="utf-8")
    print(f"Saved plot to {args.output.resolve()}")


if __name__ == "__main__":
    main()
