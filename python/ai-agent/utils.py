import os


def resolve_and_validate_path(
    working_directory: str, directory: str = "."
) -> tuple[str | None, str | None]:
    relative_target_path = os.path.join(working_directory, directory)
    absolute_working_dir_path = os.path.abspath(working_directory)
    absolute_target_path = os.path.abspath(relative_target_path)
    is_within_working_dir = absolute_target_path.startswith(absolute_working_dir_path)

    if not is_within_working_dir:
        return (
            None,
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory',
        )

    return (absolute_target_path, None)
