import numpy as np

from src.camera import Camera
from src.constants import background_color
from src.scene_objects import SceneObject
from src.light_source import LightSource
from src.simple_image import SimpleImage


class Scene:
    def __init__(
        self,
        camera: Camera,
        scene_objects: list[SceneObject],
        light_sources: list[LightSource],
    ):
        self.camera = camera
        self.scene_objects = scene_objects
        self.light_sources = light_sources

    def capture(
        self, resolution_x: int, resolution_y: int, verbose: bool = False
    ) -> SimpleImage:
        """
        Capture the scene with a given resolution.

        x is top to bottom, y is left to right.

        Camera ray given by p + t * v or P + t * V in matrix form.
        """
        assert resolution_x > 0
        assert resolution_y > 0

        if not self.scene_objects:
            return SimpleImage(
                np.tile(background_color, (1, resolution_x, resolution_y))
            )

        pixel_size_x = self.camera.window_size_x / resolution_x
        pixel_size_y = self.camera.window_size_y / resolution_y

        print("starting pixel centers calculation")

        down_units_range = (np.arange(resolution_x) + 0.5) * 2 * pixel_size_x
        right_units_range = (np.arange(resolution_y) + 0.5) * 2 * pixel_size_y
        pixel_centers = (
            self.camera.top_left[:, np.newaxis, np.newaxis]
            - down_units_range[np.newaxis, :, np.newaxis]
            * self.camera.up_unit[:, np.newaxis, np.newaxis]
            + right_units_range[np.newaxis, np.newaxis, :]
            * self.camera.right_unit[:, np.newaxis, np.newaxis]
        )  # 3 by x by y

        print("starting P and V calculation")

        V = (
            pixel_centers.reshape(3, -1) - self.camera.eye_position[:, np.newaxis]
        )  # 3 by x*y
        assert V.shape == (3, resolution_x * resolution_y)

        P = np.tile(
            self.camera.eye_position[:, np.newaxis], (1, resolution_x * resolution_y)
        )  # 3 by x*y
        # TODO probably it doesn't need to be tiled
        assert P.shape == (3, resolution_x * resolution_y)

        distances = np.zeros(
            shape=(len(self.scene_objects), resolution_x, resolution_y)
        )  # b by x by y

        print("starting intersections")

        for obj_index, scene_object in enumerate(self.scene_objects):
            intersections_unfolded = scene_object.intersect_rays(
                P, V, 1, np.inf
            )  # x * y
            intersections = intersections_unfolded.reshape(
                resolution_x, resolution_y
            )  # x by y
            distances[obj_index, :, :] = intersections

        collision_object_indices = np.argmin(distances, axis=0)  # x by y
        # taking the argmin will always find something so need to check if its
        # an actual collision
        collision_object_indices = np.where(
            intersections < np.inf, collision_object_indices, -1
        )
        assert collision_object_indices.shape == (resolution_x, resolution_y)

        print("starting color writing")

        # TODO rewrite without loops
        pixels = np.zeros((resolution_x, resolution_y, 3))
        for i in range(resolution_x):
            for j in range(resolution_y):
                obj_idx = collision_object_indices[i, j]
                pixels[i, j, :] = (
                    self.scene_objects[obj_idx].color
                    if obj_idx >= 0
                    else np.array(background_color)
                )

        # total_illumination = 0.0
        # for light_source in self.light_sources:
        #     ray_to_light_source = light_source.position - collision_point

        #     # check for shadow
        #     # in_shadow = False
        #     # for scene_object in self.scene_objects:
        #     #     if scene_object == collided_object:
        #     #         continue
        #     #     shadow_distance = scene_object.intersect_ray(
        #     #         collision_point, ray_to_light_source, 0, 1
        #     #     )
        #     #     if shadow_distance is not None:
        #     #         in_shadow = True
        #     #         break

        #     total_illumination += (
        #         max(0, dot(unit_normal, ray_to_light_source.unit()))
        #         if not in_shadow
        #         else 0
        #     )
        # illumination = total_illumination / len(self.light_sources)
        # not sure this is a good way to do illumination but it doesn't matter for one source

        return SimpleImage(pixels)
