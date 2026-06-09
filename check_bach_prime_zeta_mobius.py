"""
Numerically check the Bach/prime-zeta Mobius inversion identity.

For Re(s)>1, the Bach prime-zeta transform is

    P_B(s) = sum_p p^(-s).

Euler product algebra gives

    P_B(s) = sum_{k>=1} mu(k)/k * log(zeta(k*s)).

This script compares a finite prime sum with a finite Mobius-log-zeta sum
where both are directly meaningful. It also prints diagnostic samples near the
expected singularity at s=1 and near the first critical-line zeta zero.

These are numerical diagnostics only. They do not prove or disprove RH.
"""

from __future__ import annotations

import argparse
import cmath
import math

import mpmath as mp


def prime_flags(limit: int) -> list[bool]:
    if limit < 2:
        return [False] * (limit + 1)

    flags = [True] * (limit + 1)
    flags[0] = False
    flags[1] = False

    for p in range(2, int(math.sqrt(limit)) + 1):
        if flags[p]:
            for multiple in range(p * p, limit + 1, p):
                flags[multiple] = False

    return flags


def primes_up_to(limit: int) -> list[int]:
    flags = prime_flags(limit)
    return [n for n in range(2, limit + 1) if flags[n]]


def mobius_values(limit: int) -> list[int]:
    mu = [1] * (limit + 1)
    is_prime = [True] * (limit + 1)
    mu[0] = 0

    for p in range(2, limit + 1):
        if is_prime[p]:
            for multiple in range(p, limit + 1, p):
                is_prime[multiple] = False
                mu[multiple] *= -1
            square = p * p
            for multiple in range(square, limit + 1, square):
                mu[multiple] = 0

    return mu


def prime_zeta_partial(s: complex, prime_limit: int) -> complex:
    total = 0j

    for p in primes_up_to(prime_limit):
        total += cmath.exp(-s * math.log(p))

    return total


def prime_zeta_mobius(s: complex, k_limit: int, precision: int) -> complex:
    mp.mp.dps = precision
    mu = mobius_values(k_limit)
    s_mp = mp.mpc(s.real, s.imag)
    total = mp.mpc(0)

    for k in range(1, k_limit + 1):
        if mu[k] == 0:
            continue
        total += mp.mpf(mu[k]) / k * mp.log(mp.zeta(k * s_mp))

    return complex(total)


def print_identity_check(args: argparse.Namespace) -> None:
    s = complex(args.sigma, args.t)
    direct = prime_zeta_partial(s, args.prime_limit)
    mobius = prime_zeta_mobius(s, args.k_limit, args.precision)
    difference = direct - mobius

    print("Identity check in Re(s)>1")
    print(f"s                         = {s}")
    print(f"prime cutoff              = {args.prime_limit}")
    print(f"Mobius k cutoff           = {args.k_limit}")
    print(f"partial sum_p p^-s        = {direct:.16g}")
    print(f"partial Mobius-log-zeta   = {mobius:.16g}")
    print(f"difference                = {difference:.6g}")
    print(f"|difference|              = {abs(difference):.6g}")


def print_singularity_probe(args: argparse.Namespace) -> None:
    print()
    print("Singularity diagnostics from the Mobius-log-zeta side")
    print("These use zeta directly and are diagnostics, not proof.")

    print()
    print("Approach s=1 from the right:")
    for epsilon in [1e-1, 1e-2, 1e-3, 1e-4]:
        s = complex(1.0 + epsilon, 0.0)
        value = prime_zeta_mobius(s, args.k_limit, args.precision)
        print(f"  s={s.real:.4f}: Re={value.real: .8f}, Im={value.imag: .8f}")

    zero = mp.zetazero(1)
    gamma = float(mp.im(zero))

    print()
    print(f"Approach first critical-line zero rho=1/2+i*{gamma:.12f} from the right:")
    for epsilon in [1e-1, 1e-2, 1e-3, 1e-4]:
        s = complex(0.5 + epsilon, gamma)
        value = prime_zeta_mobius(s, args.k_limit, args.precision)
        print(
            f"  sigma={s.real:.4f}: "
            f"Re={value.real: .8f}, Im={value.imag: .8f}, |value|={abs(value):.8f}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check P_B(s)=sum mu(k)/k log(zeta(k*s)) numerically."
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=1.35,
        help="Real part for the Re(s)>1 identity check. Default: 1.35.",
    )
    parser.add_argument(
        "--t",
        type=float,
        default=7.0,
        help="Imaginary part for the Re(s)>1 identity check. Default: 7.",
    )
    parser.add_argument(
        "--prime-limit",
        type=int,
        default=200000,
        help="Prime cutoff for direct sum_p p^-s. Default: 200000.",
    )
    parser.add_argument(
        "--k-limit",
        type=int,
        default=40,
        help="Mobius inversion cutoff. Default: 40.",
    )
    parser.add_argument(
        "--precision",
        type=int,
        default=50,
        help="mpmath decimal precision. Default: 50.",
    )
    parser.add_argument(
        "--skip-probe",
        action="store_true",
        help="Only run the Re(s)>1 identity check.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.sigma <= 1:
        raise ValueError("--sigma must be greater than 1 for the direct check")
    if args.prime_limit < 10:
        raise ValueError("--prime-limit must be at least 10")
    if args.k_limit < 1:
        raise ValueError("--k-limit must be at least 1")

    print_identity_check(args)

    if not args.skip_probe:
        print_singularity_probe(args)


if __name__ == "__main__":
    main()
