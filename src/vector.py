import math
import random
from typing import Self


class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, t: float) -> Self:
        return self.__class__(t * self.x, t * self.y, t * self.z)

    def __rmul__(self, t: float) -> Self:
        return self * t

    def __add__(self, v: Self) -> Self:
        return self.__class__(self.x + v.x, self.y + v.y, self.z + v.z)

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    def __sub__(self, v: Self) -> Self:
        return self + (-v)

    def squared_magnitude(self) -> float:
        return (self.x**2) + (self.y**2) + (self.z**2)

    def magnitude(self) -> float:
        return math.sqrt(self.squared_magnitude())

    def unit(self) -> Self:
        magnitude = self.magnitude()
        return self.__class__(
            self.x / magnitude, self.y / magnitude, self.z / magnitude
        )

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"


def dot(v1: Vector, v2: Vector) -> float:
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)


def cross(v1: Vector, v2: Vector) -> Vector:
    return Vector(
        (v1.y * v2.z) - (v1.z * v2.y),
        (v1.z * v2.x) - (v1.x * v2.z),
        (v1.x * v2.y) - (v1.y * v2.x),
    )


def proj(source_vector: Vector, project_onto_vector: Vector) -> Vector:
    return (
        dot(source_vector, project_onto_vector)
        / project_onto_vector.squared_magnitude()
        * project_onto_vector
    )


def reflect_around(source_vector: Vector, reflect_around_vector: Vector) -> Vector:
    return 2 * proj(source_vector, reflect_around_vector) - source_vector


def random_vector_in_hemisphere(normal: Vector) -> Vector:
    """Pick random vectors uniformly in unit cube until one is found
    that is in the unit sphere and poining in same direction (same hemisphere as)
    the given vector."""
    while True:
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        z = random.random() * 2 - 1
        candidate = Vector(x, y, z)
        magnitude = candidate.magnitude()
        if magnitude > 1:
            continue
        if dot(candidate, normal) < 0:
            continue
        return candidate


def linear_interpolation(v1: Vector, v2: Vector, k: float) -> Vector:
    """If k = 0 return v1, if k = 1 return v2, linearly interpolate inbetween."""
    assert 0 <= k <= 1
    return v1 * (1 - k) + v2 * k


if __name__ == "__main__":
    """Basic tests"""
    u = Vector(1, 2, 3)
    v = Vector(1, 1, 1)
    print(-u)
    print(u - v)
    print(u * 2)
    print(2 * u)

    print(u.unit().magnitude())
    print(v.unit().magnitude())
    print(dot(u.unit(), v.unit()))

    w = Vector(1, 0, 0)
    x = Vector(1, 1, 0)
    print(reflect_around(w, x))

    r = random_vector_in_hemisphere(Vector(0, 0, 1))
    print(r)
