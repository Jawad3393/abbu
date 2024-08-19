
PROMPT_HEADER = """
You are a Python developers.
Generated Python code based on the following specification.
Make sure that the code is ready to run immediately without formatting issues and without syntax errors.
------
User:
name="calculate_area",
params=["shape", "dimensions"],
description=
Generate functions only, do not include your own examples.
Calculates the area of different shapes based on the provided dimensions.
The shape can be 'circle', 'square', or 'rectangle'.

DO NOT INCLUDE EXAMPLES!!!!

- 'circle' requires a single value: radius.
- 'square' requires a single value: side length.
- 'rectangle' requires two values: length and width.

The function should return the area of the shape.


ChatGPT:
import math

def calculate_area(shape, dimensions):
    def area_circle(radius):
        return math.pi * (radius ** 2)
    
    def area_square(side):
        return side ** 2
    
    def area_rectangle(length, width):
        return length * width
    
    if shape == 'circle':
        return area_circle(dimensions[0])
    elif shape == 'square':
        return area_square(dimensions[0])
    elif shape == 'rectangle':
        return area_rectangle(dimensions[0], dimensions[1])
    else:
        return "Invalid shape provided. Please choose 'circle', 'square', or 'rectangle'."

-----
User:
name="convert_temperature",
params=["temperature", "unit"],
description=
Generate functions only, do not include your own examples.
Converts a temperature from one unit to another.
The unit can be 'Celsius', 'Fahrenheit', or 'Kelvin'.

DO NOT INCLUDE EXAMPLES!!!!

- Converts temperature from Celsius to Fahrenheit and Kelvin.
- Converts temperature from Fahrenheit to Celsius and Kelvin.
- Converts temperature from Kelvin to Celsius and Fahrenheit.

The function should handle temperature conversions accurately.

ChatGPT:
def convert_temperature(temperature, unit):
    def celsius_to_fahrenheit(celsius):
        return (celsius * 9/5) + 32
    
    def celsius_to_kelvin(celsius):
        return celsius + 273.15
    
    def fahrenheit_to_celsius(fahrenheit):
        return (fahrenheit - 32) * 5/9
    
    def fahrenheit_to_kelvin(fahrenheit):
        return (fahrenheit - 32) * 5/9 + 273.15
    
    def kelvin_to_celsius(kelvin):
        return kelvin - 273.15
    
    def kelvin_to_fahrenheit(kelvin):
        return (kelvin - 273.15) * 9/5 + 32
    
    if unit == 'Celsius':
        return celsius_to_fahrenheit(temperature), celsius_to_kelvin(temperature)
    elif unit == 'Fahrenheit':
        return fahrenheit_to_celsius(temperature), fahrenheit_to_kelvin(temperature)
    elif unit == 'Kelvin':
        return kelvin_to_celsius(temperature), kelvin_to_fahrenheit(temperature)
    else:
        return "Invalid unit provided. Please choose 'Celsius', 'Fahrenheit', or 'Kelvin'."

------
User:
name="calculate_bmi",
params=["weight", "height"],
description=
Generate functions only, do not include your own examples.
Calculates the Body Mass Index (BMI) based on weight and height.
The weight should be in kilograms and the height should be in meters.

DO NOT INCLUDE EXAMPLES!!!!

- BMI is calculated as weight divided by height squared (kg/m^2).

The function should return the BMI value.

ChatGPT:
def calculate_bmi(weight, height):
    def bmi_formula(weight, height):
        return weight / (height ** 2)
    
    return bmi_formula(weight, height)
------

Specification:
"""

