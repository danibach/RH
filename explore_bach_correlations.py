"""
Explore the lcm-grouped correlation expansion of the Bach prime indicator.

The Bach prime indicator is

    Q_B(n) = product_{m=2}^{n-1} (1 - D_m(n)),

where D_m(n) is 1 when m divides n and 0 otherwise.

Expanding the product gives subset correlations:

    Q_B(n) = sum_S (-1)^|S| D_lcm(S)(n).

This script groups the subset terms by lcm(S), so you can see the Mobius-like
coefficients and the cancellation that makes composites vanish.

Python: 3.9+
No third-party dependencies.
"""

import argparse
import math


def mobius(n):
    """Return the Mobius function mu(n)."""
    if n == 1:
        return 1

    result = 1
    remaining = n
    p = 2

    while p * p <= remaining:
        if remaining % p == 0:
            remaining //= p
            result *= -1

            if remaining % p == 0:
                return 0

            while remaining % p == 0:
                remaining //= p

        p += 1 if p == 2 else 2

    if remaining > 1:
        result *= -1

    return result


def is_prime(n):
    if n < 2:
        return False

    for d in range(2, int(math.sqrt(n)) + 1):
        if n % d == 0:
            return False

    return True


def primes_up_to(limit):
    return [n for n in range(2, limit + 1) if is_prime(n)]


def prime_count_exact(limit):
    return sum(1 for n in range(2, limit + 1) if is_prime(n))


