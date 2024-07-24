import os
import sys
sys.path.append("/Users/jawada/Documents/abbu/src")
import abbu 


abbu.setup(
    api_key = os.getenv("OPENAI_API_KEY"),
    cache_file = "/Users/jawada/Documents/CC/jawad_cache.py",
    reset_cache=True 
)

spec = abbu.FunctionSpec(
    name = "number_adder_2",
    params = ["num1", "num2"],
    description = "takes as input two numbers and returns their sum"
)

def add_three_numbers(a, b, c):
    f = abbu.create_function(spec=spec)
    return f(a, b) + c

add_three_numbers(1,2,3)
