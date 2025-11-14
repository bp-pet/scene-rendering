import math

from src.camera import Camera
from src.constants import background_color, color_reflection_rate, max_number_of_bounces
from src.scene_objects import SceneObject
from src.light_source import LightSource
from src.simple_image import SimpleImage
from src.vector import (
    Vector,
    reflect_around,
    dot,
    random_vector_in_hemisphere,
    linear_interpolation,
)


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

    def get_illumination(self, point_of_interest: Vector, unit_normal: Vector) -> float:
        total_illumination = 0.0
        for light_source in self.light_sources:
            ray_to_light_source = light_source.position - point_of_interest

            # check for shadow
            in_shadow = False
            for scene_object in self.scene_objects:
                shadow_distance = scene_object.intersect_ray(
                    point_of_interest, ray_to_light_source, 0.001, 1
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
        return illumination

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

                observed_colors: list[Vector] = []

                for _ in range(max_number_of_bounces):  # TODO put in settings
                    # find next collision
                    t, object_index = self.send_ray(
                        self.camera.eye_position, ray_direction, 1, math.inf
                    )

                    # add color to list
                    if object_index is None:
                        # no collision, end tracing
                        observed_colors.append(Vector(*background_color))
                        break
                    collided_object = self.scene_objects[object_index]
                    observed_colors.append(collided_object.color)

                    # calculate next starting point
                    collision_point = starting_point + t * ray_direction
                    unit_normal = collided_object.get_unit_normal_at_point(
                        collision_point
                    )
                    starting_point = collision_point

                    # calculate next direction
                    clean_bounce = reflect_around(-ray_direction, unit_normal)
                    random_bounce = random_vector_in_hemisphere(unit_normal)
                    ray_direction = linear_interpolation(
                        clean_bounce, random_bounce, collided_object.roughness
                    )

                # calculate color
                # example for 4 observed colors: 1/2 * colors[0] + 1/4 * colors[1] + 1/8 * colors[2] + 1/8 * colors[3]
                pixel_color = Vector(0, 0, 0)
                for c in range(len(observed_colors)):
                    pixel_color += observed_colors[c] * (0.5 ** (c + 1))
                pixel_color += observed_colors[-1] * (0.5 ** (len(observed_colors)))

                row.append(pixel_color)

            pixels.append(row)
        return SimpleImage(pixels)
