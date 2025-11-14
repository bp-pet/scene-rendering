from src.camera import Camera
from src.light_source import LightSource
from src.scene import Scene
from src.scene_objects import SceneObject, Sphere
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

    scene_objects: list[SceneObject] = [
        Sphere(
            center=Vector(0, 2, 0),
            radius=1,
            color=Vector(255, 100, 100),
            roughness=1,
        ),
        Sphere(
            center=Vector(0, 0, 0), radius=1, color=Vector(201, 201, 101), roughness=1
        ),
        Sphere(
            center=Vector(0, -2, 0), radius=1, color=Vector(100, 255, 100), roughness=1
        ),
        Sphere(
            center=Vector(0, 0, -1000),
            radius=999,
            color=Vector(102, 102, 202),
            roughness=1,
        ),
    ]

    light_sources = [
        LightSource(position=Vector(5, -2, 4)),
        LightSource(position=Vector(5, 1, 4)),
    ]

    scene = Scene(
        camera=camera, scene_objects=scene_objects, light_sources=light_sources
    )

    pmm = scene.capture(300, 300, verbose=True).get_pmm()

    with open("output/output.pmm", "w") as f:
        f.write(pmm)
