import os
from typing import TypedDict


class FileInfo(TypedDict):
    name: str
    size: int
    is_dir: bool


def get_path_contents_info(full_path_abs: str) -> list[FileInfo]:
    """Gather raw file information"""
    return [
        {
            "name": item,
            "size": os.path.getsize(os.path.join(full_path_abs, item)),
            "is_dir": os.path.isdir(os.path.join(full_path_abs, item)),
        }
        for item in os.listdir(full_path_abs)
    ]


def format_contents_info(contents_info: list[FileInfo]) -> str:
    """Present file information in expected format"""
    lines = [
        f"- {item['name']}: file_size={item['size']} bytes, is_dir={item['is_dir']}"
        for item in contents_info
    ]
    return "\n".join(lines)


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        relative_target_path = os.path.join(working_directory, directory)
        absolute_working_dir_path = os.path.abspath(working_directory)
        absolute_target_path = os.path.abspath(relative_target_path)

        is_directory = os.path.isdir(absolute_target_path)
        is_within_working_dir = absolute_target_path.startswith(
            absolute_working_dir_path
        )

        if not is_within_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not is_directory:
            return f'Error: "{directory}" is not a directory'

        return format_contents_info(get_path_contents_info(absolute_target_path))

    except Exception as ex:
        return f"Error: {ex}"
