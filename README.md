# abbu

abbu is a python library for easy code generation with ChatGPT.

## Installation
`pip install abbu`

## Usage example

To use `abbu`, there's three simple key components:
* `setup`: This function initializes abbu by setting up the necessary configuration. Provide your OpenAI API key, a file path for caching, and optional settings. This step prepares everything abbu needs to generate and manage code.
* `FunctionSpec`: This class defines what you want your function to do. You specify the function name, input parameters, and the desired functionality.
* `create_function`: This function generates the code based on your FunctionSpec. It checks if the function is already in the cache; if not, it generates the code using the OpenAI API and saves it to the cache. The function is then returned, ready for use.

An example of how these come together is in the 

```python
# my_example.py
import os
import sys
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
```

As an example of how this would get run:
```
$ python3 /path/to/my_example.py
Creating function for spec: <abbu.spec.FunctionSpec object at 0x108a8b8f0>
Loaded cache: {}
Generating code for spec: <abbu.spec.FunctionSpec object at 0x108a8b8f0>
Cache saved to /Users/jawada/Documents/CC/jawad_cache.py.
6
```

abbu will create a cache file at `/path/to/your/cache.py` so that you can see what was generated.
