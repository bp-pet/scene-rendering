import math

from src.camera import Camera
from src.constants import background_color
from src.scene_objects import SceneObject
from src.light_source import LightSource
from src.simple_image import SimpleImage
from src.vector import Vector, reflect_around


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

    def send_ray(
        self, p: Vector, v: Vector, t_min: float, t_max: float
    ) -> tuple[float, int | None]:
        """
        Send a ray from point p in direction v and check for collision with any
        objects between t_min and t_max. Pick closest point of collision. Return the
        t of the collision and the index of the object.
        """
        # check collision with all objects
        distances = []
        for scene_object in self.scene_objects:
            distances.append(scene_object.intersect_ray(p, v, t_min, t_max))

        # find closest object
        min_distance = math.inf
        min_index = None
        for ind, distance in enumerate(distances):
            if distance is not None and distance < min_distance:
                min_distance = distance
                min_index = ind
        return min_distance, min_index

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
                if not self.scene_objects:
                    row.append(Vector(*background_color))
                    continue

                pixel_center = (
                    self.camera.top_left
                    - ((i + 0.5) * 2 * pixel_size_x * self.camera.up_unit)
                    + ((j + 0.5) * 2 * pixel_size_y * self.camera.right_unit)
                )
                starting_point = self.camera.eye_position
                ray_direction = pixel_center - self.camera.eye_position

                color = None

                for _ in range(10):  # TODO put in settings
                    t, object_index = self.send_ray(
                        self.camera.eye_position, ray_direction, 1, math.inf
                    )

                    if object_index is None:
                        color = Vector(*background_color)
                        break

                    collided_object = self.scene_objects[object_index]

                    # very simple setup to test reflection
                    if collided_object.roughness == 1:
                        color = collided_object.color
                        break
                    else:
                        starting_point = starting_point + t * ray_direction
                        unit_normal = collided_object.get_unit_normal_at_point(
                            starting_point
                        )
                        ray_direction = reflect_around(-ray_direction, unit_normal)

                if color is None:
                    color = Vector(*background_color)

                row.append(color)

            pixels.append(row)
        return SimpleImage(pixels)
