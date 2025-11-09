from src.camera import Camera
from src.scene import Scene
from src.scene_objects import Sphere
from src.vector import Vector


if __name__ == "__main__":
    """Simple scene capture."""

    # camera distance 5 along the x-axis, pointed towards the origin
    camera = Camera(
        eye_position=Vector(5, 0, 0),
        window_size_x=1,
        window_size_y=1,
        viewing_direction=Vector(-1, 0, 0),
        orientation_vector=Vector(0, 0, 1),
        window_distance=1,
    )

    # red ball of radius 1 at origin
    sphere1 = Sphere(center=Vector(0, 0, 0), radius=1, color=(255, 0, 0))
    sphere2 = Sphere(center=Vector(-2, 0, 0.5), radius=3, color=(0, 0, 255))
    sphere3 = Sphere(center=Vector(0, 0, 0), radius=0.5, color=(0, 255, 0)) # inside red ball

    scene = Scene(camera=camera, scene_objects=[sphere1, sphere2, sphere3])

    pmm = scene.capture(1000, 1000).get_pmm()

    with open("output/output.pmm", "w") as f:
        f.write(pmm)