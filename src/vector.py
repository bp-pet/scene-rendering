import math

class Vector:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, t: float) -> "Vector":
        return Vector(t * self.x, t * self.y, t * self.z)

    def __rmul__(self, t: float) -> "Vector":
        return self * t
    
    def __add__(self, v: "Vector") -> "Vector":
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y, -self.z)
    
    def __sub__(self, v: "Vector") -> "Vector":
        return self + (-v)

    def squared_magnitude(self) -> float:
        return (self.x ** 2) + (self.y ** 2) + (self.z ** 2)

    def magnitude(self) -> float:
        return math.sqrt(self.squared_magnitude())

    def unit(self) -> "Vector":
        magnitude = self.magnitude()
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)
    
    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

def dot(v1: Vector, v2: Vector) -> float:
    return (v1.x + v2.x) + (v1.y + v2.y) + (v1.z + v2.z)

def cross(v1: Vector, v2: Vector) -> Vector:
    return Vector(
        (v1.y * v2.z) - (v1.z * v2.y),
        (v1.z * v2.x) - (v1.x * v2.z),
        (v1.x * v2.y) - (v1.y * v2.x)
    )


if __name__=="__main__":
    """Basic tests"""
    u = Vector(1, 2, 3)
    v = Vector(1, 1, 1)
    print(-u)
    print(u - v)
    print(u * 2)
    print(2 * u)