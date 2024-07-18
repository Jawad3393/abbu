import re
import os
from typing import Optional
from openai import OpenAI
from datetime import datetime, timezone, timedelta
import importlib.util
from pathlib import Path

from .consts import PROMPT_HEADER
from .spec import FunctionSpec


# The config that will be filled in when setup(...) is called
ABBU_CONFIG = {
    "client": None,
    "model_version": None,
    "cache_file": None
}


def setup(
    api_key: str,
    cache_file: str,
    reset_cache: bool = False
    model_version = "gpt-3.5-turbo",
    config: Optional[dict] = None,
):
    """ Set up the config with which to run abbu """
    global ABBU_CONFIG
    if config is not None:
        ABBU_CONFIG = config
    else:
        ABBU_CONFIG["client"] = OpenAI(api_key="_api_key")
        ABBU_CONFIG["model_version"] = model_version
        ABBU_CONFIG["cache_file"] = cache_file

    if reset_cache:
        # TODO: Delete the contents of the cache_file if it exists
        pass

    return ABBU_CONFIG


def generate_code(spec: FunctionSpec):
    global ABBU_CONFIG
    prompt = PROMPT_HEADER + "\n" + spec.to_prompt()

    response = ABBU_CONFIG["client"].chat.completions.create(
        model = ABBU_CONFIG["model_version"],
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "User", "content": prompt}
        ]
    )

    raw_text = response.choices[0].message.content.strip()
    code_text = extract_code(raw_text, spec)
    return code_text


def extract_code(gpt_output: str, spec: FunctionSpec):
    # TODO: need to make sure that gpt_output either matches spec.name ... or replace it
    # Find the part of the response that contains the Python code
    code_start = code.find('def ')
    if code_start != -1:
        code = code[code_start:]
    else:
        # If the code does not start with a function definition, find another way to locate the start
        code = code.split('```python')[1].split('```')[0].strip()

    lines = code.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.replace('```', '')
        # Remove specific instructional comments
        if not (line.strip().startswith('Certainly!')):
            cleaned_lines.append(line)
    cleaned_code = '\n'.join(cleaned_lines)
    cleaned_code = re.sub(r'\n\s*\n', '\n', cleaned_code)
    return cleaned_code.strip()



def load_cache_as_dict(cache_file: str):
    # TODO: Returns a func_name -> code_text dictionary
    pass

def save_cache(cache: dict[str,str], cache_file):
    # Writes all the contents to the cache
    pass


def save_code(content, file):
    with open(file, 'w') as file:
        file.write(content)

def load_code(module_name, file):
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def ensure_cache_dir(cache_dir_path):
    Path(cache_dir_path).mkdir(exist_ok=True)

def load_cache(file):
    if not os.path.exists(file):
        return {}
    with open(file, 'r') as file:
        contents = file.read()
    return contents

def save_cache(contents, file):
    with open(file, 'w') as file:
        file.write(contents)

def update_cache(func, cache_contents):

    print(f"func is")
    print(func)

    cache_contents[func.__name__] = func
    return cache_contents

def create_function(spec, cache_dir):
    client = get_openai_client()
    func_text = generate_code(client, spec)
    # func_text = call_openai(spec)
    cache_file = os.path.join(cache_dir, 'cache.py')
    print(f"The cache is at {cache_file}")

    cache_contents = load_cache(cache_file)
    cache_contents = update_cache(func_text, cache_contents)
    save_cache(cache_contents, cache_file)

    
    module_name = 'generated_func_module'
    mod = load_code(module_name, cache_file)
    f = getattr(mod, func_text.__name__)
    return f
