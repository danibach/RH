import math

import matplotlib.pyplot as plt
import numpy as np


# Change these if you want a wider or denser plot.
X_MIN = -20.0
X_MAX = 80.0
SAMPLES_PER_UNIT = 120


def f_m(m, x):
    """
    Complex divisibility wave:

        f_m(x) = (1 / m) * sum_{j=0}^{m-1} exp(2*pi*i*j*x/m)

    At integer n:
        f_m(n) = 1 if m divides n
        f_m(n) = 0 otherwise

    For real x, this is a complex-valued wave.
    """
    x = np.asarray(x, dtype=float)
    total = np.zeros_like(x, dtype=complex)

    for j in range(m):
        total += np.exp(2j * np.pi * j * x / m)

    return total / m


def bach_formula(x):
    """
    Real-extension of Bach's formula:

        B(x) = sum_{m=2}^{floor(x)-1} f_m(x)

    At every integer n >= 2, this equals the original formula:

        B(n) = sum_{m=2}^{n-1} f_m(n)

    Therefore, at integer n >= 2:
        B(n) = 0 if and only if n is prime.

    For x < 3, the sum is empty, so this returns 0.
    """
    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x, dtype=complex)

    # The largest possible m needed anywhere in the plot.
    max_m = int(math.floor(np.max(x))) - 1

    if max_m < 2:
        return result

    for m in range(2, max_m + 1):
        active = np.floor(x) >= m + 1
        result += np.where(active, f_m(m, x), 0)

    return result


def bach_formula_at_integer(n):
    """
    Numerically stable exact integer version.

    This avoids tiny floating-point errors when identifying primes.
    """
    if n < 2:
        return None

    count = 0

    for m in range(2, n):
        if n % m == 0:
            count += 1

    return count


def is_prime(n):
    """
    Standard convention:
    primes are positive integers greater than 1.

    Negative numbers are not primes in the usual definition.
    """
    if n < 2:
        return False

    for m in range(2, int(math.sqrt(n)) + 1):
        if n % m == 0:
            return False

    return True


def main():
    sample_count = int((X_MAX - X_MIN) * SAMPLES_PER_UNIT) + 1
    x = np.linspace(X_MIN, X_MAX, sample_count)
    z = bach_formula(x)

    integer_min = math.ceil(X_MIN)
    integer_max = math.floor(X_MAX)
    integers = np.arange(integer_min, integer_max + 1)

    positive_integers = np.array([n for n in integers if n >= 2])
    primes = np.array([n for n in positive_integers if is_prime(n)])
    composites = np.array([n for n in positive_integers if n > 1 and not is_prime(n)])

    prime_values = np.array([bach_formula_at_integer(int(n)) for n in primes])
    composite_values = np.array([bach_formula_at_integer(int(n)) for n in composites])

    fig, axes = plt.subplots(3, 1, figsize=(16, 10), sharex=True)

    axes[0].plot(x, z.real, color="royalblue", linewidth=1.2)
    axes[0].scatter(primes, prime_values, color="red", s=45, zorder=5, label="primes")
    axes[0].scatter(composites, composite_values, color="black", s=20, zorder=4, label="composites")
    axes[0].axhline(0, color="gray", linewidth=1)
    axes[0].set_ylabel("Re B(x)")
    axes[0].set_title("Bach's Formula Extended to Real x")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(x, z.imag, color="darkorange", linewidth=1.2)
    axes[1].axhline(0, color="gray", linewidth=1)
    axes[1].set_ylabel("Im B(x)")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(x, np.abs(z), color="seagreen", linewidth=1.2)
    axes[2].scatter(primes, np.zeros_like(primes), color="red", s=45, zorder=5)
    axes[2].axhline(0, color="gray", linewidth=1)
    axes[2].set_xlabel("real x")
    axes[2].set_ylabel("|B(x)|")
    axes[2].grid(True, alpha=0.3)

    for p in primes:
        axes[2].text(p, -0.08, str(p), ha="center", va="top", fontsize=8, color="red")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
