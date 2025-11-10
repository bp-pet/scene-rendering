import math

from src.camera import Camera
from src.constants import background_color
from src.scene_objects import SceneObject
from src.light_source import LightSource
from src.simple_image import SimpleImage
from src.vector import Vector, dot


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
        """
        assert resolution_x > 0
        assert resolution_y > 0
        pixels = []
        pixel_size_x = self.camera.window_size_x / resolution_x
        pixel_size_y = self.camera.window_size_y / resolution_y
        for i in range(resolution_x):
            if verbose and (i + 1) % 10 == 0:
                print(f"Rendering row {i + 1} of {resolution_x}")
            row = []
            for j in range(resolution_y):
                pixel_center = (
                    self.camera.top_left
                    - ((i + 0.5) * 2 * pixel_size_x * self.camera.up_unit)
                    + ((j + 0.5) * 2 * pixel_size_y * self.camera.right_unit)
                )
                ray_direction = pixel_center - self.camera.eye_position

                if not self.scene_objects:
                    row.append(Vector(*background_color))
                    continue

                distances = []
                for scene_object in self.scene_objects:
                    distances.append(
                        scene_object.intersect_ray(
                            self.camera.eye_position, ray_direction, 1, math.inf
                        )
                    )

                min_distance = math.inf
                min_index = None
                for ind, distance in enumerate(distances):
                    if distance is not None and distance < min_distance:
                        min_distance = distance
                        min_index = ind

                if min_index is None:
                    row.append(Vector(*background_color))
                    continue

                collided_object = self.scene_objects[min_index]
                collision_point = (
                    self.camera.eye_position + min_distance * ray_direction
                )
                unit_normal = collided_object.get_unit_normal_at_point(collision_point)

                total_illumination = 0.0
                for light_source in self.light_sources:
                    ray_to_light_source = light_source.position - collision_point

                    # check for shadow
                    in_shadow = False
                    for scene_object in self.scene_objects:
                        if scene_object == collided_object:
                            continue
                        shadow_distance = scene_object.intersect_ray(
                            collision_point, ray_to_light_source, 0, 1
                        )
                        if shadow_distance is not None:
                            in_shadow = True
                            break

                    total_illumination += (
                        max(0, dot(unit_normal, ray_to_light_source.unit()))
                        if not in_shadow
                        else 0
                    )
                illumination = total_illumination / len(self.light_sources)
                # not sure this is a good way to do illumination but it doesn't matter for one source

                row.append(collided_object.color * illumination)
            pixels.append(row)
        return SimpleImage(pixels)
