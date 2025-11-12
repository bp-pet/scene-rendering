import numpy as np


class SimpleImage:
    def __init__(self, pixels: np.ndarray):  # x by y by 3
        """
        Create an image of an array of x (vertical) by y (horizontal)
        by 3 (rgb).
        """
        self.pixels = pixels

    def get_pmm(self) -> str:
        print("Starting image writing")
        result = f"P3\n{self.pixels.shape[0]} {self.pixels.shape[1]}\n255\n"
        for i in range(self.pixels.shape[0]):
            for j in range(self.pixels.shape[1]):
                color = self.pixels[i, j]
                result += f"{int(color[0])} {int(color[1])} {int(color[2])}\n"
        return result


if __name__ == "__main__":
    # test image generation
    pixels = []
    for i in range(256):
        row = []
        for j in range(256):
            row.append((i, j, 0))
        pixels.append(row)

    img = SimpleImage(np.array(pixels))

    with open("output/test_output.pmm", "w") as f:
        f.write(img.get_pmm())
