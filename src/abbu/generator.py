import re
import os
import json
from typing import Optional, Dict
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
    reset_cache: bool = False,
    model_version: str = "gpt-3.5-turbo",
    config: Optional[dict] = None,
):
    """ Set up the config with which to run abbu """
    global ABBU_CONFIG
    if config is not None:
        ABBU_CONFIG = config
    else:
        ABBU_CONFIG["client"] = OpenAI(api_key=api_key)
        ABBU_CONFIG["model_version"] = model_version
        ABBU_CONFIG["cache_file"] = cache_file

    ensure_cache_dir(os.path.dirname(cache_file))

    if reset_cache and os.path.exists(cache_file):
        with open(cache_file, 'w') as file:
            pass
    
    return ABBU_CONFIG


def ensure_cache_dir(cache_dir_path: str):
    Path(cache_dir_path).mkdir(parents=True, exist_ok=True)


def generate_code(spec: FunctionSpec):
    global ABBU_CONFIG
    prompt = PROMPT_HEADER + "\n" + spec.to_prompt()

    response = ABBU_CONFIG["client"].chat.completions.create(
        model=ABBU_CONFIG["model_version"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response.choices[0].message['content'].strip()
    code_text = extract_code(raw_text, spec)
    return code_text


def extract_code(raw_text: str, spec: FunctionSpec):
    # TODO: need to make sure that gpt_output either matches spec.name ... or replace it
    # Find the part of the response that contains the Python code
    code_start = raw_text.find('def ')
    if code_start != -1:
        code = raw_text[code_start:]
    else:
        # If the code does not start with a function definition, find another way to locate the start
        code = raw_text.split('```python')[1].split('```')[0].strip()

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


def load_cache():
    cache_file = ABBU_CONFIG["cache_file"]
    if not os.path.exists(cache_file):
        return {}
    with open(cache_file, 'r') as file:
        contents = file.read()
    
    return json.loads(contents)


def update_cache(code_text: str, spec: FunctionSpec, cache: Dict[str, str]):
    cache[spec.name] = code_text


def save_cache(cache: Dict[str, str]):
    cache_file = ABBU_CONFIG["cache_file"]
    with open(cache_file, 'w') as file:
        file.write(json.dumps(cache))


def load_code(module_name: str, file: str):
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_function(
    spec: FunctionSpec,
    use_cached_if_exists: bool = True,  # Prevents re-generation if it already exists in the cache
    save_to_cache: bool = False,
):
    cache = load_cache()

    if use_cached_if_exists and spec.name in cache:
        module_name = Path(ABBU_CONFIG["cache_file"]).stem
        mod = load_code(module_name, ABBU_CONFIG["cache_file"])
        f = getattr(mod, spec.name)
        return f

    func_text = generate_code(spec)

    if save_to_cache:
        update_cache(func_text, spec, cache)
        save_cache(cache)

    module_name = Path(ABBU_CONFIG["cache_file"]).stem
    mod = load_code(module_name, ABBU_CONFIG["cache_file"])
    f = getattr(mod, spec.name)
    return f
