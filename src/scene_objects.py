import math
import numpy as np

from src.vector import Vector, dot


class SceneObject:
    def __init__(self, color=Vector):
        self.color = color

    def intersect_ray(
        self, p: Vector, v: Vector, t_min: float, t_max: float
    ) -> float | None:
        pass

    def get_unit_normal_at_point(self, p: Vector) -> Vector:
        return Vector(0, 0, 0)


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

        t1_checked = t1 if t_min <= t1 <= t_max else None
        t2_checked = t2 if t_min <= t2 <= t_max else None

        if t1_checked is None and t2_checked is None:
            return None
        if t1_checked is None:
            return t2_checked
        if t2_checked is None:
            return t1_checked
        return min(t1_checked, t2_checked)

    def intersect_rays(
        self, P: np.ndarray, V: np.ndarray, t_min: float, t_max: float
    ) -> np.ndarray:
        """Multiple rays for parallelism."""

        # create arrays for sphere parameters
        S = np.array([self.center.x, self.center.y, self.center.z])[:, np.newaxis]
        R = np.array([self.radius])[:, np.newaxis]

        A = (V**2).sum(axis=0)
        B = ((P - S) * V).sum(axis=0)
        C = (P - S) ** 2 - R**2

        Dbig = B**2 - 4 * A * C

        sqrtDbig = np.sqrt(Dbig)

        T1 = (-B + sqrtDbig) / (2 * A)
        T2 = (-B - sqrtDbig) / (2 * A)
        T = np.stack([T1, T2], axis=0)
        T_processed = np.where(np.abs(T) > 1e10, np.inf, T)
        # entries will be nan if D < 0 and inf/really large if A = 0

        # checks for each entry
        valid_mask = ~(np.isnan(T_processed) | np.isinf(T_processed))
        valid_mask &= (T_processed >= t_min) & (T_processed <= t_max)
        T_masked = np.where(valid_mask, T_processed, np.inf)

        # get smallest nad drop it if it is inf
        result = np.min(T_masked, axis=1)
        result = np.where(np.isinf(result), np.nan, result)

        # result has a t-value or nan
        return result

    def get_unit_normal_at_point(self, p: Vector) -> Vector:
        """
        Calculate the normal at a point. If the point is not on
        the sphere, it will be projected on it.
        """
        return (p - self.center).unit()
