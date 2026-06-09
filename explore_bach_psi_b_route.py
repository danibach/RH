"""
Explore the Bach-derived Chebyshev psi_B route toward RH.

This diagnostic script computes:

    theta_B(x) = sum_{n <= x} Q_B(n) log(n)
    psi_B(x)   = sum_{N <= x} Lambda_B(N)

where Q_B is Bach's exact prime indicator and Lambda_B is the Bach-derived
von Mangoldt function. Computationally this uses an efficient sieve, but the
mathematical source is the Bach wave prime indicator.

The script prints RH-scale normalized errors:

    (theta_B(x) - x) / (sqrt(x) log^2 x)
    (psi_B(x)   - x) / (sqrt(x) log^2 x)

and the prime-power tail psi_B(x)-theta_B(x).

Python: 3.9+
No third-party dependencies.
"""

from __future__ import annotations

import argparse
import math


def bach_prime_flags(limit: int) -> list[bool]:
    """
    Efficient exact implementation of Q_B(n).
    """
    if limit < 2:
        return [False] * (limit + 1)

    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for p in range(2, math.isqrt(limit) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False

    return is_prime


def bach_lambda_values(limit: int, is_prime: list[bool]) -> list[float]:
    """
    Return Lambda_B(N) for N = 0, 1, ..., limit.
    """
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


def cumulative(values: list[float]) -> list[float]:
    totals = []
    running = 0.0

    for value in values:
        running += value
        totals.append(running)

    return totals


def bach_theta_values(limit: int, is_prime: list[bool]) -> list[float]:
    """
    Return theta_B(x) for x = 0, 1, ..., limit.
    """
    values = [0.0] * (limit + 1)
    running = 0.0

    for n in range(limit + 1):
        if is_prime[n]:
            running += math.log(n)
        values[n] = running

    return values


def checkpoint_values(limit: int, count: int) -> list[int]:
    if count <= 1:
        return [limit]

    values = set()
    for i in range(1, count + 1):
        values.add(max(2, round(limit * i / count)))
    values.add(limit)
    return sorted(values)


def rh_scale(x: int) -> float:
    return math.sqrt(x) * math.log(x) ** 2


def print_route_table(limit: int, checkpoints: int, min_normalized_x: int) -> None:
    is_prime = bach_prime_flags(limit)
    lambda_values = bach_lambda_values(limit, is_prime)
    psi_values = cumulative(lambda_values)
    theta_values = bach_theta_values(limit, is_prime)

    header = (
        f"{'x':>10}  "
        f"{'theta_B-x':>14}  "
        f"{'psi_B-x':>14}  "
        f"{'psi-theta':>14}  "
        f"{'theta norm':>12}  "
        f"{'psi norm':>12}"
    )

    print(header)
    print("-" * len(header))

    for x in checkpoint_values(limit, checkpoints):
        scale = rh_scale(x)
        theta_error = theta_values[x] - x
        psi_error = psi_values[x] - x
        prime_power_tail = psi_values[x] - theta_values[x]

        print(
            f"{x:>10}  "
            f"{theta_error:>14.6f}  "
            f"{psi_error:>14.6f}  "
            f"{prime_power_tail:>14.6f}  "
            f"{theta_error / scale:>12.6f}  "
            f"{psi_error / scale:>12.6f}"
        )

    max_theta_norm = 0.0
    max_psi_norm = 0.0
    max_tail = 0.0

    min_normalized_x = max(2, min(min_normalized_x, limit))

    for x in range(min_normalized_x, limit + 1):
        scale = rh_scale(x)
        max_theta_norm = max(max_theta_norm, abs((theta_values[x] - x) / scale))
        max_psi_norm = max(max_psi_norm, abs((psi_values[x] - x) / scale))
        max_tail = max(max_tail, abs(psi_values[x] - theta_values[x]))

    print()
    print(
        f"max |theta normalized error| for "
        f"{min_normalized_x} <= x <= {limit} = {max_theta_norm:.8f}"
    )
    print(
        f"max |psi normalized error| for "
        f"{min_normalized_x} <= x <= {limit}   = {max_psi_norm:.8f}"
    )
    print(
        f"max prime-power tail for "
        f"{min_normalized_x} <= x <= {limit}          = {max_tail:.8f}"
    )
    print(f"pi_B({limit})                                             = {sum(is_prime)}")
    print(f"theta_B({limit})                                          = {theta_values[limit]:.8f}")
    print(f"psi_B({limit})                                            = {psi_values[limit]:.8f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print diagnostics for the Bach psi_B route toward RH."
    )
    parser.add_argument(
        "--x-max",
        type=int,
        default=100000,
        help="Largest x to inspect. Default: 100000.",
    )
    parser.add_argument(
        "--checkpoints",
        type=int,
        default=12,
        help="Number of checkpoint rows to print. Default: 12.",
    )
    parser.add_argument(
        "--min-normalized-x",
        type=int,
        default=100,
        help=(
            "Smallest x included in max normalized-error statistics. "
            "Default: 100."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.x_max < 3:
        raise ValueError("--x-max must be at least 3")
    if args.checkpoints < 1:
        raise ValueError("--checkpoints must be at least 1")
    if args.min_normalized_x < 2:
        raise ValueError("--min-normalized-x must be at least 2")

    print_route_table(args.x_max, args.checkpoints, args.min_normalized_x)


if __name__ == "__main__":
    main()
