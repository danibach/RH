"""
Plot the Bach prime-counting error against the logarithmic integral.

The Bach count B_pi(x) is exact:

    B_pi(x) = pi(x)

so the plotted error is the classical prime-counting error:

    E_B(x) = B_pi(x) - Li(x).

Here Li(x) is evaluated as Ei(log x), matching the Riemann explicit-formula
scripts in this project. An optional offset curve Li(x)-Li(2) is also available
for comparison with the integral from 2 to x.

Python: 3.9+
Dependencies:
    pip install matplotlib mpmath scipy

SciPy is optional; mpmath is used as the fallback for Ei.
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

try:
    from scipy.special import expi as scipy_expi
except ImportError:
    scipy_expi = None

try:
    import mpmath as mp
except ImportError:
    mp = None


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


def li(x):
    """
    Logarithmic integral Li(x), evaluated as Ei(log x) for x > 1.
    """
    if x <= 1:
        raise ValueError("Li(x) here is evaluated only for x > 1")

    log_x = math.log(float(x))

    if scipy_expi is not None:
        return float(scipy_expi(log_x).real)

    if mp is None:
        raise ImportError("Install scipy or mpmath to compute Li(x)")

    return float(mp.ei(log_x).real)


def main():
    parser = argparse.ArgumentParser(
        description="Plot E_B(x)=B_pi(x)-Li(x), where B_pi(x)=pi(x)."
    )
    parser.add_argument(
        "--x-max",
        type=int,
        default=1000,
        help="Largest integer x-value to sample. Default: 1000",
    )
    parser.add_argument(
        "--offset-li",
        action="store_true",
        help="Use Li(x)-Li(2), corresponding to the integral from 2 to x.",
    )
    parser.add_argument(
        "--save",
        default="",
        help="Optional output path, for example bach_li_error.png",
    )
    args, _unknown_args = parser.parse_known_args()

    if args.x_max < 3:
        raise ValueError("--x-max must be at least 3")

    pi_counts = prime_counts_up_to(args.x_max)

    xs = list(range(2, args.x_max + 1))
    bach_pi = [pi_counts[x] for x in xs]

    li_offset = li(2) if args.offset_li else 0.0
    li_values = [li(x) - li_offset for x in xs]
    errors = [exact - approx for exact, approx in zip(bach_pi, li_values)]

    title_li = r"$\operatorname{Li}(x)-\operatorname{Li}(2)$" if args.offset_li else r"$\operatorname{Li}(x)$"

    fig, axes = plt.subplots(2, 1, figsize=(13, 9), sharex=True)

    axes[0].step(xs, bach_pi, where="post", linewidth=2.0, label=r"$B_\pi(x)=\pi(x)$")
    axes[0].plot(xs, li_values, linewidth=1.6, label=title_li)
    axes[0].set_title("Bach Prime Count Compared With Logarithmic Integral")
    axes[0].set_ylabel("count")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(xs, errors, color="crimson", linewidth=1.5, label=r"$E_B(x)=B_\pi(x)-\operatorname{Li}(x)$")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_title("Error Term")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("error")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    plt.tight_layout()

    if args.save:
        plt.savefig(args.save, dpi=180)
        print(f"Saved plot to {args.save}")
    else:
        plt.show()

    print(f"x_max = {args.x_max}")
    print(f"B_pi({args.x_max}) = {bach_pi[-1]}")
    print(f"Li({args.x_max}) = {li_values[-1]:.8f}")
    print(f"E_B({args.x_max}) = {errors[-1]:.8f}")


if __name__ == "__main__":
    main()
