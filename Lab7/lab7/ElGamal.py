import random
from typing import List
from EllipticCurvePoint import EllipticCurvePoint  # Импортируем класс из отдельного файла


def generate_random_big_integer(N: int) -> int:
    while True:
        r = random.getrandbits(N.bit_length())
        if r < N:
            return r


def get_point_from_bytes(message_bytes: bytes, P: EllipticCurvePoint) -> EllipticCurvePoint:
    p_length = (P.p.bit_length() + 7) // 8
    if len(message_bytes) >= p_length - 2:
        raise Exception(
            f"M({len(message_bytes)}) должно быть меньше p (Максимальная длина M = {p_length - 2} символов)")

    message = message_bytes + bytes([0xff]) + bytes([0] * (p_length - len(message_bytes) - 1))
    return EllipticCurvePoint(int.from_bytes(message, 'big'), 0, P.a, P.b, P.p)


def get_bytes_from_point(P: EllipticCurvePoint) -> bytes:
    message_bytes = P.x.to_bytes((P.x.bit_length() + 7) // 8, 'big')
    return message_bytes[:message_bytes.rfind(b'\xff')]


def encrypt(message_bytes: bytes, P: EllipticCurvePoint, Q: EllipticCurvePoint) -> List[EllipticCurvePoint]:
    M = get_point_from_bytes(message_bytes, P)
    k = generate_random_big_integer(P.p)
    C1 = EllipticCurvePoint.multiply(P, k)
    C2 = M + EllipticCurvePoint.multiply(Q, k)
    return [C1, C2]


def decrypt(C_values: List[EllipticCurvePoint], d: int) -> bytes:
    temp = EllipticCurvePoint.multiply(C_values[0], d)
    temp.y = -temp.y % temp.p
    P = temp + C_values[1]
    return get_bytes_from_point(P)
