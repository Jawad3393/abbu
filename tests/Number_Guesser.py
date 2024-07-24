import os
import sys
import random
import abbu

abbu.setup(
    api_key= os.getenv("OPENAI_API_KEY"),
    cache_file="/Users/jawada/Documents/CC/jawad_cache.py",
    reset_cache=True
)


spec_guess = abbu.FunctionSpec(
    name="random_number_guesser",
    params=["user_guess", "max_range"],
    description="""
    Takes a user's guess and a maximum range, generates a random number within that range, and checks if the guess matches the randomly generated number. 
    The function should return a message indicating whether the guess was correct, too low, or too high, along with the randomly generated number.
    The random number should be generated within the function. take the numbers only from the function dont use inputs.
    """
)

def guess_number(user_guess, max_range):
    f = abbu.create_function(spec=spec_guess)
    return f(user_guess, max_range)

guess_number(5,600)