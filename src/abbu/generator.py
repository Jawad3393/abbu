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
from .cache_utils import *

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
    config: Optional[dict] = None
):
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
        code_text = extract_code_from_gpt_output(raw_text, spec)
        
        return code_text
    except Exception as e:
        print(f"Error generating code from OpenAI: {e}")
        return None
    
def extract_code_from_gpt_output(raw_text: str, spec: FunctionSpec):
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


def create_function(
    spec: FunctionSpec,
    use_cached_if_exists: bool = True,
    save_to_cache: bool = True
):
    print(f"Creating function for spec: {spec}")
    cache = load_cache(ABBU_CONFIG["cache_file"])

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
        save_cache(cache, ABBU_CONFIG["cache_file"])

    module_name = Path(ABBU_CONFIG["cache_file"]).stem
    mod = load_code(module_name, ABBU_CONFIG["cache_file"])
    f = getattr(mod, spec.name)
    return f
