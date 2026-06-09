"""
Wave-only Bach prime-zero and prime-counting functions.

The core functions here intentionally avoid trial division, modulo checks,
sieves, and precomputed prime tables. They follow the three-step wave plan:

    A. Build one multiple wave for each integer m:

           W_m(n) = (1/m) sum_{j=0}^{m-1} exp(2*pi*i*j*n/m).

       At integer inputs, W_m(n) is mathematically 1 at multiples of m and
       0 at non-multiples.

    B. Sum the proper-multiple waves:

           Z_wave(n) = sum_{m=2}^{n-1} W_m(n).

       This is zero exactly at primes. It is a prime-zero indicator, not a
       0/1 prime indicator.

    C. Convert the zero indicator into a 0/1 indicator by a sinc wave and sum:

           P_wave(n) = sinc(Z_wave(n))
           B_pi_wave(x) = sum_{2 <= n <= floor(x)} P_wave(n).

This is the literal wave formula, not the fast computational version.
"""

from __future__ import annotations

import argparse
import cmath
import math


def bach_multiple_wave(m: int, n: int) -> complex:
    """
    Return the literal roots-of-unity multiple wave W_m(n).

    W_m(n) = (1/m) * sum_{j=0}^{m-1} exp(2*pi*i*j*n/m)

    The returned value is complex because the formula is evaluated numerically.
    For integer inputs it is mathematically real and equals either 0 or 1.
    """
    if m < 1:
        raise ValueError("m must be at least 1")

    angle = math.tau * n / m
    real_terms = []
    imag_terms = []

    for j in range(m):
        value = cmath.exp(1j * angle * j)
        real_terms.append(value.real)
        imag_terms.append(value.imag)

    return complex(math.fsum(real_terms), math.fsum(imag_terms)) / m


def bach_divisor_wave(m: int, n: int) -> complex:
    """
    Backward-compatible name for the multiple wave W_m(n).
    """
    return bach_multiple_wave(m, n)


def bach_prime_zero_wave_sum(n: int) -> complex:
    """
    Return Z_wave(n) = sum_{m=2}^{n-1} W_m(n).

    At integer n >= 2 this sums only proper-multiple waves. It is zero exactly
    when n is prime, and positive at composite n.
    """
    if n < 2:
        return 0j

    total = 0j

    for m in range(2, n):
        total += bach_multiple_wave(m, n)

    return total


def bach_wave_divisor_count(n: int) -> complex:
    """
    Backward-compatible name for the prime-zero wave sum Z_wave(n).
    """
    return bach_prime_zero_wave_sum(n)


def bach_prime_zero_indicator(n: int, tolerance: float = 1e-8) -> int:
    """
    Return 1 when the prime-zero wave sum is numerically zero.

    This is a 0/1 wrapper around the zero condition Z_wave(n)=0.
    """
    if n < 2:
        return 0

    return 1 if abs(bach_prime_zero_wave_sum(n)) <= tolerance else 0


def bach_wave_prime_indicator_product(n: int, tolerance: float = 1e-8) -> int:
    """
    Return the wave-only Bach prime indicator Q_B(n).

    Q_B(n) = product_{m=2}^{n-1} (1 - W_m(n))

    The result is rounded to 0 or 1 with a tolerance because the waves are
    evaluated using floating-point complex exponentials.
    """
    if n < 2:
        return 0

    product = 1 + 0j

    for m in range(2, n):
        product *= 1 - bach_multiple_wave(m, n)

    return 1 if abs(product - 1) <= tolerance else 0


def bach_wave_prime_indicator(n: int, tolerance: float = 1e-8) -> int:
    """
    Return the primary 0/1 prime indicator derived from the zero wave sum.
    """
    return bach_wave_prime_indicator_sinc(n, tolerance=tolerance)


