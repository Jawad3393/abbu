
from typing import Optional

class FunctionSpec:
    def __init__(
        self,
        name: str,
        params: list[str],
        return_type: Optional[str] = None,
        description: Optional[str] = None,
        usage_examples: Optional[list[str]] = None,
    ):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.description = description
        self.usage_examples = usage_examples

    def to_prompt(self):
        spec = "Here is the function spec\n"
        spec += f"Function name {self.name}\n"
        spec += "Function parameters:\n"
        for p in self.params:
            spec += f"    {p}\n"

        if self.return_type is not None:
            spec += f"Return type: {self.return_type}\n"

        if self.description is not None:
            spec += f"Description: {self.description}\n"

        if self.usage_examples is not None:
            spec += f"Additional usage examples:\n"
            for ex in self.usage_examples:
                spec += f"    {ex}\n"
            
        return spec

