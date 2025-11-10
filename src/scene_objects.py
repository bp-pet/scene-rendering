import math
import numpy as np

from src.vector import Vector, dot


class SceneObject:
    def intersect_ray(
        self, p: Vector, v: Vector, t_min: float, t_max: float
    ) -> float | None:
        pass

    def get_normal_at_point(self, p: Vector) -> float:
        pass

    def get_unit_normal_at_point(self, p: Vector) -> float:
        pass


class Sphere(SceneObject):
    def __init__(self, center: Vector, radius: float, color=Vector):
        self.center = center
        self.radius = radius
        self.color = color

    def __str__(self):
        return f"Sphere with center {self.center}, radius {self.radius}, color {self.color}"

    def intersect_ray(
        self, p: Vector, v: Vector, t_min: float, t_max: float
    ) -> float | None:
        """Given a ray with origin p and direction v, find the
        distance to the intersection, or return None if there isn't one.

        Returns the smaller t value that is in the given interval.

        Derivation:

        Let (x0, y0, z0) be the center of the sphere and r the radius.

        (p.x + t * v.x - x0) ** 2
        + (p.y + t * v.y - y0) ** 2
        + (p.z + t * v.z - z0) ** 2
        = r ** 2

        (vx ** 2 + vy ** 2 + vz ** 2) * t ** 2
        + 2 * ((px - x0) * vx + (py - y0) * vy + (pz - z0) * vz) * t
        + (px - x0) ** 2  + (py - y0) ** 2 + (pz - z0) ** 2 - r ** 2

        Use abc formula. Rewrite as vector operations.
        """

        a = v.squared_magnitude()
        b = 2 * dot(p - self.center, v)
        c = (p - self.center).squared_magnitude() - self.radius**2

        if a == 0:
            return -c / b

        D = b**2 - 4 * a * c

        if D < 0:
            return None

        sqrtD = math.sqrt(D)

        t1 = (-b + sqrtD) / (2 * a)
        t2 = (-b - sqrtD) / (2 * a)

        t1 = t1 if t_min <= t1 <= t_max else None
        t2 = t2 if t_min <= t2 <= t_max else None

        if t1 is None and t2 is None:
            return None
        if t1 is None:
            return t2
        if t2 is None:
            return t1
        return min(t1, t2)

    def get_unit_normal_at_point(self, p: Vector) -> float:
        """
        Calculate the normal at a point. If the point is not on
        the sphere, it will be projected on it.
        """
        return (p - self.center).unit()
