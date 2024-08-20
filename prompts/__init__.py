import utils as U
from importlib import resources


def load_prompt(prompt):
    with resources.path("prompts", f"{prompt}.txt") as prompt_path:
        return U.load_text(str(prompt_path))


def load_descriptions(description):
    with resources.path("descriptions", f"{description}.txt") as prompt_path:
        return U.load_text(str(prompt_path))
