import os
from typing import Final

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import ErrorMessage
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from prompts import SYSTEM_PROMPT

ENV_GEMINI_API_KEY: Final = "GEMINI_API_KEY"

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=SYSTEM_PROMPT,
)


def load_env() -> None:
    load_dotenv()


def get_api_key() -> str:
    api_key = os.getenv(ENV_GEMINI_API_KEY)
    if not api_key:
        raise RuntimeError(ErrorMessage.NO_API_KEY)
    return api_key


def create_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)
