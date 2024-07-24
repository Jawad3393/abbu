import os
import sys
import random
import turtle

sys.path.append("/Users/jawada/Documents/abbu/src")
import abbu

abbu.setup(
    api_key= os.getenv("OPENAI_API_KEY"),
    cache_file="/Users/jawada/Documents/CC/jawad_cache.py",
    reset_cache=True
)

spec_shape = abbu.FunctionSpec(
    name="draw_shape",
    params=["size", "color", "scale", "x", "y"],
    description="""
    Draws a shape using the Turtle graphics library. The function should take the following parameters:
    - size: The size of the shape.
    - color: The color of the turtle.
    - scale: The scaling factor for the shape.
    - x: The x-coordinate for the position of the shape.
    - y: The y-coordinate for the position of the shape.

    The function should:
    1. Change the color of the turtle.
    2. Draw the shape scaled up by the factor of 'scale'.
    3. Change the location of the shape on the screen based on the provided x and y coordinates.
    """
)

def draw_shape(size, color, scale, x, y):
    f = abbu.create_function(spec=spec_shape)
    return f(size, color, scale, x, y)

draw_shape(60, "blue", 2, 100, -100)
