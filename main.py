from src.camera import Camera
from src.light_source import LightSource
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

    scene_objects = [
        Sphere(center=Vector(0.9, -1.6, 1.9), radius=0.3, color=Vector(255, 0, 0)),
        Sphere(center=Vector(-2, 0, 0.5), radius=3, color=Vector(0, 255, 0)),
        Sphere(
            center=Vector(0, 0, 0), radius=0.5, color=Vector(0, 255, 100)
        ),  # inside red ball
        Sphere(center=Vector(0, 0, -10000), radius=9990, color=Vector(0, 0, 255)),
    ]

    light_sources = [
        LightSource(position=Vector(5, -2, 4)),
        LightSource(position=Vector(5, 1, 4)),
    ]

    scene = Scene(
        camera=camera, scene_objects=scene_objects, light_sources=light_sources
    )

    pmm = scene.capture(1000, 1000, verbose=True).get_pmm()

    with open("output/output.pmm", "w") as f:
        f.write(pmm)
