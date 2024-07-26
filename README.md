# abbu

abbu is a python library for easy code generation with ChatGPT.

## Installation
`pip install abbu`

## Usage example

To use `abbu`, there's three simple key components:
* `setup`: TODO (explain what this thing does)
* `FunctionSpec`: TODO (more explanations)
* `create_function`: TODO (more explanations). 

An example of how these come together is in the 

```python
# my_example.py
import os
import sys
import abbu 

abbu.setup(
    api_key = os.getenv("OPENAI_API_KEY"),
    cache_file = "/Users/jawada/Documents/CC/jawad_cache.py",
    reset_cache=True # Nuke the entire cache file
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
YOU CAN JUST COPY-PASTE TERMINAL OUTPUT HERE
BLAH BLAH BALh
MORE LINES
```

abbu will create a cache file at `/path/to/your/cache.py` so that you can see what was generated.
