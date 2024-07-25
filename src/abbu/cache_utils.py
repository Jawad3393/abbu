import os
import re
from typing import Optional
import importlib
from pathlib import Path

def extract_functions(file_path):
    # Read the contents of the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Define the regular expression pattern
    pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)(\s*\(.*?\)\s*):(.*?)(?=\ndef\s|\nclass\s|\Z)'
    
    print("THE CONTENT IS::::::::::::::::::::::::")
    print(content)

    # Find all matches in the content
    functions = {}
    matches = re.findall(pattern, content, re.DOTALL)
    for (name, params, body) in matches:
        whole_func_str = f"def {name}{params}:{body}"
        functions[name] = whole_func_str

    return functions


def load_cache(
    cache_file: str
):
    if not os.path.exists(cache_file):
        print(f"Cache file {cache_file} does not exist.")
        return {}

    # This code loads the python definitions, etc into the interpreter
    module_name = Path(cache_file).stem
    spec = importlib.util.spec_from_file_location(module_name, cache_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # But we now have to parse out the actual cache contents as strings
    cache = extract_functions(cache_file)
    return cache



"""
def load_cache():
    cache_file = ABBU_CONFIG["cache_file"]
    if not os.path.exists(cache_file):
        print(f"Cache file {cache_file} does not exist.")
        return {}
    
    cache = {}
    cache_namespace = {}
    with open(cache_file, 'r') as file:
        code = file.read()
        if code.strip():  # Check if the file is not empty
            exec(code, {}, cache_namespace)
    
    # Extract only the functions defined in the cache file
    for name, obj in cache_namespace.items():
        if callable(obj):
            # This seems wrong.
            # We want the cache to map function_names -> function_str because we want to make it easy
            # To update the cache by writing in the function_str
            # At present, this stores a function_obj instead, which is cannot be easily converted to a string
            # ALl keys of your cache should have the same type; All values should also have the same type
            cache[name] = obj

    print(f"Loaded cache: {cache}")
    return cache
"""

def save_cache(cache: dict[str, str], cache_file):
    with open(cache_file, 'w') as file:  
        # Important! The maps string to strings
        for func_name, func_str in cache.items():
            file.write(func_str + "\n\n")
    print(f"Cache saved to {cache_file}.")

def load_code(module_name: str, file: str):
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


