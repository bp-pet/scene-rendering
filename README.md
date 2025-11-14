# Scene rendering in Python
Simple implementation of scene rendering. Can set a camera position and some objects in `main.py`, then running it will render the scene.

Based on https://raytracing.github.io/books/RayTracingInOneWeekend.html. The goal of the project is learning so I went over some of my process below.

## Development log and design decisions
My idea with this project was to do as much of the math and logic myself as I can, based on my surface level understanding of computer graphics. In practice I went in parallel between the ebook and my own developing, using the book when I didn't have a good idea for something. I also sometimes found improvements I could use for my code while reading, for example using vector operations to get the sphere intersections.

I realized my C++ knowledge is way too low to work for this so went for Python for simplicity, as the focus is the logic more than the coding.

### Parallelization
There is a separate branch with a simple implementation in `numpy`, where all operations happen with array operations and no looping over pixels/rays. This is obviously orders of magnitude faster but is also annoying to implement so I stopped at the simple setup with no ray bouncing. It is anyway not quick enough for real-time rendering. Still, a possible improvement for this project would be to implement everything like this. See branch `parallelization`.

### Recursion
My first idea did not include recursion for the bounces so I went with that. I see that the ebook uses it and I agree it is cleaner but I don't think it is really necessary here so I leave it as it is.

### Ray bouncing
Went for linearly interpolating between a clean bounce and a random bounce based on object roughness. This should work for our purposes although the quality is likely worse than the proper logic (Lambertian random bounce for matte objects and fuzzy clean bounce for shiny objects).

### Color propagation
There is the problem of mixing the object's own color with the incoming color. My initial idea was to do this also with linear interpolation, but this gets quite messy. Doing 50-50 interpolation means giving disproportionate attention to the last observed color (which will almost always be the background color). So it has to be some weighed average but figuring out the weights seems like an annoying task. The ebook suggests multiplying the colors without any extra steps. I wouldn't intuitively guess that this would work but it does so let's go with it.

### Antialiasing/filters
My initial plan was to avoid antialiasing this entirely and just produce low quality images, as quality was not really my goal. However, it seems filters have a much more important role when dealing with randomness in bounces. So we will see if it will become necessary eventually.

### Not in this project
Some things mentioned in the ebook surely make the quality much better but I don't have much interest in them so I skip them unless they prove necessary. This would be:
- Field of view/blur/other camera properties.
- Previously mentioned ray bouncing improvements.
- Most numerical stability fixes.
- Glass-type materials.