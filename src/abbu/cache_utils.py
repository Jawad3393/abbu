import os
import re
from typing import Optional

def extract_functions(file_path):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define the regular expression pattern
    pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)(\s*\(.*?\)\s*):(.*?)(?=\ndef\s|\nclass\s|\Z)'
    
    # Find all matches in the content
    functions = {}
    matches = re.findall(pattern, content, re.DOTALL)
    for (name, params, body) in matches:
        whole_func_str = f"def {name}{params}:{body}"
        functions[name] = whole_func_str

    return functions



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
            cache[name] = obj

    print(f"Loaded cache: {cache}")
    return cache

def save_cache(cache: dict[str, str]):
    cache_file = ABBU_CONFIG["cache_file"]
    with open(cache_file, 'a') as file:  
        for func_name, func_code in cache.items():
            if isinstance(func_code, str):
                file.write(func_code + "\n\n")
    print(f"Cache saved to {cache_file}.")

def load_code(module_name: str, file: str):
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


