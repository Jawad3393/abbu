import os
import sys
sys.path.append("/home/antonxue/foo/test/abbu/src")
import abbu


abbu.setup(
    api_key = os.getenv("OPENAI_API_KEY"),
    cache_file = "/home/antonxue/foo/test/scripts/jawad_cache.py"
)

spec = abbu.FunctionSpec(
    name = "number_adder_2",
    params = ["num1", "num2"],
    description = "takes as input two numbers and returns their sum"
)

def add_three_numbers(a, b, c):
    f = abbu.create_function(spec=spec)
    return f(a, b) + c

