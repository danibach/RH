"""
Numerically check the Bach-derived Lambda transform.

The derivation gives, for Re(s)>1:

    L_B(s) = sum_{N>=1} Lambda_B(N) / N^s
           = -zeta'(s) / zeta(s).

This script computes a finite Bach/Lambda_B partial sum and compares it with
the zeta-side value.

Python: 3.9+
Dependencies:
    pip install mpmath
"""

import argparse
import math

import mpmath as mp


def bach_prime_flags(limit):
    """
    Efficient exact implementation of Bach's prime indicator Q_B(n).
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
    Build Lambda_B(N), derived from the Bach prime indicator:

        Lambda_B(p^k)=log(p), Lambda_B(N)=0 otherwise.
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


def bach_lambda_transform_partial(s, limit):
    lambda_values = bach_lambda_values(limit)
    total = mp.mpc(0)

    for n in range(1, limit + 1):
        if lambda_values[n] != 0:
            total += lambda_values[n] / mp.power(n, s)

    return total


def zeta_log_derivative_side(s):
    return -mp.diff(mp.zeta, s) / mp.zeta(s)


def main():
    parser = argparse.ArgumentParser(
        description="Check L_B(s)=sum Lambda_B(n)n^-s against -zeta'(s)/zeta(s)."
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=2.0,
        help="Real part of s. Use sigma > 1. Default: 2.0",
    )
    parser.add_argument(
        "--t",
        type=float,
        default=0.0,
        help="Imaginary part of s. Default: 0.0",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200000,
        help="Partial-sum cutoff for Lambda_B. Default: 200000",
    )
    parser.add_argument(
        "--dps",
        type=int,
        default=30,
        help="mpmath decimal precision. Default: 30",
    )
    args, _unknown_args = parser.parse_known_args()

    if args.sigma <= 1:
        raise ValueError("--sigma must be > 1 for the ordinary Dirichlet series")

    if args.limit < 10:
        raise ValueError("--limit must be at least 10")

    mp.mp.dps = args.dps

    s = mp.mpc(args.sigma, args.t)
    partial = bach_lambda_transform_partial(s, args.limit)
    zeta_side = zeta_log_derivative_side(s)
    difference = partial - zeta_side

    print(f"s = {s}")
    print(f"limit = {args.limit}")
    print()
    print(f"partial Bach L_B(s)      = {mp.nstr(partial, 18)}")
    print(f"-zeta'(s)/zeta(s)        = {mp.nstr(zeta_side, 18)}")
    print(f"partial minus zeta side  = {mp.nstr(difference, 18)}")
    print(f"absolute difference      = {mp.nstr(abs(difference), 12)}")


if __name__ == "__main__":
    main()
