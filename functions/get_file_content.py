import os

from google.genai import types
from config import MAX_CHARS


def get_file_content(
    working_directory: str,
    file_path: str,
) -> str:
    try:
        abs_wdir = os.path.abspath(working_directory)

        target_file = os.path.normpath(
            os.path.join(abs_wdir, file_path)
        )

        valid_target = (
            os.path.commonpath([abs_wdir, target_file]) == abs_wdir
        )

        if not valid_target:
            return (
                f'Error: Cannot read "{file_path}" '
                f'as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_file):
            return (
                f'Error: File not found or is not a regular file: "{file_path}"'
            )

        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += (
                    f'\n[...File "{file_path}" '
                    f'truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory.",
            ),
        },
    ),
)
