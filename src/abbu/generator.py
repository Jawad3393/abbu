import os
import re
import sys
import random
import importlib.util
from pathlib import Path
from typing import Optional, Dict
from openai import OpenAI
from .consts import PROMPT_HEADER
from .spec import FunctionSpec

# The config that will be filled in when setup(...) is called
ABBU_CONFIG = {
    "client": None,
    "model_version": None,
    "cache_file": None
}

def setup(api_key: str, cache_file: str, reset_cache: bool = False, model_version: str = "gpt-3.5-turbo", config: Optional[dict] = None):
    global ABBU_CONFIG
    if config is not None:
        ABBU_CONFIG = config
    else:
        client = OpenAI(api_key=api_key)
        ABBU_CONFIG["client"] = client
        ABBU_CONFIG["model_version"] = model_version
        ABBU_CONFIG["cache_file"] = cache_file

    if reset_cache:
        with open(cache_file, "w") as file:
            file.write("")
        print(f"Cache file {cache_file} has been reset.")
    else:
        if not os.path.exists(cache_file):
            with open(cache_file, "w") as file:
                file.write("")
            print(f"Cache file {cache_file} has been created.")

    return ABBU_CONFIG

def generate_code(spec: FunctionSpec):
    prompt = PROMPT_HEADER + "\n" + spec.to_prompt()
    print(f"Generating code for spec: {spec}")

    try:
        response = ABBU_CONFIG["client"].chat.completions.create(
            model=ABBU_CONFIG["model_version"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        raw_text = response.choices[0].message.content.strip()
        code_text = extract_code(raw_text, spec)
        
        return code_text
    except Exception as e:
        print(f"Error generating code from OpenAI: {e}")
        return None
    
def extract_code(raw_text: str, spec: FunctionSpec):
    code_blocks = re.findall(r'```python(.*?)```', raw_text, re.DOTALL)
    
    extracted_code = []
    for block in code_blocks:
        lines = block.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_line = line.replace('```', '').rstrip()
            if cleaned_line and not cleaned_line.lstrip().startswith('#'):
                cleaned_lines.append(cleaned_line)
        extracted_code.extend(cleaned_lines)

    cleaned_code = '\n'.join(extracted_code)
    cleaned_code = re.sub(r'\n\s*\n', '\n', cleaned_code)
    
    return cleaned_code.strip()

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

def save_cache(cache: Dict[str, str]):
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

def create_function(spec: FunctionSpec, use_cached_if_exists: bool = True, save_to_cache: bool = True):
    print(f"Creating function for spec: {spec}")
    cache = load_cache()

    if use_cached_if_exists and spec.name in cache:
        print(f"Function {spec.name} found in cache.")
        module_name = Path(ABBU_CONFIG["cache_file"]).stem
        mod = load_code(module_name, ABBU_CONFIG["cache_file"])
        f = getattr(mod, spec.name)
        return f

    func_text = generate_code(spec)
    if func_text is None:
        print("Failed to generate function code.")
        return None

    if save_to_cache:
        cache[spec.name] = func_text
        save_cache(cache)

    module_name = Path(ABBU_CONFIG["cache_file"]).stem
    mod = load_code(module_name, ABBU_CONFIG["cache_file"])
    f = getattr(mod, spec.name)
    return f
