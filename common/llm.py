from openai import OpenAI
from pathlib import Path
import inspect


class OpenAIResponsesWrapper:
    def __init__(self, client: OpenAI):
        self.client = client

    def __call__(self, instructions, content, model='gpt-4o-mini'):
        return self.llm(instructions, content, model=model)

    def llm(self, instructions, content, model='gpt-4o-mini'):
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": content}
        ]

        response = self.client.responses.create(
            model=model,
            input=messages,
        )

        return response.output_text


def read_prompt(path: str) -> str:
    """
    Read a prompt file located relative to the caller's file.

    Args:
        path (str): Relative path to the prompt file.
    """
    # a bit of magic to get the caller's directory
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename

    caller_dir = Path(caller_file).resolve().parent
    prompt_path = caller_dir / path

    return prompt_path.read_text(encoding='utf-8').strip()