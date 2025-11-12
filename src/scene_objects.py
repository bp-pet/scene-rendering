import numpy as np


class SceneObject:
    def __init__(self, color=np.array):  # 3
        self.color = color

    def intersect_rays(
        self, P: np.ndarray, V: np.ndarray, t_min: float, t_max: float
    ) -> np.ndarray:
        return np.array(None)

    def get_unit_normal_at_point(self, p: np.ndarray) -> np.ndarray:  # 3; 3
        return np.array((0, 0, 0))


class Sphere(SceneObject):
    def __init__(self, center: np.ndarray, radius: float, color=np.array):  # 3; 3
        self.center = center
        self.radius = radius
        self.color = color

    def __str__(self):
        return f"Sphere with center {self.center}, radius {self.radius}, color {self.color}"

    def intersect_rays(
        self, P: np.ndarray, V: np.ndarray, t_min: float, t_max: float
    ) -> np.ndarray:
        """Given rays with origins P (3-by-n) and direction v (3-by-n), find the
        distance to the intersection, or return None if there isn't one.

        Returns the smaller t value that is in the given interval.

        Derivation for a single ray:
        Let (x0, y0, z0) be the center of the sphere and r the radius.

        (p.x + t * v.x - x0) ** 2
        + (p.y + t * v.y - y0) ** 2
        + (p.z + t * v.z - z0) ** 2
        = r ** 2

        (vx ** 2 + vy ** 2 + vz ** 2) * t ** 2
        + 2 * ((px - x0) * vx + (py - y0) * vy + (pz - z0) * vz) * t
        + (px - x0) ** 2  + (py - y0) ** 2 + (pz - z0) ** 2 - r ** 2

        Use abc formula. Rewrite as vector operations. Then rewrite as matrices.
        """

        assert P.shape == V.shape
        assert len(P.shape) == 2
        assert P.shape[0] == 3

        n = P.shape[1]

        # create arrays for sphere parameters
        S = self.center[:, np.newaxis]  # 3 by 1
        r = np.array(self.radius)  # 1

        assert S.shape == (3, 1)

        A = (V**2).sum(axis=0)  # n
        B = (2 * (P - S) * V).sum(axis=0)  # n
        C = ((P - S) ** 2).sum(axis=0) - r**2  # n
        assert A.shape == B.shape == C.shape == (n,)

        Dbig = B**2 - 4 * A * C  # n

        with np.errstate(invalid="ignore"):
            sqrtDbig = np.sqrt(Dbig)  # n

        T1 = (-B + sqrtDbig) / (2 * A)  # n
        T2 = (-B - sqrtDbig) / (2 * A)  # n
        T = np.stack([T1, T2], axis=0)  # 2 by n
        assert T.shape == (2, n)
        T_processed = np.where(np.abs(T) > 1e10, np.inf, T)  # 2 by n
        # entries will be nan if D < 0 and inf/really large if A = 0
        assert T_processed.shape == (2, n)

        # checks for each entry
        valid_mask = ~(np.isnan(T_processed) | np.isinf(T_processed))  # 2 by n
        valid_mask &= (T_processed >= t_min) & (T_processed <= t_max)  # 2 by n
        T_masked = np.where(valid_mask, T_processed, np.inf)  # 2 by n
        assert T_masked.shape == (2, n)

        result = np.min(T_masked, axis=0)  # n
        assert result.shape == (n,)

        # result has a t-value either in the asked interval or inf
        return result

    def get_unit_normal_at_point(self, p: np.ndarray) -> np.ndarray:  # 3; 3
        """
        Calculate the normal at a point. If the point is not on
        the sphere, it will be projected on it.
        """
        return (p - self.center).unit()