def divisors(n):
    values = []
    for d in range(1, int(math.sqrt(n)) + 1):
        if n % d == 0:
            values.append(d)
            if d * d != n:
                values.append(n // d)
    return sorted(values)


def lcm(a, b):
    return a * b // math.gcd(a, b)


def lcm_coefficients_up_to(max_m):
    """
    Group prod_{m=2}^{max_m}(1 - D_m) by LCM frequency.

    This is the global cutoff coefficient F_M(q), unlike
    bach_lcm_coefficients_for_n(n), which first removes waves that cannot
    contribute at the evaluated integer n.
    """
    coeffs = {1: 1}

    for m in range(2, max_m + 1):
        updated = dict(coeffs)

        for q, coefficient in coeffs.items():
            new_q = lcm(q, m)
            updated[new_q] = updated.get(new_q, 0) - coefficient

        coeffs = {q: c for q, c in updated.items() if c != 0}

    return coeffs


def lcm_cutoff_layers(max_m):
    """
    Return incremental cutoff layers G_M(q)=F_M(q)-F_{M-1}(q).

    G_1(1)=1 represents the empty subset. For M>=2, G_M(q) groups exactly
    the subset correlations whose largest selected wave index is M.
    """
    layers = [(1, {1: 1})]
    previous = {1: 1}

    for m in range(2, max_m + 1):
        current = dict(previous)

        for q, coefficient in previous.items():
            new_q = lcm(q, m)
            current[new_q] = current.get(new_q, 0) - coefficient

        current = {q: c for q, c in current.items() if c != 0}
        delta = {q: current.get(q, 0) - previous.get(q, 0) for q in current}

        for q in previous:
            if q not in current:
                delta[q] = -previous[q]

        delta = {q: c for q, c in delta.items() if c != 0}
        layers.append((m, delta))
        previous = current

    return layers


def bach_indicator_from_global_cutoff(n):
    """
    Evaluate Q_B(n) from the global cutoff coefficients F_{n-1}(q).
    """
    if n < 2:
        return 0

    coeffs = lcm_coefficients_up_to(n - 1)
    return sum(coefficient for q, coefficient in coeffs.items() if n % q == 0)


def layer_value_at_n(layer, n):
    return sum(coefficient for q, coefficient in layer.items() if n % q == 0)


def bach_lcm_coefficients_for_n(n):
    """
    Group the Bach product expansion by lcm for a fixed evaluated integer n.

    Terms m that do not divide n cannot contribute to Q_B(n), because their
    lcm correlation will not divide n. So we only need proper divisors of n.
    """
    coeffs = {1: 1}
    proper_divisors = [d for d in divisors(n) if 2 <= d < n]

    for d in proper_divisors:
        updated = dict(coeffs)

        for q, coefficient in coeffs.items():
            new_q = lcm(q, d)
            updated[new_q] = updated.get(new_q, 0) - coefficient

        coeffs = {q: c for q, c in updated.items() if c != 0}

    return coeffs


def bach_indicator_from_coefficients(n):
    coeffs = bach_lcm_coefficients_for_n(n)
    return sum(coefficient for q, coefficient in coeffs.items() if n % q == 0)


def verify_lcm_identities(limit):
    """
    Verify the finite LCM-correlation identities up to `limit`.

    This checks:
      1. The coefficient-derived indicator equals the prime indicator.
      2. Contributing coefficients below n match mu(q).
      3. The top coefficient at q=n matches mu(n) for composites.
    """
    for n in range(2, limit + 1):
        coeffs = bach_lcm_coefficients_for_n(n)
        expected_indicator = 1 if is_prime(n) else 0
        actual_indicator = bach_indicator_from_coefficients(n)

        if actual_indicator != expected_indicator:
            raise AssertionError(
                f"Q_B({n}) mismatch: {actual_indicator} != {expected_indicator}"
            )

        for q, coefficient in coeffs.items():
            if q < n and coefficient != mobius(q):
                raise AssertionError(
                    f"C_{n}({q}) mismatch: {coefficient} != mu({q})={mobius(q)}"
                )

        if not is_prime(n):
            top_coefficient = coeffs.get(n, 0)
            expected_top = mobius(n)
            if top_coefficient != expected_top:
                raise AssertionError(
                    f"C_{n}({n}) mismatch: "
                    f"{top_coefficient} != mu({n})={expected_top}"
                )


def verify_global_cutoff_identities(limit):
    """
    Verify identities for the global cutoff coefficients F_M(q).

    This checks:
      1. F_{n-1} gives the same Q_B(n) indicator.
      2. F_M(q)=mu(q) for q<=M.
    """
    for n in range(2, limit + 1):
        actual_indicator = bach_indicator_from_global_cutoff(n)
        expected_indicator = 1 if is_prime(n) else 0

        if actual_indicator != expected_indicator:
            raise AssertionError(
                f"Global cutoff Q_B({n}) mismatch: "
                f"{actual_indicator} != {expected_indicator}"
            )

    for max_m in range(1, limit + 1):
        coeffs = lcm_coefficients_up_to(max_m)

        for q in range(1, max_m + 1):
            coefficient = coeffs.get(q, 0)
            expected = mobius(q)

            if coefficient != expected:
                raise AssertionError(
                    f"F_{max_m}({q}) mismatch: "
                    f"{coefficient} != mu({q})={expected}"
                )


def verify_prime_layer_compression(limit):
    """
    Verify that cutoff layers only change at prime M.

    For prime M=p, the layer consists exactly of squarefree q built from
    primes <= p and divisible by p, with coefficient mu(q). For composite M,
    the layer is empty.
    """
    for max_m, layer in lcm_cutoff_layers(limit):
        if max_m == 1:
            if layer != {1: 1}:
                raise AssertionError(f"G_1 mismatch: {layer}")
            continue

        if not is_prime(max_m):
            if layer:
                raise AssertionError(f"Composite layer G_{max_m} is not empty")
            continue

        expected = {
            d: mobius(d)
            for d, _mu in squarefree_divisors_with_mu(primes_up_to(max_m))
            if d > 1 and d % max_m == 0
        }

        if layer != expected:
            raise AssertionError(
                f"Prime layer G_{max_m} mismatch: {layer} != {expected}"
            )


def least_prime_factor(n):
    if n < 2:
        return 0

    for p in range(2, int(math.sqrt(n)) + 1):
        if n % p == 0 and is_prime(p):
            return p

    return n


def verify_least_prime_factor_layers(limit):
    """
    Verify that prime cutoff layers remove least-prime-factor classes.

    At integer n, the layer G_p contributes -1 exactly when p is the least
    prime factor of n and p<n. This gives:

        Q_B(n) = 1 + sum_{p<n} G_p(n).
    """
    for n in range(2, limit + 1):
        running_value = 1
        lpf = least_prime_factor(n)

        for p in primes_up_to(n - 1):
            value = -1 if lpf == p else 0
            expected = -1 if lpf == p else 0

            if value != expected:
                raise AssertionError(
                    f"Least-prime layer mismatch at n={n}, p={p}: "
                    f"{value} != {expected}"
                )

            running_value += value

        expected_indicator = 1 if is_prime(n) else 0
        if running_value != expected_indicator:
            raise AssertionError(
                f"Least-prime decomposition mismatch at n={n}: "
                f"{running_value} != {expected_indicator}"
            )


def bach_prime_zeta_finite_direct(s, n_limit):
    """
    Finite direct sum sum_{2<=n<=N} Q_B(n)n^{-s}.
    """
    return sum(
        bach_indicator_from_global_cutoff(n) * n ** (-s)
        for n in range(2, n_limit + 1)
    )


def bach_prime_zeta_finite_lcm_max(s, n_limit):
    """
    Finite swapped sum using LCM/max cutoff layers.

    F_{n-1}(q) is written as sum_{M<n} G_M(q), so:

        sum_{n<=N} Q_B(n)n^{-s}
        =
        sum_{M<N} sum_q G_M(q) sum_{M<n<=N, q|n} n^{-s}.
    """
    total = 0

    for max_m, layer in lcm_cutoff_layers(n_limit - 1):
        n_start = max(2, max_m + 1)

        for q, coefficient in layer.items():
            for n in range(n_start, n_limit + 1):
                if n % q == 0:
                    total += coefficient * n ** (-s)

    return total


def verify_lcm_max_dirichlet_swap(n_limit, s=2.0, tolerance=1e-12):
    direct = bach_prime_zeta_finite_direct(s, n_limit)
    swapped = bach_prime_zeta_finite_lcm_max(s, n_limit)

    if abs(direct - swapped) > tolerance:
        raise AssertionError(
            f"Finite LCM/max Dirichlet swap mismatch: "
            f"direct={direct}, swapped={swapped}"
        )


def squarefree_divisors_with_mu(primes):
    """
    Return (d, mu(d)) for all squarefree d built from the supplied primes.
    """
    values = [(1, 1)]

    for p in primes:
        values += [(d * p, -mu) for d, mu in list(values)]

    return values


def phi_legendre_from_prime_waves(x, z):
    """
    Count integers <= x not hit by any prime wave D_p with p <= z.

    This is the expanded prime-wave compression:

        Phi(x,z) = sum_{d|P(z)} mu(d) floor(x/d).
    """
    primes = primes_up_to(z)
    return sum(
        mu * (x // d)
        for d, mu in squarefree_divisors_with_mu(primes)
    )


def legendre_bach_prime_count(x):
    """
    Exact Legendre count reached from the prime-wave compression.
    """
    root = math.isqrt(x)
    return prime_count_exact(root) - 1 + phi_legendre_from_prime_waves(x, root)


def print_legendre_check(x):
    root = math.isqrt(x)
    phi_value = phi_legendre_from_prime_waves(x, root)
    legendre_value = legendre_bach_prime_count(x)
    exact_value = prime_count_exact(x)

    print(f"\nLegendre/Bach prime-wave compression at x = {x}")
    print()
    print(f"sqrt cutoff             = {root}")
    print(f"Phi(x, sqrt(x))         = {phi_value}")
    print(f"pi(sqrt(x)) - 1 + Phi   = {legendre_value}")
    print(f"exact pi(x)             = {exact_value}")

    if legendre_value != exact_value:
        raise AssertionError(
            f"Legendre/Bach count mismatch at x={x}: "
            f"{legendre_value} != {exact_value}"
        )


def theta_bach(limit):
    total = 0.0
    values = []

    for n in range(2, limit + 1):
        if bach_indicator_from_coefficients(n) == 1:
            total += math.log(n)
        values.append((n, total, total - n))

    return values


def print_coefficients(n):
    coeffs = bach_lcm_coefficients_for_n(n)
    q_width = max(3, len(str(max(coeffs))))

    print(f"\nBach lcm-correlation expansion for n = {n}")
    print(f"prime? {is_prime(n)}")
    print()
    print(f"{'q':>{q_width}}  {'C_n(q)':>8}  {'mu(q)':>6}  {'q|n':>4}")
    print("-" * (q_width + 26))

    for q in sorted(coeffs):
        divides = "yes" if n % q == 0 else "no"
        print(f"{q:>{q_width}}  {coeffs[q]:>8}  {mobius(q):>6}  {divides:>4}")

    total = bach_indicator_from_coefficients(n)
    print("-" * (q_width + 26))
    print(f"Q_B({n}) = {total}")


def print_cutoff_layer_summary(max_m):
    print(f"\nLCM/max cutoff-layer summary through M = {max_m}")
    print()
    print(
        f"{'M':>4}  {'terms':>7}  {'sum |G_M|':>11}  "
        f"{'max |G_M|':>11}  {'max q':>10}"
    )
    print("-" * 53)

    for m, layer in lcm_cutoff_layers(max_m):
        terms = len(layer)
        absolute_sum = sum(abs(c) for c in layer.values())
        max_abs = max((abs(c) for c in layer.values()), default=0)
        max_q = max(layer, default=0)
        print(f"{m:>4}  {terms:>7}  {absolute_sum:>11}  {max_abs:>11}  {max_q:>10}")


def print_theta_table(limit):
    print(f"\nWeighted Bach count theta_B(x) up to x = {limit}")
    print()
    print(f"{'x':>6}  {'theta_B(x)':>14}  {'theta_B(x)-x':>16}  {'sqrt(x)log^2(x)':>18}")
    print("-" * 62)

    checkpoints = set()
    step = max(1, limit // 12)
    for x in range(step, limit + 1, step):
        checkpoints.add(x)
    checkpoints.add(limit)

    for x, theta, error in theta_bach(limit):
        if x in checkpoints:
            scale = math.sqrt(x) * math.log(x) ** 2
            print(f"{x:>6}  {theta:>14.6f}  {error:>16.6f}  {scale:>18.6f}")


def main():
    parser = argparse.ArgumentParser(
        description="Explore Bach product lcm-correlation coefficients."
    )
    parser.add_argument(
        "--n",
        type=int,
        default=30,
        help="Integer n whose Bach correlation expansion should be printed.",
    )
    parser.add_argument(
        "--theta-limit",
        type=int,
        default=100,
        help="Limit for the theta_B(x) error table.",
    )
    parser.add_argument(
        "--verify-limit",
        type=int,
        default=0,
        help="If positive, verify LCM-correlation identities up to this limit.",
    )
    parser.add_argument(
        "--legendre-x",
        type=int,
        default=0,
        help="If positive, verify the Legendre/Bach prime-wave count at x.",
    )
    parser.add_argument(
        "--layer-max",
        type=int,
        default=0,
        help="If positive, print the LCM/max cutoff-layer summary through M.",
    )
    parser.add_argument(
        "--verify-global-limit",
        type=int,
        default=0,
        help="If positive, verify global cutoff identities up to this limit.",
    )
    parser.add_argument(
        "--verify-layer-limit",
        type=int,
        default=0,
        help="If positive, verify prime-layer compression up to this limit.",
    )
    parser.add_argument(
        "--verify-least-factor-limit",
        type=int,
        default=0,
        help="If positive, verify least-prime-factor layer decomposition.",
    )
    parser.add_argument(
        "--dirichlet-swap-limit",
        type=int,
        default=0,
        help="If positive, verify finite LCM/max Dirichlet swapping up to N.",
    )
    args, _unknown_args = parser.parse_known_args()

    if args.n < 2:
        raise ValueError("--n must be at least 2")

    if args.theta_limit < 2:
        raise ValueError("--theta-limit must be at least 2")
    if args.verify_limit < 0:
        raise ValueError("--verify-limit must be nonnegative")
    if args.legendre_x < 0:
        raise ValueError("--legendre-x must be nonnegative")
    if args.layer_max < 0:
        raise ValueError("--layer-max must be nonnegative")
    if args.verify_global_limit < 0:
        raise ValueError("--verify-global-limit must be nonnegative")
    if args.verify_layer_limit < 0:
        raise ValueError("--verify-layer-limit must be nonnegative")
    if args.verify_least_factor_limit < 0:
        raise ValueError("--verify-least-factor-limit must be nonnegative")
    if args.dirichlet_swap_limit < 0:
        raise ValueError("--dirichlet-swap-limit must be nonnegative")

    if args.verify_limit:
        verify_lcm_identities(args.verify_limit)
        print(f"LCM-correlation identities verified through n = {args.verify_limit}.")

    if args.verify_global_limit:
        verify_global_cutoff_identities(args.verify_global_limit)
        print(
            "Global cutoff identities verified through "
            f"n = {args.verify_global_limit}."
        )

    if args.verify_layer_limit:
        verify_prime_layer_compression(args.verify_layer_limit)
        print(
            "Prime-layer compression verified through "
            f"M = {args.verify_layer_limit}."
        )

    if args.verify_least_factor_limit:
        verify_least_prime_factor_layers(args.verify_least_factor_limit)
        print(
            "Least-prime-factor layer decomposition verified through "
            f"n = {args.verify_least_factor_limit}."
        )

    if args.dirichlet_swap_limit:
        verify_lcm_max_dirichlet_swap(args.dirichlet_swap_limit)
        print(
            "Finite LCM/max Dirichlet swap verified through "
            f"N = {args.dirichlet_swap_limit}."
        )

    if args.legendre_x:
        print_legendre_check(args.legendre_x)

    if args.layer_max:
        print_cutoff_layer_summary(args.layer_max)

    print_coefficients(args.n)
    print_theta_table(args.theta_limit)


if __name__ == "__main__":
    main()