def bach_wave_prime_indicator_sinc(n: int, tolerance: float = 1e-8) -> int:
    """
    Return the sinc-wave indicator sinc(Z_wave(n)).

    Since Z_wave(n) is an integer at integer inputs, sinc(Z_wave(n)) equals 1
    when Z_wave(n)=0 and equals 0 for positive integer divisor counts.
    """
    if n < 2:
        return 0

    zero_sum = bach_prime_zero_wave_sum(n)

    if abs(zero_sum) <= tolerance:
        return 1

    sinc_value = cmath.sin(math.pi * zero_sum) / (math.pi * zero_sum)
    return 1 if abs(sinc_value - 1) <= tolerance else 0


def bach_wave_prime_count(x: float, tolerance: float = 1e-8) -> int:
    """
    Return the wave-only prime count B_pi(x).

    B_pi(x) = sum_{2 <= n <= floor(x)} sinc(Z_wave(n))
    """
    limit = math.floor(x)

    if limit < 2:
        return 0

    return sum(
        bach_wave_prime_indicator(n, tolerance=tolerance)
        for n in range(2, limit + 1)
    )


def bach_sinc_wave_prime_count(x: float, tolerance: float = 1e-8) -> int:
    """
    Backward-compatible explicit name for the sinc-wave prime count.
    """
    return bach_wave_prime_count(x, tolerance=tolerance)


def bach_product_wave_prime_count(x: float, tolerance: float = 1e-8) -> int:
    """
    Return the equivalent product-wave prime count.
    """
    limit = math.floor(x)

    if limit < 2:
        return 0

    return sum(
        bach_wave_prime_indicator_product(n, tolerance=tolerance)
        for n in range(2, limit + 1)
    )


def bach_wave_prime_count_values(
    limit: int, tolerance: float = 1e-8
) -> list[tuple[int, int]]:
    """
    Return (x, B_pi(x)) values for x = 0, 1, ..., limit.
    """
    if limit < 0:
        raise ValueError("limit must be nonnegative")

    values = []
    running_total = 0

    for n in range(limit + 1):
        running_total += bach_wave_prime_indicator(n, tolerance=tolerance)
        values.append((n, running_total))

    return values


KNOWN_PRIME_COUNTS = {
    0: 0,
    1: 0,
    2: 1,
    3: 2,
    4: 2,
    5: 3,
    10: 4,
    20: 8,
    30: 10,
    50: 15,
    100: 25,
}


def run_known_count_check(limit: int, tolerance: float = 1e-8) -> None:
    """
    Check wave counts against a small table of known pi(x) values.
    """
    for x, expected in KNOWN_PRIME_COUNTS.items():
        if x <= limit:
            actual = bach_wave_prime_count(x, tolerance=tolerance)
            if actual != expected:
                raise AssertionError(
                    f"B_pi({x}) mismatch: wave count={actual}, expected={expected}"
                )

            product_actual = bach_product_wave_prime_count(x, tolerance=tolerance)
            if product_actual != expected:
                raise AssertionError(
                    f"B_pi_product({x}) mismatch: "
                    f"product wave count={product_actual}, expected={expected}"
                )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate Bach prime indicators and counts using only waves."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Largest integer x to evaluate. Default: 30.",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-8,
        help="Floating-point tolerance for wave rounding. Default: 1e-8.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check computed wave counts against known small prime counts.",
    )
    parser.add_argument(
        "--table",
        action="store_true",
        help="Print n, Q_B(n), and B_pi(n) up to --limit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.limit < 0:
        raise ValueError("--limit must be nonnegative")

    if args.check:
        run_known_count_check(args.limit, tolerance=args.tolerance)
        print(f"Known-count wave check passed through x = {args.limit}.")

    if args.table:
        print("n  Z_wave(n)  P_wave(n)  B_pi(n)")
        print("---------------------------------")
        for n, count in bach_wave_prime_count_values(
            args.limit, tolerance=args.tolerance
        ):
            zero_sum = bach_prime_zero_wave_sum(n)
            zero_sum_int = round(zero_sum.real)
            indicator = bach_wave_prime_indicator(n, tolerance=args.tolerance)
            print(f"{n:2d} {zero_sum_int:10d} {indicator:10d} {count:8d}")
    else:
        count = bach_wave_prime_count(args.limit, tolerance=args.tolerance)
        print(f"B_pi({args.limit}) = {count}")


if __name__ == "__main__":
    main()
