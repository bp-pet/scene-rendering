import random


def get_random_point_on_unit_disk() -> tuple[float, float]:
    while True:
        x = 2 * random.random() - 1
        y = 2 * random.random() - 1
        if x**2 + y**2 > 1:
            continue
        return x, y


if __name__ == "__main__":
    print(get_random_point_on_unit_disk())
