import os

from google.genai import types

from utils import resolve_and_validate_path


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        path, error = resolve_and_validate_path(working_directory, file_path)
        if error:
            return error

        assert path is not None

        parent_directory = os.path.dirname(path)
        if parent_directory:
            os.makedirs(parent_directory, exist_ok=True)

        with open(path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as ex:
        return f"Error: {ex}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the given file with the provided content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the target file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the target file.",
            ),
        },
    ),
)
