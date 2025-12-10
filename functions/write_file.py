import os

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
