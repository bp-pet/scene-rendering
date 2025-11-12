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

        down_units_range = (np.arange(resolution_x) + 0.5) * 2 * pixel_size_x
        right_units_range = (np.arange(resolution_y) + 0.5) * 2 * pixel_size_y
        pixel_centers = (
            self.camera.top_left[:, np.newaxis, np.newaxis]
            - down_units_range[np.newaxis, :, np.newaxis]
            * self.camera.up_unit[:, np.newaxis, np.newaxis]
            + right_units_range[np.newaxis, np.newaxis, :]
            * self.camera.right_unit[:, np.newaxis, np.newaxis]
        )  # 3 by x by y

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

        # Calculate intersection with each object
        object_colors = np.zeros((len(self.scene_objects) + 1, 3))  # b+1 by 3
        for obj_index, scene_object in enumerate(self.scene_objects):
            t_values_per_pixel_unfolded = scene_object.intersect_rays(
                P, V, 1, np.inf
            )  # x * y
            t_values_per_pixel = t_values_per_pixel_unfolded.reshape(
                resolution_x, resolution_y
            )  # x by y
            distances[obj_index, :, :] = t_values_per_pixel  # b by x by y

            object_colors[obj_index, :] = scene_object.color

        object_colors[-1, :] = np.array(
            background_color
        )  # set the default as last element

        # Get the closest object for each pixel
        collision_object_indices = np.argmin(distances, axis=0)  # x by y
        mask = np.any(distances < np.inf, axis=0)
        collision_object_indices = np.where(
            mask, collision_object_indices, -1
        )  # x by y
        # 2d array with elements corresponding to indices of objects
        assert collision_object_indices.shape == (resolution_x, resolution_y)

        # TODO rewrite without loops
        pixels = object_colors[collision_object_indices, :]

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
