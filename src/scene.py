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

        x is the number of pixels top to bottom.
        y is the number of pixels left to right.
        b is the number of objects

        Camera ray given by p + t * v or P + t * V in matrix form.
        """
        assert resolution_x > 0
        assert resolution_y > 0

        if not self.scene_objects:
            # if no object just return empty background
            return SimpleImage(
                np.tile(background_color, (1, resolution_x, resolution_y))
            )

        pixel_size_x = self.camera.window_size_x / resolution_x
        pixel_size_y = self.camera.window_size_y / resolution_y

        # Get all pixel centers by starting from top left and applying offsets down and right:
        down_units_range = (np.arange(resolution_x) + 0.5) * 2 * pixel_size_x  # x
        right_units_range = (np.arange(resolution_y) + 0.5) * 2 * pixel_size_y  # y
        # how many units to move in each direction for each pixel
        pixel_centers = (
            self.camera.top_left[:, np.newaxis, np.newaxis]
            - down_units_range[np.newaxis, :, np.newaxis]
            * self.camera.up_unit[:, np.newaxis, np.newaxis]
            + right_units_range[np.newaxis, np.newaxis, :]
            * self.camera.right_unit[:, np.newaxis, np.newaxis]
        )  # 3 by x by y

        # Get input for intersection function:
        V = (
            pixel_centers.reshape(3, -1) - self.camera.eye_position[:, np.newaxis]
        )  # 3 by x*y
        assert V.shape == (3, resolution_x * resolution_y)
        P = np.tile(
            self.camera.eye_position[:, np.newaxis], (1, resolution_x * resolution_y)
        )  # 3 by x*y
        assert P.shape == (3, resolution_x * resolution_y)
        # intersection function takes unfolded array of rays

        # Calculate intersection with each object and save the colors in an array
        distances = np.zeros(
            shape=(len(self.scene_objects), resolution_x, resolution_y)
        )  # b by x by y
        object_colors = np.zeros((len(self.scene_objects) + 1, 3))  # b+1 by 3
        for obj_index, scene_object in enumerate(self.scene_objects):
            t_values_per_pixel_unfolded = scene_object.intersect_rays(
                P, V, 1, np.inf
            )  # x * y
            # results have to be folded into x by y again
            t_values_per_pixel = t_values_per_pixel_unfolded.reshape(
                resolution_x, resolution_y
            )  # x by y
            distances[obj_index, :, :] = t_values_per_pixel
            object_colors[obj_index, :] = scene_object.color

        object_colors[-1, :] = np.array(
            background_color
        )  # set the default as last element

        # Get the closest object (index) for each pixel
        collision_object_indices = np.argmin(distances, axis=0)  # x by y
        collision_distances = np.min(distances, axis=0)  # x by y
        mask = np.any(distances < np.inf, axis=0)  # pixels that have a collision at all
        collision_object_indices = np.where(
            mask, collision_object_indices, -1
        )  # x by y
        # 2d array with elements corresponding to indices of objects
        assert collision_object_indices.shape == (resolution_x, resolution_y)

        pixels = object_colors[collision_object_indices, :]

        t = collision_distances.reshape(1, -1)  # 1 by x*y
        collision_points_unfolded = P + t * V
        collision_points = collision_points_unfolded.reshape(
            3, resolution_x, resolution_y
        )  # 3 by x by y

        # TODO this part has to be rewritten with numpy
        # total_illumination = 0.0
        for light_source in self.light_sources:
            rays_to_light_source = (
                light_source.position - collision_points
            )  # 3 by x by y

            # check for shadow
            for scene_object in self.scene_objects:
                shadow_distance = scene_object.intersect_rays(
                    collision_points, rays_to_light_source, 0, 1
                )

        #     total_illumination += (
        #         max(0, dot(unit_normal, ray_to_light_source.unit()))
        #         if not in_shadow
        #         else 0
        #     )
        # illumination = total_illumination / len(self.light_sources)
        # not sure this is a good way to do illumination but it doesn't matter for one source

        return SimpleImage(pixels)
