from src.vector import Vector, dot, cross

class Camera:
    """
    Characterized by an 'eye' and a 'window', where the eye 'views' a scene
    through the window.

    The eye has a position and the window has a size.

    The relationship between the eye and the window is defined by multiple things.
    1. The distance between the eye and the center of the window
    2. The viewing direction which says in which direction the window is from the
    perspective of the eye. The window's plane is always orthogonal to this direction.
    3. The 'orientation' which is a vector that defines how the window is rotated. This
    vector essentially points from the center of the window directly towards its top
    border. This means it has to be orthogonal to the viewing direction.
    """

    def __init__(
        self,
        eye_position: Vector,
        window_size_x: float,
        window_size_y: float,
        viewing_direction: Vector,
        orientation_vector: Vector,
        window_distance: float,
    ):
        self.eye_position = eye_position
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        self.viewing_direction = viewing_direction
        self.orientation_vector = orientation_vector
        # TODO implement default orientation (just vertical)
        self.window_distance = window_distance

        assert dot(self.viewing_direction, self.orientation_vector) == 0, (
            "Orientation be orthogonal to the viewing direction"
        )

        self.window_center = self.eye_position + (
            self.viewing_direction.unit() * self.window_distance
        )

        # it's not really unit but the one from the center to the top/right border
        # maybe should be renamed
        self.up_unit = self.orientation_vector.unit() * self.window_size_x
        self.right_unit = -cross(self.orientation_vector, self.viewing_direction).unit() * self.window_size_y

        self.top_right = (
            self.window_center
            + (self.up_unit * self.window_size_x)
            + (self.right_unit * self.window_size_y)
        )
        self.top_left = (
            self.window_center
            + (self.up_unit * self.window_size_x)
            - (self.right_unit * self.window_size_y)
        )
        self.bottom_right = (
            self.window_center
            - (self.up_unit * self.window_size_x)
            + (self.right_unit * self.window_size_y)
        )
        self.bottom_left = (
            self.window_center
            - (self.up_unit * self.window_size_x)
            - (self.right_unit * self.window_size_y)
        )

if __name__ == "__main__":
    """Testing basic properties."""
    camera = Camera(
        eye_position=Vector(5, 0, 0),
        window_size_x=1,
        window_size_y=1,
        viewing_direction=Vector(-1, 0, 0),
        orientation_vector=Vector(0, 0, 1),
        window_distance=1,
    )
    
    print(camera.window_center)
    print(camera.up_unit)
    print(camera.right_unit)
    print(camera.top_left)
    print(camera.bottom_right)