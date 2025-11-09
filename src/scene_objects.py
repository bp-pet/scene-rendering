import math

from src.vector import Vector

class SceneObject:
    def intersect_ray(self, p: Vector, v: Vector) -> float | None:
        pass


class Sphere(SceneObject):
    def __init__(self, center: Vector, radius: float, color=tuple[float]):
        self.center = center
        self.radius = radius
        self.color = color

    def __str__(self):
        return f"Sphere with center {self.center}, radius {self.radius}, color {self.color}"
    
    def intersect_ray(self, p: Vector, v: Vector) -> float | None:
        """Given a ray with origin p and direction v, find the
        distance to the intersection, or return None if there isn't one.

        Returns the t value if t > 1, where the ray is defined by p + t * v.

        Derivation:
        
        (p.x + t * v.x - x0) ** 2
        + (p.y + t * v.y - y0) ** 2
        + (p.z + t * v.z - z0) ** 2
        = r ** 2
        
        (vx ** 2 + vy ** 2 + vz ** 2) * t ** 2
        + 2 * ((px - x0) * vx + (py - y0) * vy + (pz - z0) * vz) * t
        + (px - x0) ** 2  + (py - y0) ** 2 + (pz - z0) ** 2 - r ** 2

        Use abc formula.
        """
        x0 = self.center.x
        y0 = self.center.y
        z0 = self.center.z
        r = self.radius

        a = (v.x ** 2 + v.y ** 2 + v.z ** 2)
        b = 2 * ((p.x - x0) * v.x + (p.y - y0) * v.y + (p.z - z0) * v.z)
        c = (p.x - x0) ** 2  + (p.y - y0) ** 2 + (p.z - z0) ** 2 - r ** 2

        if a == 0:
            return -c / b
        
        D = b ** 2 - 4 * a * c

        if D < 0:
            return None
        
        sqrtD = math.sqrt(D)
        
        t1 = (-b + sqrtD) / (2 * a)
        t2 = (-b - sqrtD) / (2 * a)

        t =  min(max(t1, 1), max(t2, 1))

        return t if t > 1 else None
