import os
from google.genai import types


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_wdir = os.path.abspath(working_directory)

        target_dir = os.path.normpath(
            os.path.join(abs_wdir, directory)
        )

        valid_target = (
            os.path.commonpath([abs_wdir, target_dir]) == abs_wdir
        )

        if not valid_target:
            return (
                f'Error: Cannot list "{directory}" '
                f'as it is outside the permitted working directory'
            )

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result = ""

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)

            result += (
                f"- {item}: "
                f"file_size={os.path.getsize(item_path)} bytes, "
                f"is_dir={os.path.isdir(item_path)}\n"
            )

        return result.rstrip()

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to list relative to the working directory.",
            ),
        },
    ),
)
