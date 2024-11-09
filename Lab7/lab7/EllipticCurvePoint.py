from dataclasses import dataclass
from sympy import mod_inverse

@dataclass
class EllipticCurvePoint:
    x: int
    y: int
    a: int
    b: int
    p: int

    def __add__(self, other):
        if self.p != other.p:
            raise ValueError("Points are not on the same curve")

        if self.x == other.x and self.y == other.y:
            return self.double_value()

        dy = (other.y - self.y) % self.p
        dx = (other.x - self.x) % self.p

        m = (dy * mod_inverse(dx, self.p)) % self.p

        x3 = (m * m - self.x - other.x) % self.p
        y3 = (m * (self.x - x3) - self.y) % self.p

        return EllipticCurvePoint(x3, y3, self.a, self.b, self.p)

    def double_value(self):
        dy = (3 * self.x * self.x + self.a) % self.p
        dx = (2 * self.y) % self.p

        m = (dy * mod_inverse(dx, self.p)) % self.p

        x3 = (m * m - 2 * self.x) % self.p
        y3 = (m * (self.x - x3) - self.y) % self.p

        return EllipticCurvePoint(x3, y3, self.a, self.b, self.p)

    @staticmethod
    def multiply(point, k):
        result = None
        addend = point

        while k:
            if k & 1:
                result = addend if result is None else result + addend
            addend = addend.double_value()
            k >>= 1

        return result
