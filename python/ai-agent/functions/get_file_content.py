import os

from google.genai import types

from config import MSG_LIMIT
from utils import resolve_and_validate_path


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        path, error = resolve_and_validate_path(working_directory, file_path)
        if error:
            return error

        assert path is not None

        if not os.path.isfile(path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(path, "r") as f:
            raw = f.read(MSG_LIMIT + 1)

            if len(raw) == MSG_LIMIT + 1:
                return (
                    raw[:MSG_LIMIT]
                    + f'[...File "{file_path}" truncated at {MSG_LIMIT} characters]'
                )
        return raw

    except Exception as ex:
        return f"Error: {ex}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Get the content of the specified file (max {MSG_LIMIT} chars), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the target file, relative to the working directory.",
            ),
        },
    ),
)
