_api_key = None  # Global variable to store the API key

def set_api_key(key: str):
    """
    Sets the global API key for the OpenAI client.

    Args:
        key (str): The API key to be set.
    """
    global _api_key
    _api_key = key

def get_openai_client():
    """
    Returns an OpenAI client instance using the stored API key.

    Returns:
        OpenAI: The OpenAI client instance.
    
    Raises:
        ValueError: If the API key is not set.
    """
    from openai import OpenAI
    if _api_key is None:
        raise ValueError("API key is not set. Use set_api_key('<your_api_key>') to set it.")
    return OpenAI(api_key=_api_key)

def refine_spec(
    spec_file: str,
    out_file: str
):
    """
    Args:
        spec_file: the file path to the specification
        out_file: where the refined spec is output
    """
    import os
    import re
    from openai import OpenAI
    from datetime import datetime, timezone, timedelta

    def read_specification(file_path):
        """This reads the specification from the file"""
        with open(file_path, 'r') as file:
            return file.read()

    def generate_prompt(specification):
        """Generates a prompt to make the specification more detailed and descriptive"""
        prompt = (
            "You are a technical writer. Based on the following brief specification, make it more detailed and descriptive, "
            "adding any necessary information that would help a developer fully understand the requirements. "
            "Ensure the specification is clear, comprehensive, and easy to follow.\n\n"
            "Specification:\n"
            f"{specification}\n\n"
         "Enhanced Specification:"
        )
        return prompt

    def clean_generated_text(text):
        """Cleans the generated text by removing backticks and unnecessary comments using parsing"""
        # Split the text into lines
        lines = text.split('\n')
    
        # Initialize an empty list to hold cleaned lines
        cleaned_lines = []
    
        # Remove backticks and unnecessary comments
        for line in lines:
            # Remove backticks
            line = line.replace('```', '')
        
            # Add the cleaned line to the list
            cleaned_lines.append(line)
    
        # Join the cleaned lines back together, removing excessive newlines
        cleaned_text = '\n'.join(cleaned_lines)
    
        # Remove any excessive newlines
        cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)
    
        return cleaned_text.strip()

    def call_openai_api(client, prompt):
        """Calls the API to enhance the specification"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        enhanced_text = response.choices[0].message.content.strip()
        cleaned_text = clean_generated_text(enhanced_text)
        return cleaned_text

    def save_to_file(content, file_path):
        """Saves the generated content to a file"""
        with open(file_path, 'w') as file:
            file.write(content)

    def enhance_specification(client, specification_file, output_file):
        """Enhances the specification and saves the result"""
        # Read the specification
        specification = read_specification(specification_file)

        # Generate prompt
        prompt = generate_prompt(specification)
    
        # Call OpenAI API
        enhanced_specification = call_openai_api(client, prompt)
    
        # Save the enhanced specification to a file
        save_to_file(enhanced_specification, output_file)

        print(f"Enhanced specification has been saved to {output_file}")

    def main(specification_file, output_file):
        client = get_openai_client()

        # Enhance the specification
        enhance_specification(client, specification_file, output_file)

        print("Enhancement process completed.")

    # Example usage:
    specification_file = spec_file  # Path to the specification file

    est = timezone(timedelta(hours=-4))  # Get current time in EST
    current_time = datetime.now(est)
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S_EST")
    output_file = f"enhanced_specification_{formatted_time}.txt"

    main(specification_file, output_file)


def genererate_code(
    spec_file: str,
    out_file: str
):
    """
    Args:
        spec_file: where the spec file for generating code is based on
        out_file: where the generated code gets written
    """
    import re
    import os
    from openai import OpenAI
    from datetime import datetime, timezone, timedelta

    def read_specification(file_path):
        """This reads the specification from the file"""
        with open(file_path, 'r') as file:
            return file.read()

    def generate_prompt(specification, current_code=None):
        """Generates a prompt for the AI based on the specification and current code"""
        if current_code:
            prompt = (
                "You are a Python developer. Based on the following specification and current code, "
                "improve the code by adding any missing features and ensuring it meets the specification. Make sure the code has no mistakes at all\n\n"
                "Specification:\n"
                f"{specification}\n\n"
                "Current Code:\n"
                f"{current_code}\n\n"
                "Make sure the file is commented and easy to understand."
            )
        else:
            prompt = (
                "You are a Python developer. Based on the following specification, ensure the code is ready to run immediately with no formatting issues or syntax errors, like backticks."
                "Generate a Python file.\n\n"
                "Specification:\n"
                f"{specification}\n\n"
                "Make sure the file is commented and easy to understand. Make sure it is ready to run with no backticks."
            )
        return prompt

    def clean_generated_code(code):
        """Cleans the generated code by removing backticks and unnecessary comments using parsing"""
    
        # Split the code into lines
        lines = code.split('\n')
    
        # Initialize an empty list to hold cleaned lines
        cleaned_lines = []
    
        # Remove backticks and unnecessary comments
        for line in lines:
            # Remove backticks
            line = line.replace('```', '')
        
            # Remove specific instructional comments
            if not (line.strip().startswith('# Below') or
                    line.strip().startswith('# Python') or
                    line.strip().startswith('# Ensure') or
                    line.strip().startswith('# In') or
                    line.strip().startswith('# The') or
                    line.strip().startswith('# This') or
                    line.strip().startswith('# Here')):
                # Remove the specific word "Python"
                line = line.replace('Python', '').replace('python', '')
            
                # Add the cleaned line to the list
                cleaned_lines.append(line)
    
        # Join the cleaned lines back together, removing excessive newlines
        cleaned_code = '\n'.join(cleaned_lines)
    
        # Remove any excessive newlines
        cleaned_code = re.sub(r'\n\s*\n', '\n', cleaned_code)
    
        return cleaned_code.strip()

    def call_openai_api(client, prompt):
        """Calls the API to generate code based on the spec."""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_code = response.choices[0].message.content.strip()
        cleaned_code = clean_generated_code(generated_code)
        return cleaned_code

    def save_to_file(content, file_path):
        """Saves the generated content to a file"""
        with open(file_path, 'w') as file:
            file.write(content)

    def generate_and_refine_code(client, specification, initial_file, output_file):
        """Generates and refines the code based on the specification"""
        # Initial code generation
        prompt = generate_prompt(specification)
        generated_code = call_openai_api(client, prompt)

        # Save the initial generated code to a file
        save_to_file(generated_code, initial_file)

        for i in range(4):
            print(f"Refinement iteration {i + 1}")
            prompt = generate_prompt(specification, generated_code)
            generated_code = call_openai_api(client, prompt)

            if i == 0:
                # Save the generated code after the first iteration to a file
                save_to_file(generated_code, initial_file.replace("initial", "after_first_iteration"))

        # Save the final generated code to a file
        save_to_file(generated_code, output_file)

    def main(specification_file, output_file):
        client = client = get_openai_client()

        # Read the specification
        specification = read_specification(specification_file)

        # Generate and refine the code
        generate_and_refine_code(client, specification, "generated_code_initial.py", output_file)

        print(f"Generated code files have been saved.")

    # Example usage:
    specification_file = spec_file  # Path to the specification file

    est = timezone(timedelta(hours=-4))  # Get current time in EST
    current_time = datetime.now(est)
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S_EST")
    output_file = f"generated_code_{formatted_time}.py"

    main(specification_file, output_file)
