import os
import sys
import random

sys.path.append("/Users/jawada/Documents/abbu/src")
import abbu

abbu.setup(
    api_key= os.getenv("OPENAI_API_KEY"),
    cache_file="/Users/jawada/Documents/CC/jawad_cache.py",
    reset_cache=True
)

spec_password = abbu.FunctionSpec(
    name="generate_password",
    params=["strength"],
    description="""
    Generate functions only, do not include your own examples.
    Generates a new password based on the desired strength. 
    The strength can be 'weak', 'medium', or 'strong'.

    - 'weak' passwords are made up of two random words from a predefined list.
    - 'medium' passwords include a mix of uppercase and lowercase letters and numbers.
    - 'strong' passwords include a mix of uppercase and lowercase letters, numbers, and symbols.

    The function should ensure that passwords do not follow an easily guessable pattern.
    """
)

def generate_password(strength):
    f = abbu.create_function(spec=spec_password)
    return f(strength)

generate_password("weak")
generate_password("medium")
