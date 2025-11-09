import math

from src.camera import Camera
from src.scene_objects import SceneObject
from src.simple_image import SimpleImage

class Scene:
    def __init__(self, camera: Camera, scene_objects: list[SceneObject]):
        self.camera = camera
        self.scene_objects = scene_objects

    def capture(self, resolution_x: int, resolution_y: int) -> SimpleImage:
        assert resolution_x > 0
        assert resolution_y > 0
        pixels = []
        pixel_size_x = self.camera.window_size_x / resolution_x
        pixel_size_y = self.camera.window_size_y / resolution_y
        for i in range(resolution_x):
            row = []
            for j in range(resolution_y):
                pixel_center = (
                    self.camera.top_left
                    - ((i + 0.5) * 2 * pixel_size_x * self.camera.up_unit)
                    + ((j + 0.5) * 2 * pixel_size_y * self.camera.right_unit)
                )
                ray_direction = pixel_center - self.camera.eye_position

                if not self.scene_objects:
                    row.append((0, 0, 0))
                    continue
                
                distances = []
                for scene_object in self.scene_objects:
                    distances.append(scene_object.intersect_ray(self.camera.eye_position, ray_direction))

                min_val = math.inf
                min_index = None
                for ind, distance in enumerate(distances):
                    if distance is not None and distance < min_val:
                        min_val = distance
                        min_index = ind
                
                if min_index is None:
                    row.append((0, 0, 0))
                    continue
                    
                collided_object = self.scene_objects[min_index]
                row.append(collided_object.color)
            pixels.append(row)
        return SimpleImage(pixels)

