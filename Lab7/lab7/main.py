import random
import secrets
from EllipticCurvePoint import EllipticCurvePoint  # Импортируем ваш класс из файла
import ElGamal  # Импортируем ваш класс ElGamal из другого файла (если используется)


def main():
    p = generate_prime(509, 512)
    q = generate_prime(254, 256)

    while not is_condition_met(p, q):
        p = generate_prime(509, 512)
        q = generate_prime(254, 256)

    print("Generated prime p:", p)
    print("Generated prime q:", q)
    print("Condition (p - 1) & q == 0 is met.")

    # Здесь можно добавить код для работы с EllipticCurvePoint или ElGamal, если они должны быть использованы


def generate_prime(min_bits: int, max_bits: int) -> int:
    """Генерация простого числа с использованием вероятностной проверки."""
    bit_length = random.randint(min_bits, max_bits)
    while True:
        prime = generate_random_big_integer(bit_length)
        if is_probably_prime(prime):
            return prime


def generate_random_big_integer(bit_length: int) -> int:
    """Генерация случайного большого целого числа с заданной длиной в битах."""
    bytes_length = (bit_length + 7) // 8
    random_bytes = secrets.token_bytes(bytes_length)
    number = int.from_bytes(random_bytes, byteorder='big')

    # Установка старшего бита для обеспечения заданного диапазона
    number |= (1 << (bit_length - 1))
    return number


def is_probably_prime(number: int, certainty: int = 20) -> bool:
    """Проверка числа на простоту с использованием теста Миллера-Рабина."""
    if number < 2:
        return False
    if number in (2, 3):
        return True
    if number % 2 == 0:
        return False

    # Преобразование числа для Миллера-Рабина
    d = number - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(certainty):
        if not miller_rabin_test(number, d, r):
            return False
    return True


def miller_rabin_test(n: int, d: int, r: int) -> bool:
    """Один раунд теста Миллера-Рабина для проверки числа на простоту."""
    a = generate_random_big_integer_in_range(2, n - 2)
    x = pow(a, d, n)

    if x == 1 or x == n - 1:
        return True

    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False


def generate_random_big_integer_in_range(min_val: int, max_val: int) -> int:
    """Генерация случайного числа в заданном диапазоне."""
    while True:
        number = generate_random_big_integer(max_val.bit_length())
        if min_val <= number <= max_val:
            return number


def is_condition_met(p: int, q: int) -> bool:
    """Проверка выполнения условия (p - 1) & q == 0."""
    return ((p - 1) & q) == 0


if __name__ == "__main__":
    main()
