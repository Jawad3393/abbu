import re
import os
from openai import OpenAI
from datetime import datetime, timezone, timedelta
import importlib.util
from pathlib import Path

_api_key = None

def set_api_key(key: str):
    global _api_key
    _api_key = key
    print("API key set successfully.")

def get_openai_client():
    if _api_key is None:
        raise ValueError("API key is not set. Use set_api_key('<your_api_key>') to set it.")
    return OpenAI(api_key=_api_key)

def from_spec(spec: str, use_cache: bool = True):
    def decorator(func):
        if _api_key is None:
            raise ValueError("API key is not set. Use set_api_key('<your_api_key>') to set it.")
        
        spec_hash = hash(spec)
        cache_dir = "cache"
        ensure_cache_dir(cache_dir)
        cache_file = os.path.join(cache_dir, f"cache_{spec_hash}.py")

        if use_cache and os.path.exists(cache_file):
            # Load cached function implementation
            module = load_code("cached_module", cache_file)
        else:
            # Generate function implementation
            client = get_openai_client()
            generated_code = generate_code(client, spec)
            save_code(generated_code, cache_file)
            module = load_code("generated_module", cache_file)

        func_name = func.__name__
        if hasattr(module, func_name):
            func.__code__ = getattr(module, func_name).__code__
        else:
            raise AttributeError(f"The generated module does not have the expected function '{func_name}'")

        return func

    return decorator

def generate_code(client, spec):
    prompt = create_prompt(spec)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    generated_code = response.choices[0].message.content.strip()
    cleaned_code = clean_code(generated_code)
    return cleaned_code

def create_prompt(specification):
    prompt = (
        "You are a Python developer. Based on the following specification, ensure the code is ready to run immediately with no formatting issues or syntax errors."
        "Generate a Python file.\n\n"
        "Specification:\n"
        f"{specification}\n\n"
    )
    return prompt

def clean_code(code):
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

def save_code(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

def load_code(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def ensure_cache_dir(cache_dir_path):
    Path(cache_dir_path).mkdir(exist_ok=True)

def load_cache(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        contents = file.read()
    return contents

def save_cache(contents, file_path):
    with open(file_path, 'w') as file:
        file.write(contents)

def update_cache(func, cache_contents):
    cache_contents[func.__name__] = func
    return cache_contents

def create_function(spec, cache_dir):
    func_text = call_openai(spec)
    cache_file_path = os.path.join(cache_dir, 'cache.py')
    cache_contents = load_cache(cache_file_path)
    cache_contents = update_cache(func_text, cache_contents)
    save_cache(cache_contents, cache_file_path)
    
    module_name = 'generated_func_module'
    mod = load_code(module_name, cache_file_path)
    f = getattr(mod, func_text.__name__)
    return f