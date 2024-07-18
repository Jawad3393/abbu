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


def ensure_cache_dir(cache_dir_path):
    # # TODO: move this into the setup function.
    # Specifically: somewhere around the if reset_cache block of code.
    # We kinda have to decide if you want an entire directory for the cache, or a single file
    Path(cache_dir_path).mkdir(exist_ok=True)


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


def extract_code(raw_text: str, spec: FunctionSpec):
    # TODO: need to make sure that gpt_output either matches spec.name ... or replace it
    # Find the part of the response that contains the Python code
    code_start = raw_text.find('def ')
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



def load_cache():
    cache_file = ABBU_CONFIG["cache_file"]
    if not os.path.exists(file):
        return {}
    with open(file, 'r') as file:
        contents = file.read()

    # TODO: need to convert contents to a dict[str,str]
    # This is probably non-trivial
    return contents


def update_cache(code_text: str, spec: FunctionSpec, cache: dict[str,str]):
    cache[spec.name] = code_text


def save_cache(cache: dict[str,str]):
    # TODO: Make sure the lgoic is correct?
    all_code = ""
    for func_name, func_text in cache.items():
        all_code += func_text + "\n\n"

    with open(file, 'w') as file:
        file.write(all_code)

def load_code(module_name, file):
    # TODO: Make sure this is correct ...? :)
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



def create_function(
    spec: FunctionSpec,
    use_cached_if_exists: bool = True,  # Prevents re-generation if it already exists in the cache
    name_this_parameter_correctly_about_cache_saving: bool = False,
):

    cache = load_cache()

    if use_cached_if_exists:
        # TODO: check if it exists in the cache
        if exists_in_cache:
            return cached_function_which_is_a_callable_object

    func_text = generate_code(spec)

    # Save to the cachea if we want it to
    if we_should_save_the_cache:
        update_cache(func_text, spec, cache)
        save_cache(...)

    # TODO: The python module's name is equal to its file name (without .py).
    # So you'd have to name your file generated_func_module.py for this to work (but give it a better name)
    module_name = 'generated_func_module'   # This should be ABBU_CONFIG["cache_file"].strip_the_dot_py_suffix()
    mod = load_code(module_name, cache_file)
    f = getattr(mod, func_text.__name__)
    return f
