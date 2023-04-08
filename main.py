import numpy as np
import matplotlib.pyplot as plt

# Define constants
WIDTH = 500
HEIGHT = 500
FOV = np.pi / 3
BACKGROUND_COLOR = np.array([0, 0, 0])

# Define camera position and viewing direction
camera_pos = np.array([0, 0, -5])
pixel_size = 2 * np.tan(FOV/2) / WIDTH
image = np.zeros((HEIGHT, WIDTH, 3))

# Define properties of spheres in the scene
spheres = [
    (np.array([0, 0, 0]), 1, np.array([1, 0, 0])),
    (np.array([1, 1, 1]), 0.5, np.array([0, 1, 0]))
]

# Define function to compute color of a sphere based on its properties
def compute_color(color, normal):
    light_dir = np.array([1, 1, -1])
    light_dir = light_dir / np.linalg.norm(light_dir)
    ambient = 0.2
    diffuse = 1.0 - ambient
    intensity = ambient + diffuse * np.dot(light_dir, normal)
    return intensity * color

# Define function to trace a ray and compute its color
def trace_ray(origin, direction):
    global spheres
    min_distance = float('inf')
    hit_sphere = None
    for sphere in spheres:
        center, radius, color = sphere
        oc = origin - center
        a = np.dot(direction, direction)
        b = 2 * np.dot(oc, direction)
        c = np.dot(oc, oc) - radius**2
        discriminant = b**2 - 4*a*c
        if discriminant >= 0:
            t1 = (-b - np.sqrt(discriminant)) / (2*a)
            t2 = (-b + np.sqrt(discriminant)) / (2*a)
            if t1 > 0 and t1 < min_distance:
                min_distance = t1
                hit_sphere = sphere
            if t2 > 0 and t2 < min_distance:
                min_distance = t2
                hit_sphere = sphere
    if hit_sphere is not None:
        center, radius, color = hit_sphere
        intersection_point = origin + min_distance * direction
        normal = (intersection_point - center) / radius
        color = compute_color(color, normal)
        return color
    else:
        return BACKGROUND_COLOR

# Define function to render the image
def render_image():
    global camera_pos, image
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # Compute viewing ray direction
            direction = np.array([
                (x - WIDTH/2) * pixel_size,
                -(y - HEIGHT/2) * pixel_size,
                1
            ])
            direction = direction / np.linalg.norm(direction)
            # Trace the ray and compute its color
            color = trace_ray(camera_pos, direction)
            # Set the pixel color in the image
            image[y, x] = color
    # Display the image
    plt.imshow(image)
    plt.show()

# Call the render_image function to generate the image
render_image()
