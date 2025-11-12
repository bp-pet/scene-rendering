import numpy as np

from src.camera import Camera
from src.light_source import LightSource
from src.scene import Scene
from src.scene_objects import Sphere, SceneObject


if __name__ == "__main__":
    """Simple scene capture."""

    # camera distance 5 along the x-axis, pointed towards the origin
    camera = Camera(
        eye_position=np.array((5, 0, 0)),
        window_size_x=1,
        window_size_y=1,
        viewing_direction=np.array((-1, 0, 0)),
        orientation_vector=np.array((0, 0, 1)),
        window_distance=1,
    )

    scene_objects: list[SceneObject] = [
        Sphere(
            center=np.array((0.9, -1.6, 1.9)),
            radius=0.3,
            color=np.array((255, 0, 0)),
        ),
        Sphere(center=np.array((-2, 0, 0.5)), radius=3, color=np.array((0, 255, 0))),
        Sphere(
            center=np.array((0, 0, 0)), radius=0.5, color=np.array((0, 255, 100))
        ),  # inside red ball
        Sphere(
            center=np.array((0, 0, -10000)), radius=9990, color=np.array((0, 0, 255))
        ),
    ]

    light_sources = [
        LightSource(position=np.array((5, -2, 4))),
        LightSource(position=np.array((5, 1, 4))),
    ]

    scene = Scene(
        camera=camera, scene_objects=scene_objects, light_sources=light_sources
    )

    pmm = scene.capture(1000, 1000, verbose=True).get_pmm()

    with open("output/output.pmm", "w") as f:
        f.write(pmm)
